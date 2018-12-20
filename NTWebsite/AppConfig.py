import os
#import sys
#from NTWebsite import MainMethods as mMs
#import MainMethods as mMs
#sys.path.append('C:\\Users\\flysafely\\Documents\\百度云同步盘\\14.程序相关\\12.Website\\nagetiveSite\\NTWebsite\\MainMethods.py')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

temlatesDIR = os.path.join(BASE_DIR, 'NTWebsite\\templates')

Topic_Card_Item = "TopicCardItem.html"

Category_Card_Item = "CategoryCard.html"

Index_html = "Nagetive-IndexBase.html"

IndexCardLimit = 100

CommentCardLimit = 100

IndexTopicRead = '10'

Section_Map_Field = {"Theme": {"TableName": "TopicArticleStatistic",
                               "JudgementCondition": "TAS_Theme__contains=",
                               "Operations": ".order_by('TAS_Read')",
                               "Template": Index_html,
                               "Limit": IndexCardLimit, },
                     "Category": {"TableName": "TopicArticleStatistic",
                                  "JudgementCondition": "TAS_Type=",
                                  "Operations": ".order_by('TAS_Read')",
                                  "Template": Index_html,
                                  "Limit": IndexCardLimit, },
                     "Index": {"TableName": "TopicArticleStatistic",
                               "JudgementCondition": "TAS_Read__gte=",
                               "Operations": ".order_by('TAS_Read')",
                               "Template": Index_html,
                               "Limit": IndexCardLimit, },
                     "Content": {"TableName": "TopicArticleStatistic",
                                 "JudgementCondition": "TAS_ID=",
                                 "Operations": ".order_by('TAS_ID')",
                                 "Template": "Nagetive-TopicContentBase.html",
                                 "Limit": CommentCardLimit, },
                     "TopicSearch": {"TableName": "TopicArticleStatistic",
                                    "JudgementCondition": "TAS_Title__contains=",
                                    "Operations": ".order_by('TAS_Read')",
                                    "Template": Index_html,
                                    "Limit": IndexCardLimit, },
                     # UserProfile
                     "Publish": {"TableName": "TopicArticleStatistic",
                                 "JudgementCondition": "TAS_Author=",
                                 "Operations": ".order_by('TAS_Read')",
                                 "ForeignKeyField": '',
                                 "ExtraCondition": '',
                                 "Template": 'Nagetive-UserProfile.html'},
                     "Likes": {"TableName": "ArticleUserLikesOrDislikesTable",
                               "JudgementCondition": "ALD_UserNickName=",
                               "Operations": ".order_by('ALD_EditDate')",
                               "ForeignKeyField": 'ALD_ArticleID',
                               "ExtraCondition": "ALD_StandPoint=1",
                               "Template": 'Nagetive-UserProfile.html'},
                     "Dislikes": {"TableName": "ArticleUserLikesOrDislikesTable",
                                  "JudgementCondition": "ALD_UserNickName=",
                                  "Operations": ".order_by('ALD_EditDate')",
                                  "ForeignKeyField": 'ALD_ArticleID',
                                  "ExtraCondition": "ALD_StandPoint=2",
                                  "Template": 'Nagetive-UserProfile.html'},
                     "Circusee": {"TableName": "UserCircuseeCollect",
                                  "JudgementCondition": "UCC_UserNickName=",
                                  "Operations": ".order_by('-UCC_CollectTime')",
                                  "ForeignKeyField": '',
                                  "ExtraCondition": '',
                                  "Template": 'Nagetive-UserProfile.html'},
                     "Collect": {"TableName": "UserCollect",
                                 "JudgementCondition": "UC_UserNickName=",
                                 "Operations": ".order_by('-UC_CollectTime')",
                                 "ForeignKeyField": 'UC_Article',
                                 "ExtraCondition": '',
                                 "Template": 'Nagetive-UserProfile.html'},
                     "Comment": {"TableName": "ArticleComment",
                                 "JudgementCondition": "AC_UserNickName=",
                                 "Operations": ".order_by('-AC_EditDate')",
                                 "ForeignKeyField": 'AC_ArticleID',
                                 "ExtraCondition": '',
                                 "Template": 'Nagetive-UserProfile.html'},
                     "Follow": {"TableName": "SpecialTopicFollow",
                                 "JudgementCondition": "STF_UserNickName=",
                                 "Operations": ".order_by('-STF_CollectTime')",
                                 "ForeignKeyField": 'STF_SpecialTopic',
                                 "ExtraCondition": '',
                                 "Template": 'Nagetive-UserProfile.html'},


                     "RollCallIndex": {"TableName": "RollCallInfo",
                                       "JudgementCondition": "RCI_Read__gte=",
                                       "Operations": ".order_by('-RCI_EditDate')",
                                       "ForeignKeyField": '',
                                       "ExtraCondition": '',
                                       "Template": 'Nagetive-RollCallSquare.html'},
                     "RollCallContent": {"TableName": "RollCallDialogue",
                                         "JudgementCondition": "RCD_ID=",
                                         "Operations": ".order_by('RCD_EditDate')",
                                         "ForeignKeyField": '',
                                         "ExtraCondition": '',
                                         "Template": 'Nagetive-RollCallContentBase.html'},

                     "RollCallSearch": {"TableName": "RollCallInfo",
                                       "JudgementCondition": "RCI_Title__contains=",
                                       "Operations": ".order_by('-RCI_EditDate')",
                                       "ForeignKeyField": '',
                                       "ExtraCondition": '',
                                       "Template": 'Nagetive-RollCallSquare.html'},
                     "SpecialTopicHot":{"TableName": "SpecialTopicInfo",
                                       "JudgementCondition": "STI_Hot__gte=",
                                       "Operations": ".order_by('-STI_Hot')",
                                       "ForeignKeyField": '',
                                       "ExtraCondition": '',
                                       "Template": 'Nagetive-SpecialTopicSquare.html'},
                     "SpecialTopicDate":{"TableName": "SpecialTopicInfo",
                                       "JudgementCondition": "STI_Hot__gte=",
                                       "Operations": ".order_by('-STI_EditDate')",
                                       "ForeignKeyField": '',
                                       "ExtraCondition": '',
                                       "Template": 'Nagetive-SpecialTopicSquare.html'},
                     "SpecialTopicContent":{"TableName": "SpecialTopicInfo",
                                       "JudgementCondition": "STI_ID=",
                                       "Operations": "",
                                       "ForeignKeyField": '',
                                       "ExtraCondition": '',
                                       "Template": 'Nagetive-SpecialContentBase.html'},
                     "SpecialTopicSearch":{"TableName": "SpecialTopicInfo",
                                       "JudgementCondition": "STI_Title__contains=",
                                       "Operations": "",
                                       "ForeignKeyField": '',
                                       "ExtraCondition": '',
                                       "Template": 'Nagetive-SpecialTopicSquare.html'},   
                     "Focuslist":{"TableName": "UserLink",
                                       "JudgementCondition": "UL_UserLinking=",
                                       "Operations": "",
                                       "ForeignKeyField": '',
                                       "ExtraCondition": '',
                                       "Template": 'Nagetive-UserProfile.html'}, 
                     "Fanslist":{"TableName": "UserLink",
                                       "JudgementCondition": "UL_UserBeLinked=",
                                       "Operations": "",
                                       "ForeignKeyField": '',
                                       "ExtraCondition": '',
                                       "Template": 'Nagetive-UserProfile.html'},                                                           
                     }


StantPointStatusNumber = {'Like': 1, 'LikeCancel': -
                          1, 'Dislike': 2, 'DislikeCancel': -2}

UNIQUE_ERROR = {'UNIQUE constraint failed: NTWebsite_user.UT_Nick': '昵称已经存在!',
                'UNIQUE constraint failed: NTWebsite_user.username': '用户名已经存在!',
                'UNIQUE constraint failed: NTWebsite_topicarticlestatistic.TAS_Title': '文章标题已经存在!'}

Taste_KeyString = {'Article': {'TabelName': 'TopicArticleStatistic',
                               'ForeignKey_ID_Field': 'TAS_ID',
                               'UserNickName_Field': 'ALD_UserNickName',
                               'ID_Field': 'ALD_ArticleID',
                               'StandPoint_Field': 'ALD_StandPoint',
                               'Like_Field': 'TAS_Like',
                               'Dislike_Field': 'TAS_Dislike',
                               'TasteTableName': 'ArticleUserLikesOrDislikesTable'
                               },
                   'Comment': {'TabelName': 'ArticleComment',
                               'ForeignKey_ID_Field': 'AC_ID',
                               'UserNickName_Field': 'CLD_UserNickName',
                               'ID_Field': 'CLD_CommentID',
                               'StandPoint_Field': 'CLD_StandPoint',
                               'Like_Field': 'AC_Like',
                               'Dislike_Field': 'AC_Dislike',
                               'TasteTableName': 'CommentUserLikesOrDislikesTable',
                               }
                   }