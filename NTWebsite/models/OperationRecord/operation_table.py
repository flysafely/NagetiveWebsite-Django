from django.db import models
from ..User import *
from ..Topic import *
from ..SpecialTopic import *
from ..RollCall import *

import uuid

# 文章立场统计


class ArticleUserLikesOrDislikesTable(models.Model):
    """docstring for ArticleLikseIP"""
    ALD_UserNickName = models.ForeignKey(
        User, to_field='username', default='flysafely', on_delete=models.CASCADE, verbose_name='用户名')
    ALD_StandPoint = models.IntegerField(blank=False, verbose_name='立场代码')
    # ALD_ArticleID = models.CharField(max_length=100, null=True,
    #                                 blank=True, verbose_name='文章ID')
    ALD_EditDate = models.DateField(auto_now=True, verbose_name='时间')
    ALD_ArticleID = models.ForeignKey(
        TopicArticleStatistic, to_field='TAS_Title', on_delete=models.CASCADE, verbose_name='文章ID')

    class Meta:
        verbose_name = '立场记录'
        # 末尾不加s
        verbose_name_plural = '**1**文章立场统计**1**'
        app_label = 'NTWebsite'

# 评论立场统计


class CommentUserLikesOrDislikesTable(models.Model):
    """docstring for ArticleLikseIP"""
    CLD_UserNickName = models.ForeignKey(
        User, to_field='username', default='flysafely', on_delete=models.CASCADE, verbose_name='用户名')
    CLD_StandPoint = models.IntegerField(blank=False, verbose_name='立场代码')
    # ALD_ArticleID = models.CharField(max_length=100, null=True,
    #                                 blank=True, verbose_name='文章ID')
    CLD_EditDate = models.DateField(auto_now=True, verbose_name='时间')
    CLD_CommentID = models.ForeignKey(
        ArticleComment, to_field='AC_ID', on_delete=models.CASCADE, verbose_name='评论ID')

    class Meta:
        verbose_name = '评论立场记录'
        # 末尾不加s
        verbose_name_plural = '**1**评论立场统计**1**'
        app_label = 'NTWebsite'

# 阅读IP统计


class ArticleReadsIP(models.Model):
    """docstring for ArticleLikseIP"""
    AR_IP = models.CharField(max_length=100, null=True,
                             blank=True, verbose_name='IP')
    AR_EditDate = models.DateField(auto_now=True, verbose_name='时间')
    # AR_ArticleID = models.CharField(max_length=100, null=True,
    #                                blank=True, verbose_name='文章ID')
    AR_ArticleID = models.ForeignKey(
        TopicArticleStatistic, to_field='TAS_Title', on_delete=models.CASCADE, verbose_name='文章ID')

    class Meta:
        verbose_name = '阅读IP记录'
        # 末尾不加s
        verbose_name_plural = '**1**文章阅读IP统计**1**'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.AR_IP

# 用户关注


class UserLink(models.Model):
    """docstring for UserLink"""
    UL_UserBeLinked = models.ForeignKey(
        User, to_field='username', null=False, blank=False, on_delete=models.CASCADE, verbose_name='被关注用户')
    UL_UserLinking = models.ForeignKey(
        User, to_field='username', related_name='UserNameLinking', null=False, blank=False, on_delete=models.CASCADE, verbose_name='关注用户')
    UL_LinkTime = models.DateField(auto_now=True, verbose_name='时间')

    class Meta:
        verbose_name = '关注信息'
        verbose_name_plural = '**4**用户关注信息**4**'
        app_label = 'NTWebsite'


class UserCollect(models.Model):
    """docstring for UserCollect"""
    UC_UserNickName = models.ForeignKey(
        User, to_field='username', default='flysafely', on_delete=models.CASCADE, verbose_name='用户名')
    UC_Article = models.ForeignKey(
        TopicArticleStatistic, to_field='TAS_ID', on_delete=models.CASCADE, verbose_name='文章ID')
    UC_CollectTime = models.DateField(auto_now=True, verbose_name='时间')

    class Meta:
        verbose_name = '文章收藏'
        verbose_name_plural = '**1**文章用户收藏**1**'
        app_label = 'NTWebsite'



class RecommendAuthor(models.Model):
    RA_Author = models.ForeignKey(
        User, to_field='username', default='flysafely', on_delete=models.CASCADE, verbose_name='用户名')
    RA_Rank = models.IntegerField(
        default=0, blank=False, verbose_name='顺序')

    class Meta:
        verbose_name = '用户'
        # 末尾不加s
        verbose_name_plural = '**1**推荐用户**1**'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.RA_Author.UT_Nick


class NotificationTable(models.Model):

    NT_ID = models.UUIDField(
        primary_key=True, auto_created=True, default=uuid.uuid4, verbose_name='通知ID')
    NT_KeyID = models.CharField(
        max_length=100, blank=False, default='', verbose_name='关键ID')
    NT_AnchorID = models.CharField(
        max_length=100, blank=False, default='', verbose_name='定位ID')
    NT_Title = models.CharField(
        max_length=100, blank=False, default='', verbose_name='标题')
    NT_URL = models.CharField(max_length=30, blank=False, verbose_name='URL')
    NT_Part = models.CharField(
        max_length=30, blank=False, default='', verbose_name='板块')
    NT_Sign = models.CharField(
        max_length=30, blank=False, default='', verbose_name='标记')
    NT_SourceUser = models.ForeignKey(
        User, to_field='username', related_name='SourceUser', on_delete=models.CASCADE, verbose_name='通知者', default='')
    NT_TargetUser = models.ForeignKey(
        User, to_field='username', related_name='TargetUser', on_delete=models.CASCADE, verbose_name='被通知者')

    class Meta:
        verbose_name = '信息'
        # 末尾不加s
        verbose_name_plural = '**4**通知信息**4**'
        app_label = 'NTWebsite'

    def __str__(self):
        return str(self.NT_ID)


class BlackList(models.Model):
    """docstring for blacklist"""

    BL_ID = models.UUIDField(
        primary_key=True, auto_created=True, default=uuid.uuid4, verbose_name='黑名单ID')
    BL_User = models.ForeignKey(
        User, to_field='username', related_name='BL_User', on_delete=models.CASCADE, verbose_name='被添加用户')
    BL_Handler = models.ForeignKey(
        User, to_field='username', related_name='BL_Handler', on_delete=models.CASCADE, verbose_name='操作用户')

    class Meta:
        verbose_name = '记录'
        # 末尾不加s
        verbose_name_plural = '**6**黑名单**6**'
        app_label = 'NTWebsite'

    def __str__(self):
        return str(self.BL_User.UT_Nick)