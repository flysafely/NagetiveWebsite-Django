from .improtFiles.views_import_head import *
from .models import *

def UserInfoOperation(UserName,field,method):
    UserObject = QDBC(TableName='User',QueryMethod='get',username=UserName)
    exec('UserObject.%s%s' % (field,method))
    UserObject.save()

def CommentConversation(request):
    if request.method == 'GET':
        ConfigData = mMs.GetConfig()
        ReplayedUserName = request.GET.get('replayeduser')
        ReplayedUser = QDBC(TableName='User',QueryMethod='get',UT_Nick=ReplayedUserName)
        ReplayUserName = request.GET.get('replayuser')
        ReplayUser = QDBC(TableName='User',QueryMethod='get',UT_Nick=ReplayUserName)
        ObjectID = request.GET.get('ObjectID')
        From = request.GET.get('from')

        PageNumber = request.GET.get(
            'PageNumber') if 'PageNumber' in request.GET.keys() else ''
        NotificationCount = GetNotificationCount(request)
        CommentsObject_Treated = []
        CommentInfos = []
        
        KeyWord = {'SpecialTopic':('SpecialTopicInfo','STI','STC'),'Article':('TopicArticleStatistic','TAS','AC')}
        TopicsObject = eval('%s.objects.get(%s_ID=ObjectID)' % (KeyWord[From][0],KeyWord[From][1]))
        
        CommentsObjectReplayUser = eval('%sComment.objects.filter(%s_%sID=TopicsObject,%s_UserNickName=ReplayUser)' % 
            (From,KeyWord[From][2],From,KeyWord[From][2]))
        CommentsObjectReplayedUser = eval('%sComment.objects.filter(%s_%sID=TopicsObject,%s_UserNickName=ReplayedUser)' % 
            (From,KeyWord[From][2],From,KeyWord[From][2]))
        CommentsObject = list(CommentsObjectReplayUser) + list(CommentsObjectReplayedUser)
        
        for CommentObject in CommentsObject:
            if eval("CommentObject.%s_Parent != ''" % (KeyWord[From][2])): 
                if eval('%sComment.objects.get(%s_ID=CommentObject.%s_Parent).%s_UserNickName == ReplayedUser' % 
                    (From,KeyWord[From][2],KeyWord[From][2],KeyWord[From][2])) and eval("CommentObject.%s_UserNickName == ReplayUser" % (KeyWord[From][2])):
                    CommentsObject_Treated.append(CommentObject)
                if eval('%sComment.objects.get(%s_ID=CommentObject.%s_Parent).%s_UserNickName == ReplayUser' % 
                    (From,KeyWord[From][2],KeyWord[From][2],KeyWord[From][2])) and eval("CommentObject.%s_UserNickName == ReplayedUser" % (KeyWord[From][2])):
                    CommentsObject_Treated.append(CommentObject)

        for CommentObject_Treated in CommentsObject_Treated:
            if eval("CommentObject_Treated.%s_Parent != ''" % (KeyWord[From][2])):
                ParentCommentObject = eval('%sComment.objects.get(%s_ID=CommentObject_Treated.%s_Parent)' % 
                    (From,KeyWord[From][2],KeyWord[From][2]))
                CommentInfos.append(
                    ('HasParent', ParentCommentObject, CommentObject_Treated))
            else:
                CommentInfos.append(('HasNoParent', '', CommentObject_Treated))

        # 评论数据分页
        CommentsObject = RecordsetPaging(
            CommentInfos, PageNumber, ConfigData['CommentsPageLimit'])
        page_card_display = CommentsObject.paginator.num_pages
        page_href = '/CommentConversation?ObjectID=' + ObjectID + '&replayeduser='+ ReplayedUserName +'&replayuser=' + ReplayUserName + '&from=' + From + '&PageNumber='

        return render(request, 'Nagetive-CommentConversationBase.html', {"SearchSource": From,
                                                                         "IsCommentConversation":'True',
                                                                         "exportList_cards": CommentsObject,
                                                                         #"comment_display": comment_display,
                                                                         "page_card_display":page_card_display,
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
        Query_Params = aConf.Part_Dict[Part]

        SpecialTopicList = QDBC(TableName=Query_Params['TableName'], 
                                QueryMethod='filter',
                                DefaultCondition=Query_Params['DefaultField'] + "=" + (ConfigData['ReadsThreshold'] if Part == 'SpecialTopicHot' else "'" + FilterWord + "'"),
                                operations=Query_Params['Operations'],
                                limit=ConfigData['TopicsLimit'])
        if Part == 'SpecialTopicContent':
            ip = mMs.GetUserIP(request)
            SpecialTopic = QDBC(TableName='SpecialTopicInfo',
                                QueryMethod='get',
                                STI_ID=FilterWord)
            if not QDBC(TableName='SpecialTopicReadsIP',
                        QueryMethod='filter',
                        STR_IP=ip, 
                        STR_SpecialTopicID=SpecialTopic,
                        Refresh=True).exists():
                try:
                    QDBC(TableName='SpecialTopicReadsIP',
                         QueryMethod='create',
                         STR_IP=ip, 
                         STR_SpecialTopicID=SpecialTopic,
                         Refresh=True)
                    SpecialTopic.STI_Hot += 1
                    SpecialTopic.save()
                except Exception as e:
                    return HttpResponse(aConf.UNIQUE_ERROR[str(e)])
            # 收藏状态
            if not QDBC(TableName='SpecialTopicFollow',
                        QueryMethod='filter',
                        STF_UserNickName=request.user.username, 
                        STF_SpecialTopic=SpecialTopic,
                        Refresh=True):
                followstatus = 'show'
            else:
                followstatus = 'hide'
            # 评论数据获取
            CommentInfoList = QDBC(TableName='SpecialTopicComment',
                                   QueryMethod='filter',
                                   STC_SpecialTopicID=QDBC(TableName='SpecialTopicInfo',
                                                           QueryMethod='get',
                                                           STI_ID=FilterWord),
                                   operations=".order_by('-STC_EditDate')")
            CommentInfos = []
            for commentobject in CommentInfoList:
                if commentobject.STC_Parent:
                    ParentCommentObject = QDBC(TableName='SpecialTopicComment',
                                               QueryMethod='get',
                                               STC_ID=commentobject.STC_Parent)
                    CommentInfos.append(
                        ('HasParent', ParentCommentObject, commentobject))
                else:
                    CommentInfos.append(('HasNoParent', '', commentobject))
            # 评论数据分页
            CommentsObject = RecordsetPaging(
                CommentInfos, PageNumber, ConfigData['CommentsPageLimit'])
            page_card_display = CommentsObject.paginator.num_pages

            page_href = '/SpecialTopicSquare?Part=SpecialTopicContent&FilterWord=' + FilterWord + '&PageNumber='
            return render(request, Query_Params['Template'], {"SpecialTopicContent": SpecialTopic,
                                                                 "SearchSource": 'SpecialTopic',
                                                                 'IsCommentConversation':'False',
                                                                 "export_collectstatus": followstatus,
                                                                 "exportList_cards": CommentsObject,
                                                                 "page_card_display": page_card_display,
                                                                 "export_href": page_href,
                                                                 "search_placeholder": ConfigData['HotKeyWord'],
                                                                 "NotificationCount": str(NotificationCount)})
        else:
            SpecialTopicPageObjects = RecordsetPaging(
                SpecialTopicList, PageNumber, ConfigData['SpecialTopicsPageLimit'])
            page_card_display = SpecialTopicPageObjects.paginator.num_pages
            page_href = "/SpecialTopicSquare?Part=" + Part + '&FilterWord=' + FilterWord + '&PageNumber='

            return render(request, Query_Params['Template'], {"exportList_cards": SpecialTopicPageObjects,
                                                                 "SearchSource": 'SpecialTopic',
                                                                 'IsCommentConversation':'False',
                                                                 "export_from": 'SpecialTopicsSquare',
                                                                 "page_card_display": page_card_display,
                                                                 "export_href": page_href,
                                                                 "search_placeholder": ConfigData['HotKeyWord'],
                                                                 "NotificationCount": str(NotificationCount)})

def Circusee(request):
    if request.method =='GET':
        ConfigData = mMs.GetConfig()
        RollCallID = request.GET.get(
            'RollCallID') if 'RollCallID' in request.GET.keys() else ''

        RollCallID = QDBC(TableName='RollCallInfo',
                          QueryMethod='get',
                          RCI_ID=RollCallID)
        if request.user.is_authenticated:
            if not QDBC(TableName='UserCircuseeCollect',
                        QueryMethod='filter',
                        UCC_RollCall=RollCall,
                        UCC_UserNickName=request.user,
                        Refresh=True):
                try:
                    QDBC(TableName='UserCircuseeCollect',
                         QueryMethod='create',
                         UCC_UserNickName=request.user,
                         UCC_RollCall=RollCall,
                         Refresh=True)
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
        Query_Params = aConf.Part_Dict[Part]

        RollCallList = QDBC(TableName=Query_Params['TableName'], 
                            QueryMethod='filter',
                            DefaultCondition=Query_Params['DefaultField'] + "=" + (ConfigData['ReadsThreshold'] if Part == 'RollCallIndex' else "'" + FilterWord + "'"),
                            operations=Query_Params['Operations'],
                            limit=ConfigData['TopicsLimit'])

        if Part != 'RollCallContent':

            RollCallPageObjects = RecordsetPaging(
                RollCallList, PageNumber, ConfigData['RollCallsPageLimit'])
            page_card_display = RollCallPageObjects.paginator.num_pages
            page_href = "/RollCallSquare?Part=" + Part + '&FilterWord=' + FilterWord + '&PageNumber='

            return render(request, Query_Params['Template'], {"exportList_cards": RollCallPageObjects,
                                                                 "SearchSource": 'RollCall',
                                                                 "page_card_display": page_card_display,
                                                                 "export_href": page_href,
                                                                 "search_placeholder": ConfigData['HotKeyWord'],
                                                                 "NotificationCount": str(NotificationCount)})
        else:
            ip = mMs.GetUserIP(request)
            RollCall = QDBC(TableName='RollCallInfo',
                            QueryMethod='get',
                            RCI_ID=FilterWord)
            if not QDBC(TableName='RollCallReadsIP',
                        QueryMethod='filter',
                        RCR_IP=ip, 
                        RCR_ArticleID=RollCall,
                        Refresh=True).exists():
                try:
                    QDBC(TableName='RollCallReadsIP',
                         QueryMethod='create',
                         RCR_IP=ip, 
                         RCR_ArticleID=RollCall)
                    RollCall.RCI_Read += 1
                    RollCall.save()
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
            return render(request, Query_Params['Template'],{"export_RollCallDialogue":RollCallList,
                                                                "SearchSource":'RollCall',
                                                                "Replay_Display":Replay_Display,
                                                                "Replay_location":Replay_location,
                                                                "NotificationCount": str(NotificationCount)})  

def RollCallReplay(request):
    if request.method == 'POST':
        ConfigData = mMs.GetConfig()
        RollCallReplayContent = request.POST.get('RollCallReplayContent')
        FilterWord = request.POST.get('FilterWord')
        Query_Params = aConf.Part_Dict['RollCallContent']

        RollCallList = QDBC(TableName=Query_Params['TableName'],
                            QueryMethod='filter',
                            DefaultCondition=Query_Params['DefaultField'] + "='" + FilterWord + "'",
                            operations=Query_Params['Operations'],
                            limit=ConfigData['TopicsLimit'])
        RollCallListLen = len(RollCallList)
        if RollCallList[RollCallListLen-1].RCD_Reply == '':
            if request.user.UT_Nick == RollCallList[RollCallListLen-1].RCD_ID.RCI_Target.UT_Nick:
                RollCallList[RollCallListLen-1].RCD_Reply = RollCallReplayContent
                RollCallList[RollCallListLen-1].save()
                AddToNotificationTable('',RollCallList[RollCallListLen-1].RCD_ID.RCI_Title,'RollCallSquare','RollCallContent','RollCallRepaly',FilterWord,RollCallList[RollCallListLen-1].RCD_ID.RCI_Publisher,request.user)
                UserInfoOperation(request.user.username,'UT_RreplayCount','+=1')
                return HttpResponse('replayok')
            else:

                return HttpResponse('对方尚未回复!')
        else:
            if request.user.UT_Nick == RollCallList[RollCallListLen-1].RCD_ID.RCI_Publisher.UT_Nick:
                RCDObject =QDBC(TableName='RollCallDialogue',
                                QueryMethod='create',
                                RCD_ID = RollCallList[RollCallListLen-1].RCD_ID, 
                                RCD_Query = RollCallReplayContent,
                                Refresh=True)
                AddToNotificationTable('',RCDObject.RCD_ID.RCI_Title,'RollCallSquare','RollCallContent','RollCallRepaly',FilterWord,RollCallList[RollCallListLen-1].RCD_ID.RCI_Target,request.user)
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
            Publisher = QDBC(TableName='User',
                             QueryMethod='get',
                             username=request.user.username)
            if QDBC(TableName='User',
                    QueryMethod='get',
                    UT_Nick = RollCallUserNick,
                    Refresh=True):
                try:
                    TargetUser = QDBC(TableName='User',
                                      QueryMethod='get',
                                      UT_Nick = RollCallUserNick)
                    NewRollCall = QDBC(TableName='RollCallInfo',
                                       QueryMethod='create',
                                       RCI_Title=RollCallTitle,
                                       RCI_Publisher=Publisher,
                                       RCI_Target=TargetUser)
                    NewDialogue = QDBC(TableName='RollCallDialogue',
                                       QueryMethod='create',
                                       RCD_ID=NewRollCall,
                                       RCD_Query=RollCallContent)

                    AddToNotificationTable("",NewRollCall.RCI_Title,'RollCallSquare','RollCallContent','RollCallPublish',NewRollCall.RCI_ID,TargetUser,request.user)
                    UserInfoOperation(request.user.username,'UT_RollCallsCount','+=1')
                    return HttpResponse('publishok')
                except Exception as e:
                    if 'UNIQUE' in e:
                        return HttpResponse('titleisexisted')
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
            userObject = QDBC(TableName='User',
                              QueryMethod='get',
                              username=request.user.username)

            if From == 'Topic':
                Article = QDBC(TableName='TopicArticleStatistic',
                               QueryMethod='get',
                               TAS_ID=ArticleID)
                Article = QDBC(TableName='ArticleComment',
                               QueryMethod='create',
                               AC_ArticleID=Article, 
                               AC_Comment=Comment, 
                               AC_Parent=CommentID, 
                               AC_UserNickName=userObject)
                AddToNotificationTable(ArticleCommentObject.AC_ID,Article.TAS_Title,'Topics','Content','CommentReplay',ArticleID,Article.TAS_Author,request.user)
                UserInfoOperation(request.user.username,'UT_TreplayCount','+=1')
                return HttpResponse('replayok')
            elif From == 'SpeciaTopic':
                SpeciaTopic = QDBC(TableName='SpecialTopicInfo', 
                                   QueryMethod='get',
                                   STI_ID=ArticleID)
                SpecialTopicCommentObject = QDBC(TableName='SpecialTopicComment',
                                                 QueryMethod='create',
                                                 STC_SpecialTopicID=SpeciaTopic, 
                                                 STC_Comment=Comment, 
                                                 STC_Parent=CommentID, 
                                                 STC_UserNickName=userObject)
                AddToNotificationTable(SpecialTopicCommentObject.STC_ID,SpeciaTopic.STI_Title,'SpecialTopicSquare','SpecialTopicContent','CommentReplay',SpeciaTopic.STI_ID,SpeciaTopic.STI_Publisher,request.user)
                UserInfoOperation(request.user.username,'UT_SreplayCount','+=1')
                return HttpResponse('replayok')
        else:
            return HttpResponse('login')


def CollectCancel(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            ArticleID = request.POST.get('ArticleID')
            UserNickName = request.user.UT_Nick
            userObject = QDBC(TableName='User',
                              QueryMethod='get',
                              UT_Nick=UserNickName)
            QDBC(TableName='UserCollect',
                 QueryMethod='filter',
                 UC_UserNickName=request.user.username, 
                 UC_Article=ArticleID)[0].delete()
            return HttpResponse('cancel')
        else:
            return HttpResponse('login')


def Collect(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            ArticleID = request.POST.get('ArticleID')
            UserNickName = request.user.UT_Nick
            userObject = QDBC(TableName='User',
                              QueryMethod='get',
                              UT_Nick=UserNickName)
            if not QDBC(TableName='UserCollect',
                        QueryMethod='filter',
                        UC_UserNickName=request.user.username, 
                        UC_Article=ArticleID,Refresh=True):
                QDBC(TableName='UserCollect',
                     QueryMethod='create',
                     UC_UserNickName=request.user, 
                     UC_Article=QDBC(TableName='TopicArticleStatistic',
                                     QueryMethod='get',
                                     TAS_ID=ArticleID),
                     Refresh=True)
                return HttpResponse('collect')
            else:
                QDBC(TableName='UserCollect',
                     QueryMethod='filter',
                     UC_UserNickName=request.user.username, 
                     UC_Article=ArticleID)[0].delete()
                return HttpResponse('cancel')
        else:
            return HttpResponse('login')

def Follow(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            SpecialTopicID = request.POST.get('SpecialTopicID')
            UserName = request.user.username
            userObject = QDBC(TableName='User',
                              QueryMethod='get',
                              username=UserName)
            Topic = QDBC(TableName='SpecialTopicInfo',
                         QueryMethod='get',
                         STI_ID=SpecialTopicID,
                         Refresh=True)
            if not QDBC(TableName='SpecialTopicFollow',
                        QueryMethod='filter',
                        STF_UserNickName=request.user.username, 
                        STF_SpecialTopic=Topic,
                        Refresh=True):
                QDBC(TableName='SpecialTopicFollow',
                     QueryMethod='create',
                     STF_UserNickName=request.user, 
                     STF_SpecialTopic=Topic,
                     Refresh=True)
                Topic.STI_Follower += 1
                Topic.save()
                return HttpResponse('follow')
            else:
                QDBC(TableName='SpecialTopicFollow',
                     QueryMethod='filter',
                     STF_UserNickName=request.user.username, 
                     STF_SpecialTopic=Topic)[0].delete()
                Topic.STI_Follower -= 1
                Topic.save()
                return HttpResponse('cancel')
        else:

            return HttpResponse('login')        

def Link(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            UserNickName = request.POST.get('UserNickName')
            userObject = QDBC(TableName='User',
                              QueryMethod='get',
                              UT_Nick=UserNickName)
            if not QDBC(TableName='UserLink',
                        QueryMethod='filter',
                        UL_UserBeLinked=userObject.username, 
                        UL_UserLinking=request.user,
                        Refresh=True):

                    if not QDBC(TableName='BlackList',
                             QueryMethod='filter',
                             BL_User=request.user,
                             BL_Handler=userObject,
                             Refresh=True):
                        BlackListDeleteObject = QDBC(TableName='BlackList',
                                                     QueryMethod='filter',
                                                     BL_User=userObject,
                                                     BL_Handler=request.user,
                                                     Refresh=True)
                        if BlackListDeleteObject:
                            BlackListDeleteObject[0].delete()
                            return HttpResponse('blockcancel')

                        else:
                            QDBC(TableName='UserLink',
                                 QueryMethod='create',
                                 UL_UserBeLinked=userObject, 
                                 UL_UserLinking=request.user,
                                 Refresh=True)
                            UserInfoOperation(request.user.username,'UT_FoucusCount','+=1')
                            UserInfoOperation(userObject.username,'UT_FansCount','+=1')
                            return HttpResponse('link')
                    else:
                        return HttpResponse('block')
            else:
                QDBC(TableName='UserLink',
                     QueryMethod='get',
                     UL_UserBeLinked=userObject, 
                     UL_UserLinking=request.user,operations='.delete()',Refresh=True)
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

        userObject = QDBC(TableName='User',
                          QueryMethod='get',
                          username=request.user.username)
        if userObject.UT_Nick != UserNickName:
            if QDBC(TableName='User',
                    QueryMethod='filter',
                    UT_Nick=UserNickName):
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
        username = QDBC(TableName='User', 
                        QueryMethod='get',
                        UT_Nick=usernickname).username
        PartSelection = request.GET.get('Select')
        PageNumber = request.GET.get('PageNumber')
        UserObject = QDBC(TableName='User', 
                          QueryMethod='get',
                          UT_Nick=usernickname)
        # 相关状态
        if request.user.is_authenticated and usernickname == request.user.UT_Nick:
            status = ('', '', '', '', '', 'SelfProfile')
        elif request.user.is_authenticated and usernickname != request.user.UT_Nick:
            if QDBC(TableName='UserLink',
                    QueryMethod='filter',
                    UL_UserBeLinked=QDBC(TableName='User',
                                         QueryMethod='get',
                                         UT_Nick=usernickname).username, 
                    UL_UserLinking=request.user,
                    Refresh=True):
                status = ('readonly', 'disabled',
                          'hidden', 'selected', 'linked', 'UserProfile')
            elif QDBC(TableName='BlackList',
                      QueryMethod='filter',
                      BL_User=QDBC(TableName='User',
                                   QueryMethod='get',
                                   UT_Nick=usernickname),
                      BL_Handler=request.user,
                      Refresh=True):
                status = ('readonly', 'disabled',
                          'hidden', 'selected', 'blocked', 'UserProfile')                
            else:
                status = ('readonly', 'disabled', 'hidden',
                          'selected', 'link', 'UserProfile')
        else:
            status = ('readonly', 'disabled',
                      'hidden', 'selected', 'link', 'UserProfile')


        NotificationCount = GetNotificationCount(request)
        Query_Params = aConf.Part_Dict[PartSelection]

        ObjectList = QDBC(TableName=Query_Params['TableName'], 
                          QueryMethod='filter',
                          DefaultCondition=Query_Params['DefaultField'] + "='" + username + "'",
                          operations=Query_Params['Operations'],
                          limit=ConfigData['TopicsLimit'],
                          Refresh=True)


        # 获取关注信息
        LinkCount = QDBC(TableName='UserLink',
                         QueryMethod='filter',
                         UL_UserLinking=QDBC(TableName='User',
                                             QueryMethod='get',
                                             UT_Nick=usernickname),
                         operations='.count()')
        LinkedCount = QDBC(TableName='UserLink',
                           QueryMethod='filter',
                           UL_UserBeLinked=username,
                           operations='.count()')
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
                    str(eval("TopicInfo.%s.TAS_ID" % Query_Params['ForeignKeyField'])))
            for TopicID in set(tempList):
                #Topic = TopicArticleStatistic.objects.get(TAS_ID=TopicID)
                Topic = QDBC(TableName='TopicArticleStatistic',
                             QueryMethod='get',
                             TAS_ID=TopicID)
                ThemeList = Topic.TAS_Theme.split(
                    '&') if Topic.TAS_Theme != '' else []
                ObjectList_Treated.append((Topic, ThemeList))
        elif PartSelection == 'Circusee':
            export_type='Circusee'
            for rollcall in ObjectList:
                ObjectList_Treated.append(QDBC(TableName='RollCallInfo',
                                               QueryMethod='get',
                                               RCI_ID = rollcall.UCC_RollCall.RCI_ID))
        elif PartSelection == 'Focuslist':
            export_type = 'Linking'
            ObjectList_Treated = ObjectList
        elif PartSelection == 'Fanslist':
            export_type = 'Linked'
            ObjectList_Treated = ObjectList
        # 间接获取文章对象
        elif PartSelection in ['Likes','Dislikes','Collect']:
            export_type = 'Topic'
            for TopicInfo in ObjectList:
                ThemeList = eval("TopicInfo.%s.TAS_Theme.split('&') if TopicInfo.%s.TAS_Theme != '' else []" % (
                    Query_Params['ForeignKeyField'], Query_Params['ForeignKeyField']))
                ObjectList_Treated.append(
                    (eval("TopicInfo.%s" % Query_Params['ForeignKeyField']), ThemeList))
        elif PartSelection == 'Follow':
            export_type = 'Follow'
            for TopicInfo in ObjectList:
                ObjectList_Treated.append(TopicInfo.STF_SpecialTopic)

        # 内容分页处理
        ObjectPaged = RecordsetPaging(
            ObjectList_Treated, PageNumber, ConfigData['TopicsPageLimit'])
        page_card_display = ObjectPaged.paginator.num_pages
        page_href = '/UserProfile?UserNickName=' + \
            usernickname + '&Select=' + PartSelection + '&PageNumber='
        # 返回渲染
        return render(request, 'Nagetive-UserProfile.html', {'selforguest': status,
                                                             'export_from': status[5],
                                                             'export_type': export_type,
                                                             "SearchSource": 'Topic',
                                                             'export_userinfo': UserObject,
                                                             'export_linkinfo': LinkInfo,
                                                             "exportList_cards": ObjectPaged,
                                                             "page_card_display": page_card_display,
                                                             "export_href": page_href,
                                                             "search_placeholder": ConfigData['HotKeyWord'],
                                                             "NotificationCount": str(NotificationCount)
                                                             })


def indexView(request):

    return HttpResponseRedirect("/Topics?Part=Index&PageNumber=1")

def PageMiss(request):

    return render(request,'Nagetive-PageMiss.html')

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
        Query_Params = aConf.Part_Dict[Part]

        TopicsInfoList = QDBC(TableName=Query_Params['TableName'],
                              QueryMethod='filter', 
                              DefaultCondition = Query_Params['DefaultField'] + "=" + (ConfigData['ReadsThreshold'] if Part in 'IndexOrderDate' else "'" + FilterWord + "'"),
                              #exec("%s=%s" % (Query_Params['DefaultField'], ConfigData['ReadsThreshold'] if Part in 'IndexOrderDate' else "'" + FilterWord + "'")),
                              operations=Query_Params['Operations'],
                              limit=ConfigData['TopicsLimit'] if Part in ['Index', 'IndexOrderDate','Theme', 'Category', 'TopicSearch'] else ConfigData['CommentsLimit'])
        if Part in ['Index', 'IndexOrderDate','Theme', 'Category', 'TopicSearch']:
            TopicsInfoList_Treated = []
            CategorysInfoList = QDBC(TableName='CategoryInfo', QueryMethod='all')
            RecommendAuthorInfoList = QDBC(TableName='RecommendAuthor', QueryMethod='all')
            for TopicInfo in TopicsInfoList:
                ThemeList = TopicInfo.TAS_Theme.split(
                    '&') if TopicInfo.TAS_Theme != '' else []
                TopicsInfoList_Treated.append((TopicInfo, ThemeList))

            TopicsObject = RecordsetPaging(
                TopicsInfoList_Treated, PageNumber, ConfigData['TopicsPageLimit'])
            page_card_display = TopicsObject.paginator.num_pages
            page_href = "/Topics?Part=" + Part + '&FilterWord=' + FilterWord + '&PageNumber='

            return render(request, Query_Params['Template'], {"export_from": 'Index',
                                                                 "SearchSource": 'Topic',
                                                                 "exportList_cards": TopicsObject,
                                                                 "exportList_category": CategorysInfoList,
                                                                 "exportList_author":RecommendAuthorInfoList,
                                                                 #"topic_display": topic_display,
                                                                 "page_card_display": page_card_display,
                                                                 "current_pagenumber": str(PageNumber),
                                                                 "export_href": page_href,
                                                                 "search_placeholder": ConfigData['HotKeyWord'],
                                                                 "NotificationCount": str(NotificationCount)})
        elif Part == 'Content':
            ip = mMs.GetUserIP(request)
            Topic = QDBC(TableName='TopicArticleStatistic',
                         QueryMethod='get',
                         TAS_ID=FilterWord)
            if not QDBC(TableName='ArticleReadsIP',
                        QueryMethod='filter',
                        AR_IP=ip,
                        AR_ArticleID=Topic, 
                        Refresh=True).exists():
                try:
                    QDBC(TableName='ArticleReadsIP',
                         QueryMethod='create',
                         AR_IP=ip, 
                         AR_ArticleID=Topic, 
                         Refresh=True)
                    Topic.TAS_Read += 1
                    Topic.save()
                except Exception as e:
                    return HttpResponse(aConf.UNIQUE_ERROR[str(e)])
            # 收藏状态
            if not QDBC(TableName='UserCollect',QueryMethod='filter',UC_UserNickName=request.user.username, UC_Article=Topic, Refresh=True):
                collectstatus = 'show'
            else:
                collectstatus = 'hide'
            # 评论数据获取
            CommentInfoList = QDBC(TableName='ArticleComment',
                                   QueryMethod='filter',
                                   AC_ArticleID=Topic,
                                   operations=".order_by('-AC_EditDate')",
                                   TimeOut=1)
            CommentInfos = []
            for commentobject in CommentInfoList:
                if commentobject.AC_Parent: 
                    ParentCommentObject = QDBC(TableName='ArticleComment',
                                               QueryMethod='get',
                                               AC_ID=commentobject.AC_Parent,
                                               TimeOut=1)
                    CommentInfos.append(
                        ('HasParent', ParentCommentObject, commentobject))
                else:
                    CommentInfos.append(('HasNoParent', '', commentobject))

            # 评论数据分页
            CommentsObject = RecordsetPaging(
                CommentInfos, PageNumber, ConfigData['CommentsPageLimit'])
            page_card_display = CommentsObject.paginator.num_pages
            page_href = '/Topics?Part=Content&FilterWord=' + FilterWord + '&PageNumber='
            return render(request, Query_Params['Template'], {"TopicsContent": TopicsInfoList[0],
                                                                 "SearchSource": 'Topic',
                                                                 "IsCommentConversation":'False',
                                                                 "export_collectstatus": collectstatus,
                                                                 "exportList_cards": CommentsObject,
                                                                 "page_card_display": page_card_display,
                                                                 "current_pagenumber": str(PageNumber),
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

            Category = QDBC(TableName='CategoryInfo',
                            QueryMethod='get',
                            CI_Name=request.POST.get('CategoryText'))

            ContentText = request.POST.get('ContentRichText')
            ContentPoorText = request.POST.get('ContentPoorText')
            Themes = request.POST.get('Themes')
            try:
                QDBC(TableName='TopicArticleStatistic', 
                     QueryMethod='create', 
                     TAS_Author=request.user, 
                     TAS_Title=Title, 
                     TAS_Type=Category,
                     TAS_Content=ContentText, 
                     TAS_Description=ContentPoorText, 
                     TAS_Theme=Themes, 
                     Refresh=True)

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
        username = mMs.Decrypt(mMs.DecodeWithBase64(request.POST.get('username')))
        userpassword = mMs.Decrypt(mMs.DecodeWithBase64(request.POST.get('password')))
        print(username,userpassword)
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
        username = mMs.Decrypt(mMs.DecodeWithBase64(request.POST.get('username')))
        usernickname = mMs.Decrypt(mMs.DecodeWithBase64(request.POST.get('usernickname')))
        password = mMs.Decrypt(mMs.DecodeWithBase64(request.POST.get('password')))
        email = mMs.Decrypt(mMs.DecodeWithBase64(request.POST.get('email')))
        try:
                #CheckInDate = str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
                # 这里通过前端注册账号一定要是要create_user 不然后期登录的时候  auth.authenticate无法验证用户名和密码
            User.objects.create_user(username, UT_Nick=usernickname, password=password, email=email, UT_Avatar=userimageURL)
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
            UserObject = QDBC(TableName='User',
                           QueryMethod='get',
                           username=request.user.username)
            if From == 'Topic':
                Article = QDBC(TableName='TopicArticleStatistic',
                               QueryMethod='get',
                               TAS_ID=ArticleID)
                CommentObject = QDBC(TableName='ArticleComment',
                                     QueryMethod='create',
                                     AC_Comment=CommentInfo, 
                                     AC_UserNickName=UserObject, 
                                     AC_ArticleID=Article, Refresh=True)
                # 评论数统计
                Article.TAS_Comment += 1
                Article.save()
                AddToNotificationTable(CommentObject.AC_ID,Article.TAS_Title,'Topics','Content','Comment',ArticleID,Article.TAS_Author,request.user)
                UserInfoOperation(request.user.username,'UT_TreplayCount','+=1')
                return HttpResponse('ok')
            elif From == 'SpecialTopic':
                SpecialTopic = QDBC(TableName='SpecialTopicInfo',
                                    QueryMethod='get',
                                    STI_ID=ArticleID)
                CommentObject = QDBC(TableName='SpecialTopicComment',
                                     QueryMethod='create',
                                     STC_Comment=CommentInfo,
                                     STC_UserNickName=UserObject, 
                                     STC_SpecialTopicID=SpecialTopic)
                SpecialTopic.STI_Comment += 1
                SpecialTopic.save()
                AddToNotificationTable(CommentObject.STC_ID,SpecialTopic.STI_Title,'SpecialTopicSquare','SpecialTopicContent','Comment',ArticleID,SpecialTopic.STI_Publisher,request.user)
                UserInfoOperation(request.user.username,'UT_SreplayCount','+=1')
                return HttpResponse('ok')                
        else:
            return HttpResponse('login')


def AddToNotificationTable(anchor,title,url, part, sign, keyid, targetUser,sourceUser):
    try:
        QDBC(TableName='NotificationTable',
             QueryMethod='create',
             NT_AnchorID=anchor,
             NT_Title=title,
             NT_KeyID=keyid,
             NT_Part=part,
             NT_Sign=sign,
             NT_URL=url,
             NT_TargetUser=targetUser,
             NT_SourceUser=sourceUser,
             Refresh=True)
    except Exception as e:
        raise e

def GetNotificationInfo(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            try:
                NotificationObjects = QDBC(TableName='NotificationTable',
                                           QueryMethod='filter',
                                           NT_TargetUser=request.user,
                                           Refresh=True)
                if NotificationObjects:
                    dataList = []
                    for Object in NotificationObjects:
                        dataDict = {}
                        dataDict['NT_ID'] = str(Object.NT_ID)
                        dataDict['NT_KeyID'] = Object.NT_KeyID
                        dataDict['NT_AnchorID'] = Object.NT_AnchorID
                        dataDict['NT_URL'] = Object.NT_URL
                        dataDict['NT_Title'] = Object.NT_Title
                        dataDict['NT_Part'] = Object.NT_Part
                        dataDict['NT_PageNumber'] = GetNotificationInfoPageNum(dataDict['NT_Part'],dataDict['NT_KeyID'],dataDict['NT_AnchorID'])
                        dataDict['NT_Sign'] = Object.NT_Sign
                        dataDict['NT_SourceUser'] = Object.NT_SourceUser.UT_Nick
                        dataList.append(dataDict)
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
        if request.POST.get('NT_ID'):
            NT_ID_Datas = request.POST.get('NT_ID').split(',')
            
            if request.user.is_authenticated:
                if len(NT_ID_Datas) == 1:
                    try:
                        QDBC(TableName='NotificationTable',
                             QueryMethod='get',
                             NT_ID=NT_ID_Datas[0]).delete()
                        return HttpResponse('OneDeleteOk')
                    except Exception as e:
                        raise e
                else:
                    for NT_ID_Data in NT_ID_Datas:
                        try:
                            QDBC(TableName='NotificationTable', 
                                 QueryMethod='get', 
                                 NT_ID=NT_ID_Data).delete()
                        except Exception as e:
                            raise e
                    return HttpResponse('AllDeleteOk')  
        else:
            return HttpResponse('DeleteFail')               
        

def GetNotificationCount(requestObject):
    if requestObject.user.is_authenticated:
        try:
            return QDBC(TableName='NotificationTable', 
                        QueryMethod='filter', 
                        NT_TargetUser=requestObject.user, 
                        operations='.count()',
                        isLimit=False,
                        Refresh=True)
        except Exception as e:
            raise e
    else:
        return 0

def GetNotificationInfoPageNum(part,keyid,anchorid):
    ConfigData = mMs.GetConfig()
    if part == 'Content':
        ACObjects = list(QDBC(TableName='ArticleComment', 
                              QueryMethod='filter', 
                              operations=".order_by('-AC_EditDate')", 
                              AC_ArticleID=QDBC(TableName='TopicArticleStatistic', 
                                                QueryMethod='get', 
                                                TAS_ID=keyid)))
        Number = 0
        for ACObject in ACObjects:
            Number += 1
            if str(ACObject.AC_ID) == anchorid:
                break
        PageNumber = Number // ConfigData['CommentsPageLimit'] if Number%ConfigData['CommentsPageLimit'] == 0 else Number // ConfigData['CommentsPageLimit'] + 1
        return str(PageNumber)
    elif part == 'SpecialTopicContent':
        STCommentObjects = list(QDBC(TableName='SpecialTopicComment',
                                     QueryMethod='filter',
                                     STC_SpecialTopicID=QDBC(TableName='SpecialTopicInfo',
                                                             QueryMethod='get',
                                                             STI_ID=keyid),
                                     operations=".order_by('-STC_EditDate')"))
        Number = 0
        for STCommentObject in STCommentObjects:
            Number += 1
            if str(STCommentObject.STC_ID) == anchorid:
                break
        PageNumber = Number // ConfigData['SpecialTopicsPageLimit'] if Number%ConfigData['SpecialTopicsPageLimit'] == 0 else Number // ConfigData['SpecialTopicsPageLimit'] + 1
        return str(PageNumber)
    else:
        return '1'


def BlackListOperation(request):
    if request.method == 'POST':
        UserNcik = request.POST.get('UserNick')
        Operation = request.POST.get('Operation')
        UserNcikObject = QDBC(TableName='User',
                              QueryMethod='get',
                              UT_Nick=UserNcik)
        if request.user.is_authenticated and Operation == 'add':
            if not QDBC(TableName='BlackList',
                        QueryMethod='filter',
                        BL_User=UserNcikObject,
                        BL_Handler=request.user, 
                        Refresh=True):
                try:
                    QDBC(TableName='BlackList',
                         QueryMethod='create',
                         BL_User=UserNcikObject,
                         BL_Handler=request.user,
                         Refresh=True)
                    QDBC(TableName='UserLink',
                         QueryMethod='get',
                         UL_UserBeLinked=request.user,
                         UL_UserLinking=UserNcikObject,
                         Refresh=True)
                    if UserLinkObject:

                        UserLinkObject.delete()
                        return HttpResponse('已拉黑')
                except Exception as e:
                    return HttpResponse(e)
            else:
                return HttpResponse('addfail')
        elif request.user.is_authenticated and Operation == 'delete':
            BlackObject = QDBC(TableName='BlackList',
                               QueryMethod='filter',
                               BL_User=UserNcikObject,
                               BL_Handler=request.user)
            if BlackObject:
                try:
                    BlackObject = QDBC(TableName='BlackList',
                                       QueryMethod='filter',
                                       BL_User=UserNcikObject,
                                       BL_Handler=request.user).delete()
                    return HttpResponse('已取消拉黑')
                except Exception as e:
                    return HttpResponse(e)
            else:
                return HttpResponse('blockcancelfail')            
        else:
            return HttpResponse('login')


def GetTemplate(templateName):

    # 读取card模板html信息
    return Template(mMs.GetStringFromHtml(aConf.temlatesDIR, templateName))


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

    return len(QDBC(TableName='UserTable',
                    QueryMethod='filter',
                    UT_Name=username))

def StatisticalDataUpdata(objectStr,methodDsc):
    exec(objectStr + methodDsc)
    exec(objectStr + '.save()')


def GetParam(request):
    if request.method == "POST":
        KeyWord = request.POST.get('KeyWord')
        if KeyWord == 'SecretKey':
            Params = mMs.GetConfig()
            jsondata = json.dumps([Params['SecretKey'],Params['SecretVI']],ensure_ascii=False)
            return HttpResponse(jsondata)
        else:
            pass