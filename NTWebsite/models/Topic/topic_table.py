from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from ..User import *
import uuid

class TopicArticleTheme(models.Model):
    """docstring for TopicArticleTheme"""
    TAT_ID = models.CharField(
        primary_key=True, max_length=10, default='0', verbose_name='主题代码')
    TAT_Name = models.CharField(
        max_length=10, unique=True, verbose_name='主题名称')

    class Meta:
        verbose_name = '文章'
        # 末尾不加s
        verbose_name_plural = '**1**文章主题**1**'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.TAT_Name

# 品类信息表


class CategoryInfo(models.Model):
    CI_Name = models.CharField(primary_key=True,
                               max_length=10, null=False, blank=False, verbose_name='品类名称')
    CI_SVG = models.TextField(max_length=1000, verbose_name='图标SVG')

    class Meta:
        verbose_name = '类目'
        # 末尾不加s
        verbose_name_plural = '**1**来自类目**1**'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.CI_Name


# 文章信息表.


class TopicArticleStatistic(models.Model):
    """docstring for ClassName"""

    TAS_ID = models.UUIDField(
        primary_key=True, auto_created=True, default=uuid.uuid4, verbose_name='文章ID')
    TAS_Title = models.CharField(
        max_length=35, unique=True, verbose_name='文章标题')
    TAS_Description = models.TextField(max_length=140, verbose_name='文章描述')
    TAS_EditDate = models.DateField(auto_now=True, verbose_name='编辑时间')
    TAS_Author = models.ForeignKey(
        User, to_field='username', default='flysafely', on_delete=models.CASCADE, verbose_name='用户名')
    TAS_Theme = models.CharField(
        max_length=100, default="其他", verbose_name='文章主题')
    TAS_Type = models.ForeignKey(
        CategoryInfo, to_field='CI_Name', on_delete=models.CASCADE, verbose_name='文章类别')
    TAS_Like = models.IntegerField(verbose_name='赞', default=0)
    TAS_Dislike = models.IntegerField(verbose_name='怼', default=0)
    TAS_Read = models.IntegerField(verbose_name='阅读量', default=10)
    TAS_Comment = models.IntegerField(verbose_name='评论数', default=0)
    TAS_Content = RichTextUploadingField(
        null=True, blank=True, config_name='admin', verbose_name='文章正文')

    class Meta:
        verbose_name = '文章信息'
        # 末尾不加s
        verbose_name_plural = '**1**文章基础信息**1**'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.TAS_Title


# 文章标签表


class ArticleTags(models.Model):
    AT_TAID = models.UUIDField(
        default=uuid.uuid4, null=False, editable=False, verbose_name='文章ID')
    AT_ID = models.IntegerField(verbose_name='标签代码')
    AT_Name = models.CharField(max_length=10, verbose_name='标签名称')

    class Meta:
        verbose_name = '标签'
        # 末尾不加s
        verbose_name_plural = '**1**文章标签**1**'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.AT_Name

# 文章评论表


class ArticleComment(models.Model):
    """docstring for ArticleComment"""
    Readstatus = (("Y", "已阅"), ("N", "未读"))

    AC_ID = models.UUIDField(
        primary_key=True, editable=False, auto_created=True, default=uuid.uuid4, verbose_name='评论ID')
    AC_ArticleID = models.ForeignKey(
        TopicArticleStatistic, to_field='TAS_Title', on_delete=models.CASCADE, verbose_name='文章ID')
    # AC_ArticleID = models.UUIDField(
    #    null=False, editable=True, verbose_name='文章ID')
    AC_Comment = models.TextField(verbose_name="评论内容")
    AC_Parent = models.CharField(
        max_length=100, editable=True, default='', verbose_name='父评论ID')
    AC_Like = models.IntegerField(verbose_name='赞', default="0")
    AC_Dislike = models.IntegerField(verbose_name='怼', default="0")
    AC_EditDate = models.DateTimeField(auto_now=True, verbose_name='编辑时间')
    AC_UserNickName = models.ForeignKey(
        User, to_field='username', default='flysafely', on_delete=models.CASCADE, verbose_name='用户名')
    AC_Readstatus = models.CharField(
        max_length=1, default="N", choices=Readstatus, verbose_name='是否阅读')

    class Meta:
        verbose_name = '评论'
        # 末尾不加s
        verbose_name_plural = '**1**文章评论**1**'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.AC_Comment