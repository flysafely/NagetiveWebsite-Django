from django.contrib import admin
from NTWebsite.models import \
TopicArticleTheme,\
ArticleTags,\
ConfigParams,\
PreferredConfigName,\
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
# Register your models here.
@admin.register(RecommendAuthor)
class RecommendAuthorAdminView(admin.ModelAdmin):
    list_display = ('RA_Author','RA_Rank',)

@admin.register(SpecialTopicComment)
class SpecialTopicCommentAdminView(admin.ModelAdmin):
    list_display = ('STC_ID','STC_Comment',)

@admin.register(SpecialTopicReadsIP)
class SpecialTopicReadsIPAdminView(admin.ModelAdmin):
    list_display = ('STR_IP','STR_SpecialTopicID',)

@admin.register(SpecialTopicFollow)
class SpecialTopicFollowtAdminView(admin.ModelAdmin):
    list_display = ('STF_SpecialTopic','STF_UserNickName',)

    

@admin.register(SpecialTopicInfo)
class SpecialTopicInfoAdminView(admin.ModelAdmin):
    list_display = ('STI_Title','STI_Publisher',)

@admin.register(RollCallDialogue)
class RollCallDialogueAdminView(admin.ModelAdmin):
    list_display = ('RCD_ID','RCD_EditDate',)

@admin.register(NotificationTable)
class NotificationTableAdminView(admin.ModelAdmin):
    list_display = ('NT_Plate','NT_TargetUser',)

@admin.register(RollCallInfo)
class RollCallInfoAdminView(admin.ModelAdmin):
    """docstring for RollCallInfo"""
    list_display = ('RCI_Title','RCI_Publisher','RCI_Target',)



@admin.register(PreferredConfigName)
class PreferredConfigNameAdminView(admin.ModelAdmin):
    """docstring for PreferredConfigName"""
    list_display = ('PC_Name',)
        

@admin.register(ConfigParams)
class ConfigParamsAdminView(admin.ModelAdmin):
    """docstring for ConfigParams"""
    list_display = ('CP_Name',)


@admin.register(TopicArticleStatistic)
class TopicArticleStatisticAdminView(admin.ModelAdmin):
    """docstring for TopicArticleStatistic"""
    list_display = ('TAS_Title', 'TAS_Author', 'TAS_ID',)


@admin.register(User)
class UserAdminView(admin.ModelAdmin):
    """docstring for UserTable"""
    list_display = ('username', 'date_joined',)


@admin.register(ArticleUserLikesOrDislikesTable)
class ArticleUserLikesOrDislikesTableAdminView(admin.ModelAdmin):
    """docstring for ArticleUserLikesOrDislikesTable"""
    list_display = ('ALD_UserNickName', 'ALD_StandPoint')

@admin.register(CommentUserLikesOrDislikesTable)
class CommentUserLikesOrDislikesTableAdminView(admin.ModelAdmin):
    list_display = ('CLD_UserNickName','CLD_StandPoint')


@admin.register(ArticleReadsIP)
class ArticleReadsIPAdminView(admin.ModelAdmin):
    """docstring for CategoryInfo"""
    list_display = ('AR_IP',)

@admin.register(RollCallReadsIP)
class RollCallReadsIPAdminView(admin.ModelAdmin):
    """docstring for CategoryInfo"""
    list_display = ('RCR_IP',)

@admin.register(CategoryInfo)
class CategoryInfoAdminView(admin.ModelAdmin):
    """docstring for CategoryInfo"""
    list_display = ('CI_Name',)


@admin.register(ArticleTags)
class ArticleTagsAdminView(admin.ModelAdmin):
    """docstring for ArticleTags"""
    list_display = ('AT_ID', 'AT_Name',)


@admin.register(ArticleComment)
class ArticleCommentAdminView(admin.ModelAdmin):
    """docstring for ArticleComment"""
    list_display = ('AC_Comment','AC_UserNickName','AC_EditDate')


@admin.register(TopicArticleTheme)
class TopicArticleThemeAdminView(admin.ModelAdmin):
    """docstring for ArticleComment"""
    list_display = ('TAT_ID', 'TAT_Name',)

@admin.register(UserLink)
class UserLinkAdminView(admin.ModelAdmin):
    """docstring for ArticleComment"""
    list_display = ('UL_UserBeLinked','UL_UserLinking', 'UL_LinkTime')

@admin.register(UserCollect)
class UserCollectAdminView(admin.ModelAdmin):
    """docstring for UserCollect"""
    list_display = ('UC_UserNickName','UC_Article','UC_CollectTime')

@admin.register(UserCircuseeCollect)
class UserCircuseeCollectAdminView(admin.ModelAdmin):
    """docstring for UserCircuseeCollect"""
    list_display = ('UCC_UserNickName','UCC_RollCall','UCC_CollectTime')