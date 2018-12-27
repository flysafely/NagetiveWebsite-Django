# from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import Template, Context, RequestContext
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from PIL import Image as im
from NTConfig import settings

from NTWebsite import MainMethods as mMs
from NTWebsite import AppConfig as aConf
from NTWebsite.models import \
NotificationTable,\
RecommendAuthor,\
SpecialTopicComment,\
SpecialTopicReadsIP,\
SpecialTopicFollow,\
SpecialTopicInfo,\
UserCircuseeCollect,\
RollCallReadsIP,\
RollCallDialogue,\
RollCallInfo,\
UserCollect,\
UserLink,\
TopicArticleStatistic,\
ArticleUserLikesOrDislikesTable,\
CommentUserLikesOrDislikesTable,\
ArticleReadsIP,\
User,\
CategoryInfo,\
ArticleComment

import sys
import os
import base64
import uuid
import time
import json

def UserInfoOperation(UserName,field,method):
    UserObject = User.objects.get(username=UserName)
    exec('UserObject.%s%s' % (field,method))
    UserObject.save()

def CommentConversation(request):
    if request.method == 'GET':
        ConfigData = mMs.GetConfig()
        ReplayedUserName = request.GET.get('replayeduser')
        ReplayedUser = User.objects.get(UT_Nick=ReplayedUserName)
        ReplayUserName = request.GET.get('replayuser')
        ReplayUser = User.objects.get(UT_Nick=ReplayUserName)
        ObjectID = request.GET.get('ObjectID')
        From = request.GET.get('from')

        PageNumber = request.GET.get(
            'PageNumber') if 'PageNumber' in request.GET.keys() else ''

        CommentsObject_Treated = []
        CommentInfos = []
        
        KeyWord = {'SpecialTopic':('SpecialTopicInfo','STI','STC'),'Article':('TopicArticleStatistic','TAS','AC')}
        TopicsObject = eval('%s.objects.get(%s_ID=ObjectID)' % (KeyWord[From][0],KeyWord[From][1]))
        
        CommentsObjectReplayUser = eval('%sComment.objects.filter(%s_%sID=TopicsObject,%s_UserNickName=ReplayUser)' % (From,KeyWord[From][2],From,KeyWord[From][2]))
        CommentsObjectReplayedUser = eval('%sComment.objects.filter(%s_%sID=TopicsObject,%s_UserNickName=ReplayedUser)' % (From,KeyWord[From][2],From,KeyWord[From][2]))
        CommentsObject = list(CommentsObjectReplayUser) + list(CommentsObjectReplayedUser)
        
        for CommentObject in CommentsObject:
            #print(CommentObject)
            if eval("CommentObject.%s_Parent != ''" % (KeyWord[From][2])): 
                if eval('%sComment.objects.get(%s_ID=CommentObject.%s_Parent).%s_UserNickName == ReplayedUser' % (From,KeyWord[From][2],KeyWord[From][2],KeyWord[From][2])) and eval("CommentObject.%s_UserNickName == ReplayUser" % (KeyWord[From][2])):
                    CommentsObject_Treated.append(CommentObject)
                if eval('%sComment.objects.get(%s_ID=CommentObject.%s_Parent).%s_UserNickName == ReplayUser' % (From,KeyWord[From][2],KeyWord[From][2],KeyWord[From][2])) and eval("CommentObject.%s_UserNickName == ReplayedUser" % (KeyWord[From][2])):
                    CommentsObject_Treated.append(CommentObject)

        for CommentObject_Treated in CommentsObject_Treated:
            if eval("CommentObject_Treated.%s_Parent != ''" % (KeyWord[From][2])):
                ParentCommentObject = eval('%sComment.objects.get(%s_ID=CommentObject_Treated.%s_Parent)' % (From,KeyWord[From][2],KeyWord[From][2]))
                CommentInfos.append(
                    ('HasParent', ParentCommentObject, CommentObject_Treated))
            else:
                CommentInfos.append(('HasNoParent', '', CommentObject_Treated))

        comment_display = 'show' if len(CommentsObject_Treated) > ConfigData['CommentsPageLimit'] else 'hide'
        # 评论数据分页
        CommentsObject = RecordsetPaging(
            CommentInfos, PageNumber, ConfigData['CommentsPageLimit'])
        page_href = '/CommentConversation?ObjectID=' + ObjectID + '&replayeduser='+ ReplayedUserName +'&replayuser=' + ReplayUserName + '&from=' + From + '&PageNumber='

        return render(request, 'Nagetive-CommentConversationBase.html', {"SearchSource": From,
                                                                         "IsCommentConversation":'True',
                                                                         "exportList_comment": CommentsObject,
                                                                         "comment_display": comment_display,
                                                                         "export_href": page_href,
                                                                         "search_placeholder": ConfigData['HotKeyWord'],
                                                                         "NotificationCount": str(NotificationCount)})


def SpecialTopicsSquareInfoGet(request):
    if request.method == 'GET':
        ConfigData = mMs.GetConfig()
        Part = request.GET.get(
            'Part') if 'Part' in request.GET.keys() else ''
        FilterWord = request.GET.get(
            'FilterWord') if 'FilterWord' in request.GET.keys() else ''
        PageNumber = request.GET.get(
            'PageNumber') if 'PageNumber' in request.GET.keys() else ''
        NotificationCount = GetNotificationCount(request)
        Query_condition = aConf.Section_Map_Field[Part]
        SpecialTopicList = GetContextData(Query_condition['TableName'],
                                        Query_condition['JudgementCondition'] + str(
                                            ConfigData['ReadsLimit']) if Part != 'SpecialTopicSearch' else Query_condition['JudgementCondition'] + "'" + FilterWord + "'",
                                        operations=Query_condition['Operations'],
                                        limit=ConfigData['TopicsLimit'])

        if Part == 'SpecialTopicContent':
            ip = mMs.GetUserIP(request)
            SpecialTopic = SpecialTopicInfo.objects.get(STI_ID=FilterWord)
            if not SpecialTopicReadsIP.objects.filter(STR_IP=ip, STR_SpecialTopicID=SpecialTopic).exists():
                try:
                    SpecialTopicReadsIP.objects.create(
                        STR_IP=ip, STR_SpecialTopicID=SpecialTopic)
                    SpecialTopic.STI_Hot += 1
                    SpecialTopic.save()
                except Exception as e:
                    return HttpResponse(aConf.UNIQUE_ERROR[str(e)])
            # 收藏状态
            if not SpecialTopicFollow.objects.filter(STF_UserNickName=request.user.username, STF_SpecialTopic=SpecialTopic):
                followstatus = 'show'
            else:
                followstatus = 'hide'
            # 评论数据获取
            CommentInfoList = SpecialTopicComment.objects.filter(
                STC_SpecialTopicID=SpecialTopicInfo.objects.get(STI_ID=FilterWord)).order_by('-STC_EditDate')
            CommentInfos = []
            for commentobject in CommentInfoList:
                if commentobject.STC_Parent:
                    ParentCommentObject = SpecialTopicComment.objects.get(
                        STC_ID=commentobject.STC_Parent)
                    CommentInfos.append(
                        ('HasParent', ParentCommentObject, commentobject))
                else:
                    CommentInfos.append(('HasNoParent', '', commentobject))
            comment_display = 'show' if len(CommentInfoList) > ConfigData['CommentsPageLimit'] else 'hide'
            # 评论数据分页
            CommentsObject = RecordsetPaging(
                CommentInfos, PageNumber, ConfigData['CommentsPageLimit'])
            page_href = '/SpecialTopicSquare?Part=SpecialTopicContent&FilterWord=' + FilterWord + '&PageNumber='
            return render(request, Query_condition['Template'], {"exportList_info": SpecialTopic,
                                                                 "SearchSource": 'SpecialTopic',
                                                                 'IsCommentConversation':'False',
                                                                 "export_collectstatus": followstatus,
                                                                 "exportList_comment": CommentsObject,
                                                                 "comment_display": comment_display,
                                                                 "export_href": page_href,
                                                                 "search_placeholder": ConfigData['HotKeyWord'],
                                                                 "NotificationCount": str(NotificationCount)})
        else:
            page_display = 'show' if len(SpecialTopicList) > ConfigData['TopicsPageLimit'] else 'hide'
            SpecialTopicPageObjects = RecordsetPaging(
                SpecialTopicList, PageNumber, ConfigData['TopicsPageLimit'])

            page_href = "/SpecialTopicSquare?Part=" + Part + '&FilterWord=' + FilterWord + '&PageNumber='

            return render(request, Query_condition['Template'], {"exportList_info": SpecialTopicPageObjects,
                                                                 "SearchSource": 'SpecialTopic',
                                                                 'IsCommentConversation':'False',
                                                                 "export_from": 'SpecialTopicsSquare',
                                                                 "topic_display": page_display,
                                                                 "export_href": page_href,
                                                                 "search_placeholder": ConfigData['HotKeyWord'],
                                                                 "NotificationCount": str(NotificationCount)})

def Circusee(request):
    if request.method =='GET':
        ConfigData = mMs.GetConfig()
        RollCallID = request.GET.get(
            'RollCallID') if 'RollCallID' in request.GET.keys() else ''
        RollCall = RollCallInfo.objects.get(RCI_ID=RollCallID)   
        if request.user.is_authenticated:
            if not UserCircuseeCollect.objects.filter(UCC_RollCall=RollCall,UCC_UserNickName=request.user):
                try:
                    UserCircuseeCollect.objects.create(UCC_UserNickName=request.user,UCC_RollCall=RollCall)
                    return HttpResponse('collect')
                except Exception as e:
                    return HttpResponse(e)
            else:
                return HttpResponse('曾经收藏过!')
        else:
            return HttpResponse('login')

def RollCallSquareInfoGet(request):
    if request.method == 'GET':
        ConfigData = mMs.GetConfig()

        Part = request.GET.get(
            'Part') if 'Part' in request.GET.keys() else ''
        FilterWord = request.GET.get(
            'FilterWord') if 'FilterWord' in request.GET.keys() else ''
        PageNumber = request.GET.get(
            'PageNumber') if 'PageNumber' in request.GET.keys() else ''

        NotificationCount = GetNotificationCount(request)
        Query_condition = aConf.Section_Map_Field[Part]
        RollCallList = GetContextData(Query_condition['TableName'],
                                        Query_condition['JudgementCondition'] + str(
                                            ConfigData['ReadsLimit']) if Part == 'RollCallIndex' else Query_condition['JudgementCondition'] + "'" + FilterWord + "'",
                                        operations=Query_condition['Operations'],
                                        limit=ConfigData['TopicsLimit'])
        if Part != 'RollCallContent':
            page_display = 'show' if len(RollCallList) > ConfigData['TopicsPageLimit'] else 'hide'
            RollCallPageObjects = RecordsetPaging(
                RollCallList, PageNumber, ConfigData['TopicsPageLimit'])

            page_href = "/RollCallSquare?Part=" + Part + '&FilterWord=' + FilterWord + '&PageNumber='

            return render(request, Query_condition['Template'], {"exportList_info": RollCallPageObjects,
                                                                 "SearchSource": 'RollCall',
                                                                 "topic_display": page_display,
                                                                 "export_href": page_href,
                                                                 "search_placeholder": ConfigData['HotKeyWord'],
                                                                 "NotificationCount": str(NotificationCount)})
        else:
            ip = mMs.GetUserIP(request)
            Article = RollCallInfo.objects.get(RCI_ID=FilterWord)
            if not RollCallReadsIP.objects.filter(RCR_IP=ip, RCR_ArticleID=Article).exists():
                try:
                    RollCallReadsIP.objects.create(
                        RCR_IP=ip, RCR_ArticleID=Article)
                    Article.RCI_Read += 1
                    Article.save()
                except Exception as e:
                    return HttpResponse(aConf.UNIQUE_ERROR[str(e)])            


            PublisherNick=RollCallList[0].RCD_ID.RCI_Publisher.UT_Nick
            TargetNick=RollCallList[0].RCD_ID.RCI_Target.UT_Nick
            if request.user.is_authenticated:

                if request.user.UT_Nick == PublisherNick:
                    Replay_Display = 'show'
                    Replay_location = 'left'
                elif request.user.UT_Nick == TargetNick:
                    Replay_Display = 'show'
                    Replay_location = 'right'   
                else:
                    Replay_Display = 'hide'
                    Replay_location = 'left'      
            else:
                Replay_Display = 'hide'
                Replay_location = 'left'
            return render(request, Query_condition['Template'],{"export_RollCallDialogue":RollCallList,
                                                                "SearchSource":'RollCall',
                                                                "Replay_Display":Replay_Display,
                                                                "Replay_location":Replay_location,
                                                                "NotificationCount": str(NotificationCount)})  

def RollCallReplay(request):
    if request.method == 'POST':
        ConfigData = mMs.GetConfig()
        RollCallReplayContent = request.POST.get('RollCallReplayContent')
        FilterWord = request.POST.get('FilterWord')
        Query_condition = aConf.Section_Map_Field['RollCallContent']
        RollCallList = GetContextData(Query_condition['TableName'],
                                        Query_condition['JudgementCondition'] + "'" + FilterWord + "'",
                                        operations=Query_condition['Operations'],
                                        limit=ConfigData['TopicsLimit'])
        RollCallListLen = len(RollCallList)
        if RollCallList[RollCallListLen-1].RCD_Reply == '':
            if request.user.UT_Nick == RollCallList[RollCallListLen-1].RCD_ID.RCI_Target.UT_Nick:
                RollCallList[RollCallListLen-1].RCD_Reply = RollCallReplayContent
                RollCallList[RollCallListLen-1].save()
                AddToNotificationTable(RollCallList[RollCallListLen-1].RCD_ID.RCI_Title,'RollCallSquare','RollCallContent','RollCallRepaly',FilterWord,RollCallList[RollCallListLen-1].RCD_ID.RCI_Publisher,request.user)
                UserInfoOperation(request.user.username,'UT_RreplayCount','+=1')
                return HttpResponse('replayok')
            else:

                return HttpResponse('对方尚未回复!')
        else:
            if request.user.UT_Nick == RollCallList[RollCallListLen-1].RCD_ID.RCI_Publisher.UT_Nick:
                RCDObject = RollCallDialogue.objects.create(RCD_ID = RollCallList[RollCallListLen-1].RCD_ID,RCD_Query=RollCallReplayContent)
                AddToNotificationTable(RCDObject.RCD_ID.RCI_Title,'RollCallSquare','RollCallContent','RollCallRepaly',FilterWord,RollCallList[RollCallListLen-1].RCD_ID.RCI_Target,request.user)
                UserInfoOperation(request.user.username,'UT_RreplayCount','+=1')
                return HttpResponse('replayok')

            else:
                return HttpResponse('对方尚未回复!')

def RollCallPublish(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            RollCallTitle = request.POST.get('RollCallTitle')
            RollCallUserNick = request.POST.get('RollCallUserNick')
            RollCallContent = request.POST.get('RollCallContent')
            Publisher = User.objects.get(username=request.user.username)
            if User.objects.filter(UT_Nick = RollCallUserNick):
                try:
                    TargetUser = User.objects.get(UT_Nick = RollCallUserNick)
                    NewRollCall = RollCallInfo.objects.create(RCI_Title=RollCallTitle,RCI_Publisher=Publisher,RCI_Target=TargetUser)
                    NewDialogue = RollCallDialogue.objects.create(RCD_ID=NewRollCall,RCD_Query=RollCallContent)

                    AddToNotificationTable(NewRollCall.RCI_Title,'RollCallSquare','RollCallContent','RollCallPublish',NewRollCall.RCI_ID,TargetUser,request.user)
                    UserInfoOperation(request.user.username,'UT_RollCallsCount','+=1')
                    return HttpResponse('publishok')
                except Exception as e:
                    return HttpResponse(e)
            else:

                return HttpResponse("用户:'"+RollCallUserNick +"'"+ '不存在!')
        else:
            return HttpResponse('login')
    


def Replay(request):
    if request.method == 'POST':
        ArticleID = request.POST.get('ArticleID')
        CommentID = request.POST.get('CommentID')
        Comment = request.POST.get('Comment') 
        From = request.POST.get('From')        
        if request.user.is_authenticated:
            userObject = User.objects.get(username=request.user.username)

            if From == 'Topic':
                Article = TopicArticleStatistic.objects.get(TAS_ID=ArticleID)
                ArticleComment.objects.create(
                    AC_ArticleID=Article, AC_Comment=Comment, AC_Parent=CommentID, AC_UserNickName=userObject)
                AddToNotificationTable(Article.TAS_Title,'Topics','Content','CommentReplay',ArticleID,Article.TAS_Author,request.user)
                UserInfoOperation(request.user.username,'UT_TreplayCount','+=1')
                return HttpResponse('replayok')
            elif From == 'SpeciaTopic':
                SpeciaTopic = SpecialTopicInfo.objects.get(STI_ID=ArticleID)
                SpecialTopicComment.objects.create(STC_SpecialTopicID=SpeciaTopic, STC_Comment=Comment, STC_Parent=CommentID, STC_UserNickName=userObject)
                AddToNotificationTable(SpeciaTopic.STI_Title,'SpecialTopicSquare','SpecialTopicContent','CommentReplay',SpeciaTopic.STI_ID,SpeciaTopic.STI_Publisher,request.user)
                UserInfoOperation(request.user.username,'UT_SreplayCount','+=1')
                return HttpResponse('replayok')
        else:
            return HttpResponse('login')


def CollectCancel(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            ArticleID = request.POST.get('ArticleID')
            UserNickName = request.user.UT_Nick
            userObject = User.objects.get(UT_Nick=UserNickName)
            UserCollect.objects.filter(
                UC_UserNickName=request.user.username, UC_Article=ArticleID)[0].delete()
            return HttpResponse('cancel')
        else:
            return HttpResponse('login')


def Collect(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            ArticleID = request.POST.get('ArticleID')
            UserNickName = request.user.UT_Nick
            userObject = User.objects.get(UT_Nick=UserNickName)
            if not UserCollect.objects.filter(UC_UserNickName=request.user.username, UC_Article=ArticleID):
                UserCollect.objects.create(
                    UC_UserNickName=request.user, UC_Article=TopicArticleStatistic.objects.get(TAS_ID=ArticleID))
                return HttpResponse('collect')
            else:
                UserCollect.objects.filter(
                    UC_UserNickName=request.user.username, UC_Article=ArticleID)[0].delete()
                return HttpResponse('cancel')
        else:
            return HttpResponse('login')

def Follow(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            SpecialTopicID = request.POST.get('SpecialTopicID')
            UserName = request.user.username
            userObject = User.objects.get(username=UserName)
            Topic = SpecialTopicInfo.objects.get(STI_ID=SpecialTopicID)
            if not SpecialTopicFollow.objects.filter(STF_UserNickName=request.user.username, STF_SpecialTopic=Topic):
                SpecialTopicFollow.objects.create(
                    STF_UserNickName=request.user, STF_SpecialTopic=Topic)
                Topic.STI_Follower += 1
                Topic.save()
                return HttpResponse('follow')
            else:
                SpecialTopicFollow.objects.filter(
                    STF_UserNickName=request.user.username, STF_SpecialTopic=Topic)[0].delete()
                Topic.STI_Follower -= 1
                Topic.save()
                return HttpResponse('cancel')
        else:

            return HttpResponse('login')        

def Link(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            UserNickName = request.POST.get('UserNickName')
            userObject = User.objects.get(UT_Nick=UserNickName)
            if not UserLink.objects.filter(UL_UserBeLinked=userObject.username, UL_UserLinking=request.user):
                UserLink.objects.create(
                    UL_UserBeLinked=userObject, UL_UserLinking=request.user)
                UserInfoOperation(request.user.username,'UT_FoucusCount','+=1')
                UserInfoOperation(userObject.username,'UT_FansCount','+=1')
                return HttpResponse('link')
            else:
                UserLink.objects.filter(
                    UL_UserBeLinked=userObject, UL_UserLinking=request.user)[0].delete()
                UserInfoOperation(request.user.username,'UT_FoucusCount','-=1')
                UserInfoOperation(userObject.username,'UT_FansCount','-=1')
                return HttpResponse('cancel')
        else:
            return HttpResponse('login')


def UserProfileUpdate(request):
    if request.method == 'POST':
        UserImageData = request.POST.get('UserImageData')
        UserImageFormat = request.POST.get('UserImageFormat')
        UserNickName = request.POST.get('UserNickName')
        UserDescription = request.POST.get('UserDescription')
        UserSex = request.POST.get('UserSex')
        UserConstellation = request.POST.get('UserConstellation')
        UserEmail = request.POST.get('UserEmail')
        UserRegion = request.POST.get('UserRegion')

        userObject = User.objects.get(username=request.user.username)

        if userObject.UT_Nick != UserNickName:
            if User.objects.filter(UT_Nick=UserNickName):
                return HttpResponse('Nick')
            else:
                print('设置昵称为', UserNickName)
                userObject.UT_Nick = UserNickName

        if UserImageData[0:4].upper() != 'HTTP':
            UserimageURL = UserAvatarOperation(
                UserImageData, UserImageFormat, request.user.UT_Avatar.split('/')[-1].split('.')[0] if request.user.UT_Avatar.split('/')[-1] != 'DefaultLogo.jpg' else None)
            userObject.UT_Avatar = UserimageURL
        userObject.UT_Sex = UserSex
        userObject.UT_Region = UserRegion
        userObject.email = UserEmail
        userObject.UT_Description = UserDescription
        userObject.UT_Constellation = UserConstellation
        userObject.save()
        return HttpResponse(userObject.UT_Nick)


def UserProfile(request):
    if request.method == "GET":
        ConfigData = mMs.GetConfig()
        usernickname = request.GET.get('UserNickName')
        username = User.objects.get(UT_Nick=usernickname).username
        PartSelection = request.GET.get('Select')
        PageNumber = request.GET.get('PageNumber')
        UserObject = User.objects.filter(UT_Nick=usernickname)[0]

        # 相关状态
        if request.user.is_authenticated and usernickname == request.user.UT_Nick:
            status = ('', '', '', '', '', 'SelfProfile')
        elif request.user.is_authenticated and usernickname != request.user.UT_Nick:
            if UserLink.objects.filter(UL_UserBeLinked=User.objects.get(UT_Nick=usernickname).username, UL_UserLinking=request.user):
                status = ('readonly', 'disabled',
                          'hidden', 'selected', 'linked', 'UserProfile')
            else:
                status = ('readonly', 'disabled', 'hidden',
                          'selected', 'link', 'UserProfile')
        else:
            status = ('readonly', 'disabled',
                      'hidden', 'selected', 'link', 'UserProfile')


        NotificationCount = GetNotificationCount(request)
        Query_condition = aConf.Section_Map_Field[PartSelection]
        ObjectList = GetContextData(Query_condition['TableName'],
                                        Query_condition['JudgementCondition'] +
                                        "'" + username + "'",
                                        Query_condition['ExtraCondition'],
                                        operations=Query_condition['Operations'],
                                        limit=ConfigData['TopicsLimit'],
                                        )
        topic_display = 'show' if len(ObjectList) > ConfigData['TopicsPageLimit'] else 'hide'

        # 获取关注信息
        LinkCount = UserLink.objects.filter(
            UL_UserLinking=User.objects.get(UT_Nick=usernickname)).count()
        LinkedCount = UserLink.objects.filter(UL_UserBeLinked=username).count()
        LinkInfo = (LinkCount, LinkedCount)
        ObjectList_Treated = []
        # 直接获取文章对象
        if PartSelection == 'Publish':
            export_type = 'Topic'
            for TopicInfo in ObjectList:
                ThemeList = TopicInfo.TAS_Theme.split(
                    '&') if TopicInfo.TAS_Theme != '' else []
                ObjectList_Treated.append((TopicInfo, ThemeList))
        # 评论文章去重输出
        elif PartSelection == 'Comment':
            export_type = 'Topic'
            tempList = []
            for TopicInfo in ObjectList:
                tempList.append(
                    str(eval("TopicInfo.%s.TAS_ID" % Query_condition['ForeignKeyField'])))
            for TopicID in set(tempList):
                Topic = TopicArticleStatistic.objects.get(TAS_ID=TopicID)
                ThemeList = Topic.TAS_Theme.split(
                    '&') if Topic.TAS_Theme != '' else []
                ObjectList_Treated.append((Topic, ThemeList))
        elif PartSelection == 'Circusee':
            export_type='Circusee'
            for rollcall in ObjectList:
                ObjectList_Treated.append(RollCallInfo.objects.get(RCI_ID = rollcall.UCC_RollCall.RCI_ID))
        elif PartSelection == 'Focuslist':
            export_type = 'Linking'
            ObjectList_Treated = ObjectList
            #print('Focuslist',ObjectPaged)
        elif PartSelection == 'Fanslist':
            export_type = 'Linked'
            ObjectList_Treated = ObjectList
            #print('Fanslist',ObjectPaged)
        # 间接获取文章对象
        elif PartSelection in ['Likes','Dislikes','Collect']:
            export_type = 'Topic'
            for TopicInfo in ObjectList:
                ThemeList = eval("TopicInfo.%s.TAS_Theme.split('&') if TopicInfo.%s.TAS_Theme != '' else []" % (
                    Query_condition['ForeignKeyField'], Query_condition['ForeignKeyField']))
                ObjectList_Treated.append(
                    (eval("TopicInfo.%s" % Query_condition['ForeignKeyField']), ThemeList))
        elif PartSelection == 'Follow':
            export_type = 'Follow'
            for TopicInfo in ObjectList:
                ObjectList_Treated.append(TopicInfo.STF_SpecialTopic)

        # 内容分页处理
        ObjectPaged = RecordsetPaging(
            ObjectList_Treated, PageNumber, ConfigData['TopicsPageLimit'])
        page_href = '/UserProfile?UserNickName=' + \
            usernickname + '&Select=' + PartSelection + '&PageNumber='
        # 返回渲染
        return render(request, 'Nagetive-UserProfile.html', {'selforguest': status,
                                                             'export_from': status[5],
                                                             'export_type': export_type,
                                                             "SearchSource": 'Topic',
                                                             'export_userinfo': UserObject,
                                                             'export_linkinfo': LinkInfo,
                                                             "exportList_info": ObjectPaged,
                                                             "topic_display": topic_display,
                                                             "export_href": page_href,
                                                             "search_placeholder": ConfigData['HotKeyWord'],
                                                             "NotificationCount": str(NotificationCount)
                                                             })


def indexView(request):

    return HttpResponseRedirect("/Topics?Part=Index&PageNumber=1")


def TopicsInfoGet(request):
    if request.method == 'GET':

        ConfigData = mMs.GetConfig()

        Part = request.GET.get(
            'Part') if 'Part' in request.GET.keys() else ''
        FilterWord = request.GET.get(
            'FilterWord') if 'FilterWord' in request.GET.keys() else ''
        PageNumber = request.GET.get(
            'PageNumber') if 'PageNumber' in request.GET.keys() else ''


        NotificationCount = GetNotificationCount(request)
        #print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',NotificationCount)
        Query_condition = aConf.Section_Map_Field[Part]
        TopicsInfoList = GetContextData(Query_condition['TableName'],
                                        Query_condition['JudgementCondition'] + str(
                                            ConfigData['ReadsLimit']) if Part in 'IndexOrderDate' else Query_condition['JudgementCondition'] + "'" + FilterWord + "'",
                                        operations=Query_condition['Operations'],
                                        limit=ConfigData['TopicsLimit'] if Part in ['Index', 'IndexOrderDate','Theme', 'Category', 'TopicSearch'] else ConfigData['CommentsLimit'])

        if Part in ['Index', 'IndexOrderDate','Theme', 'Category', 'TopicSearch']:
            TopicsInfoList_Treated = []
            CategorysInfoList = CategoryInfo.objects.all()
            RecommendAuthorInfoList = RecommendAuthor.objects.all()
            for TopicInfo in TopicsInfoList:
                ThemeList = TopicInfo.TAS_Theme.split(
                    '&') if TopicInfo.TAS_Theme != '' else []
                TopicsInfoList_Treated.append((TopicInfo, ThemeList))
            topic_display = 'show' if len(TopicsInfoList) > ConfigData['TopicsPageLimit'] else 'hide'
            TopicsObject = RecordsetPaging(
                TopicsInfoList_Treated, PageNumber, ConfigData['TopicsPageLimit'])

            page_href = "/Topics?Part=" + Part + '&FilterWord=' + FilterWord + '&PageNumber='

            return render(request, Query_condition['Template'], {"export_from": 'Index',
                                                                 "SearchSource": 'Topic',
                                                                 "exportList_info": TopicsObject,
                                                                 "exportList_category": CategorysInfoList,
                                                                 "exportList_author":RecommendAuthorInfoList,
                                                                 "topic_display": topic_display,
                                                                 "export_href": page_href,
                                                                 "search_placeholder": ConfigData['HotKeyWord'],
                                                                 "NotificationCount": str(NotificationCount)})
        elif Part == 'Content':
            ip = mMs.GetUserIP(request)
            Article = TopicArticleStatistic.objects.get(TAS_ID=FilterWord)
            if not ArticleReadsIP.objects.filter(AR_IP=ip, AR_ArticleID=Article).exists():
                try:
                    ArticleReadsIP.objects.create(
                        AR_IP=ip, AR_ArticleID=Article)
                    Article.TAS_Read += 1
                    Article.save()
                except Exception as e:
                    return HttpResponse(aConf.UNIQUE_ERROR[str(e)])
            # 收藏状态
            if not UserCollect.objects.filter(UC_UserNickName=request.user.username, UC_Article=Article):
                collectstatus = 'show'
            else:
                collectstatus = 'hide'
            # 评论数据获取
            CommentInfoList = ArticleComment.objects.filter(
                AC_ArticleID=Article).order_by('-AC_EditDate')
            CommentInfos = []
            for commentobject in CommentInfoList:
                if commentobject.AC_Parent:
                    ParentCommentObject = ArticleComment.objects.get(
                        AC_ID=commentobject.AC_Parent)
                    CommentInfos.append(
                        ('HasParent', ParentCommentObject, commentobject))
                else:
                    CommentInfos.append(('HasNoParent', '', commentobject))
            comment_display = 'show' if len(CommentInfoList) > ConfigData['CommentsPageLimit'] else 'hide'
            # 评论数据分页
            CommentsObject = RecordsetPaging(
                CommentInfos, PageNumber, ConfigData['CommentsPageLimit'])
            page_href = '/Topics?Part=Content&FilterWord=' + FilterWord + '&PageNumber='
            return render(request, Query_condition['Template'], {"exportList_info": TopicsInfoList,
                                                                 "SearchSource": 'Topic',
                                                                 "IsCommentConversation":'False',
                                                                 "export_collectstatus": collectstatus,
                                                                 "exportList_comment": CommentsObject,
                                                                 "comment_display": comment_display,
                                                                 "export_href": page_href,
                                                                 "search_placeholder": ConfigData['HotKeyWord'],
                                                                 "NotificationCount": str(NotificationCount)})
        else:
            return HttpResponse('TopicsInfoGet请求错误！')


# 查询结果分页


def RecordsetPaging(records, pagenum, valueconfig):
    paginator = Paginator(list(records), valueconfig)
    try:
        objectList = paginator.page(pagenum)
    except PageNotAnInteger:
        objectList = paginator.page(1)
    except EmptyPage:
        objectList = paginator.page(paginator.num_pages)
    return objectList


def CreateUserArticle(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            Title = request.POST.get('Title')
            Category = CategoryInfo.objects.get(
                CI_Name=request.POST.get('CategoryText'))
            ContentText = request.POST.get('ContentRichText')
            ContentPoorText = request.POST.get('ContentPoorText')
            Themes = request.POST.get('Themes')
            try:
                TopicArticleStatistic.objects.create(TAS_Author=request.user, TAS_Title=Title, TAS_Type=Category,
                                                     TAS_Content=ContentText, TAS_Description=ContentPoorText, TAS_Theme=Themes)
                UserInfoOperation(request.user.username,'UT_TopicsCount','+=1')
                return HttpResponse('ok')
            except Exception as e:
                print(aConf.UNIQUE_ERROR[str(e)])
                return HttpResponse(aConf.UNIQUE_ERROR[str(e)])
        else:
            print('未登录')
            return HttpResponse('login')


def StatisticTasteData(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            Source = request.GET.get('Source')
            ID = request.GET.get('ID')
            GetStandPoint = request.GET.get(
                'StandPoint')
            GetStandPointNum = aConf.StantPointStatusNumber[GetStandPoint]
            ConditionsParam = aConf.Taste_KeyString[Source]
            Object = eval("%s.objects.get(%s='%s')" % (
                ConditionsParam['TabelName'], ConditionsParam['ForeignKey_ID_Field'], ID))

            TasteQuerySet = eval("%s.objects.filter(%s=request.user.username,%s=Object)" % (
                ConditionsParam['TasteTableName'], ConditionsParam['UserNickName_Field'], ConditionsParam['ID_Field']))

            if TasteQuerySet.exists():
                StandPointStatus = eval("TasteQuerySet[0].%s" %
                                        ConditionsParam['StandPoint_Field'])
                if StandPointStatus == abs(GetStandPointNum):
                    if GetStandPointNum < 0:
                        if GetStandPointNum == -1:
                            TasteDataOperation(
                                ConditionsParam['TabelName'], ConditionsParam['Like_Field'], '-', ID)
                        elif GetStandPointNum == -2:
                            TasteDataOperation(
                                ConditionsParam['TabelName'], ConditionsParam['Dislike_Field'], '-', ID)
                        TasteQuerySet[0].delete()
                        return HttpResponse(GetStandPoint + 'Success')
                    else:
                        return HttpResponse('None')
                else:
                    if GetStandPointNum == 1:
                        TasteDataOperation(
                            ConditionsParam['TabelName'], ConditionsParam['Like_Field'], '+', ID)
                        TasteDataOperation(
                            ConditionsParam['TabelName'], ConditionsParam['Dislike_Field'], '-', ID)
                    elif GetStandPointNum == 2:
                        TasteDataOperation(
                            ConditionsParam['TabelName'], ConditionsParam['Like_Field'], '-', ID)
                        TasteDataOperation(
                            ConditionsParam['TabelName'], ConditionsParam['Dislike_Field'], '+', ID)
                    eval("TasteQuerySet.update(%s=GetStandPointNum)" %
                         ConditionsParam['StandPoint_Field'])
                    return HttpResponse(GetStandPoint + 'Success')
            else:
                eval("%s.objects.create(%s=request.user,%s=Object,%s=GetStandPointNum)" % (
                    ConditionsParam['TasteTableName'], ConditionsParam['UserNickName_Field'], ConditionsParam['ID_Field'], ConditionsParam['StandPoint_Field']))

                if GetStandPoint == 'Like':
                    TasteDataOperation(
                        ConditionsParam['TabelName'], ConditionsParam['Like_Field'], '+', ID)
                    return HttpResponse(GetStandPoint + 'Success')
                else:
                    TasteDataOperation(
                        ConditionsParam['TabelName'], ConditionsParam['Dislike_Field'], '+', ID)
                    return HttpResponse(GetStandPoint + 'Success')

        else:
            return HttpResponse('login')

# 文章统计数据操作


def TasteDataOperation(tableName, fieldName, method, param):
    Records = eval("%s.objects.get(%s_ID='%s')" %
                   (tableName, fieldName.split("_")[0], param))

    if method == '-':
        exec('Records.%s-= 1' % (fieldName))
        Records.save()
    else:
        exec('Records.%s+= 1' % (fieldName))
        Records.save()


def Login(request):
    if request.method == 'GET':

        return render(request, 'Nagetive-Login.html')

    if request.method == 'POST':
        # 注册信息获取
        username = request.POST.get('username')
        userpassword = request.POST.get('password')
        user = auth.authenticate(username=username, password=userpassword)

        if user:
            login(request, user)
            return HttpResponse(True)
        else:
            return HttpResponse("")
# 注册界面


def Regist(request):
    if request.method == 'GET':
        return render(request, 'Nagetive-Regist.html')
    if request.method == 'POST':
        userimageURL = UserAvatarOperation(request.POST.get(
            'userimagedata'), request.POST.get('userimageformat'))
        username = request.POST.get('username')
        usernickname = request.POST.get('usernickname')
        password = request.POST.get('password')
        email = request.POST.get('email')
        try:
                #CheckInDate = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
                # 这里通过前端注册账号一定要是要create_user 不然后期登录的时候  auth.authenticate无法验证用户名和密码
            User.objects.create_user(
                username, UT_Nick=usernickname, password=password, email=email, UT_Avatar=userimageURL)
            return HttpResponse('ok')

        except Exception as e:
            print("问题描述:", aConf.UNIQUE_ERROR[str(e)])
            return HttpResponse(aConf.UNIQUE_ERROR[str(e)])


def Logout(request):
    if request.method == 'GET':
        auth.logout(request)
        return HttpResponse('Logout')

@csrf_exempt
def UploadImg(request):
    if request.method == 'GET':
        print('UploadImg method is GET!!!!')
    else:
        return HttpResponse(True)

#@login_required(redirect_field_name='')
def Comment(request):
    if request.method == 'POST':
        From = request.POST.get('From')
        ArticleID = request.POST.get('ArticleID')
        CommentInfo = request.POST.get('TextAreaValue')
        if request.user.is_authenticated:
            UserObject = User.objects.get(
                username=request.user.username)
            if From == 'Topic':
                Article = TopicArticleStatistic.objects.get(TAS_ID=ArticleID)
                CommentObject = ArticleComment(
                    AC_Comment=CommentInfo, AC_UserNickName=UserObject, AC_ArticleID=Article)
                CommentObject.save()
                # 评论数统计
                Article.TAS_Comment += 1
                Article.save()
                AddToNotificationTable(Article.TAS_Title,'Topics','Content','Comment',ArticleID,Article.TAS_Author,request.user)
                UserInfoOperation(request.user.username,'UT_TreplayCount','+=1')
                return HttpResponse('ok')
            elif From == 'SpecialTopic':
                SpecialTopic = SpecialTopicInfo.objects.get(STI_ID=ArticleID)
                CommentObject = SpecialTopicComment(STC_Comment=CommentInfo,STC_UserNickName=UserObject, STC_SpecialTopicID=SpecialTopic)
                CommentObject.save()
                SpecialTopic.STI_Comment += 1
                SpecialTopic.save()
                AddToNotificationTable(SpecialTopic.STI_Title,'SpecialTopicSquare','SpecialTopicContent','Comment',ArticleID,SpecialTopic.STI_Publisher,request.user)
                UserInfoOperation(request.user.username,'UT_SreplayCount','+=1')
                return HttpResponse('ok')                
        else:
            return HttpResponse('login')


def AddToNotificationTable(title,url, part, sign, keyid, targetUser,sourceUser):
    try:
        NotificationTable.objects.create(NT_Title=title,NT_KeyID=keyid,NT_Part=part,NT_Sign=sign,NT_URL=url,NT_TargetUser=targetUser,NT_SourceUser=sourceUser)
    except Exception as e:
        raise e

def GetNotificationInfo(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            try:
                NotificationObjects = NotificationTable.objects.filter(NT_TargetUser=request.user)
                if NotificationObjects:
                    dataList = []
                    for Object in NotificationObjects:
                        dataDict = {}
                        dataDict['NT_ID'] = str(Object.NT_ID)
                        dataDict['NT_KeyID'] = Object.NT_KeyID
                        dataDict['NT_URL'] = Object.NT_URL
                        dataDict['NT_Title'] = Object.NT_Title
                        dataDict['NT_Part'] = Object.NT_Part
                        dataDict['NT_Sign'] = Object.NT_Sign
                        dataDict['NT_SourceUser'] = Object.NT_SourceUser.UT_Nick
                        dataList.append(dataDict)
                    #print(dataList)
                    jsondata = json.dumps(dataList,ensure_ascii=False)
                    return HttpResponse(jsondata)
                else:
                    return HttpResponse('None')

            except Exception as e:
                raise e
        else:
            return HttpResponse('login')

@csrf_exempt
def RemoveNotificationInfo(request):
    if request.method == 'POST':
        NT_ID_Datas = request.POST.get('NT_ID').split(',')
        print('***********^^^^^^^^^^^^^^',len(NT_ID_Datas))
        
        if request.user.is_authenticated:
            if len(NT_ID_Datas) == 1:
                try:
                    NotificationTable.objects.get(NT_ID=NT_ID_Datas[0]).delete()
                    return HttpResponse('OneDeleteOk')
                except Exception as e:
                    raise
            else:
                for NT_ID_Data in NT_ID_Datas:
                    try:
                        NotificationTable.objects.get(NT_ID=NT_ID_Data).delete()
                
                    except Exception as e:
                        raise   
                return HttpResponse('AllDeleteOk')                 
        

def GetNotificationCount(requestObject):
    if requestObject.user.is_authenticated:
        try:
            #NotificationTable.objects.filter(NT_TargetUser=requestObject.user)[0].delete()
            return NotificationTable.objects.filter(NT_TargetUser=requestObject.user).count()
        except Exception as e:
            raise e
    else:
        return 0

def GetTemplate(templateName):

    # 读取card模板html信息
    return Template(mMs.GetStringFromHtml(aConf.temlatesDIR, templateName))

# 数据获取


def GetContextData(TableName, *conditions, **others):
    # 关于查询数据库的性能优化:https://www.jb51.net/article/124433.htm
    # print("%s.objects.filter(%s%s'%s').order_by('%s')[0:aConf.IndexCardLimit]" % (
    #    TableName, field, Judgement, conditions, others['orderby']))
    print('**************************', "%s.objects.filter(%s)%s[0:%s]" % (
        TableName, ','.join(conditions), others['operations'], others['limit']))
    return eval("%s.objects.filter(%s)%s[0:%s]" % (TableName, ','.join(conditions), others['operations'], others['limit']))

# 上传头像处理存储


def UserAvatarOperation(ImageData, ImageFormat, Original=None):
    ConfigData = mMs.GetConfig()
    if ImageData and ImageFormat:
        AvatarUUID = str(uuid.uuid1())
        savePath = settings.MEDIA_ROOT + '/Avatar'
        if os.path.exists(savePath) == False:
            os.makedirs(savePath)
        saveFile = AvatarUUID + '.' + ImageFormat if not Original else Original + \
            str(time.time()).split('.')[0] + '.' + ImageFormat
        saveFilePath = savePath + '/' + saveFile
        with open(saveFilePath, 'wb') as picHandle:
            picHandle.write(base64.b64decode(ImageData.split('base64')[1]))
        with im.open(saveFilePath) as sizeHandle:
            compress_avatar = sizeHandle.resize(
                (ConfigData['AvatarResolution'], ConfigData['AvatarResolution']), im.BILINEAR)
            compress_avatar.save(saveFilePath)
        return '/static/media/Avatar/' + saveFile
    else:
        return '/static/media/DefaultLogo.jpg'


def CheckExists(username):

    return len(UserTable.objects.filter(UT_Name=username))
