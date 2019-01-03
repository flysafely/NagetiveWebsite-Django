from django.db import models

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.processors import SmartResize

from ckeditor_uploader.fields import RichTextUploadingField
from ..User import *

import uuid

class SpecialTopicInfo(models.Model):
    """docstring for SpecialTopicInfo"""
    STI_ID = models.UUIDField(
        primary_key=True, auto_created=True, default=uuid.uuid4, verbose_name='专题ID')
    STI_Title = models.CharField(
        max_length=35, unique=True, verbose_name='专题标题')
    STI_Cover = models.ImageField(
        upload_to='Cover', blank=False, verbose_name='封面图', default='')
    STI_Cover_210x140 = ImageSpecField(source='STI_Cover', processors=[
                                       SmartResize(210, 140)], format='JPEG', options={'quality': 95})
    STI_Cover_SR965x300 = ImageSpecField(source='STI_Cover', processors=[
                                         SmartResize(965, 300)], format='JPEG', options={'quality': 95})
    STI_EditDate = models.DateField(auto_now=True, verbose_name='发布时间')
    STI_Publisher = models.ForeignKey(
        User, to_field='username', related_name='Publisher', on_delete=models.CASCADE, verbose_name='发布者')
    STI_Type = models.CharField(
        max_length=10, default='article', verbose_name='专题类型')
    STI_Follower = models.IntegerField(
        default=0, blank=False, verbose_name='关注量')
    STI_Hot = models.IntegerField(default=10, blank=False, verbose_name='热度')
    STI_Abstract = models.CharField(
        max_length=30, blank=False, default='', verbose_name='简介')
    STI_Content = RichTextUploadingField(
        null=True, blank=True, config_name='admin', verbose_name='正文')
    STI_Comment = models.IntegerField(verbose_name='评论数', default=0)

    class Meta:
        verbose_name = '专题'
        # 末尾不加s
        verbose_name_plural = '**3**专题信息**3**'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.STI_Title


class SpecialTopicFollow(models.Model):
    STF_UserNickName = models.ForeignKey(
        User, to_field='username', default='flysafely', on_delete=models.CASCADE, verbose_name='用户名')
    STF_SpecialTopic = models.ForeignKey(
        SpecialTopicInfo, to_field='STI_ID', on_delete=models.CASCADE, verbose_name='专题ID')
    STF_CollectTime = models.DateField(auto_now=True, verbose_name='时间')

    class Meta:
        verbose_name = '关注'
        verbose_name_plural = '**3**专题关注**3**'
        app_label = 'NTWebsite'


class SpecialTopicReadsIP(models.Model):
    """docstring for SpecialTopicReadsIP"""
    STR_IP = models.CharField(max_length=100, null=True,
                              blank=True, verbose_name='IP')
    STR_EditDate = models.DateField(auto_now=True, verbose_name='时间')
    # AR_ArticleID = models.CharField(max_length=100, null=True,
    #                                blank=True, verbose_name='文章ID')
    STR_SpecialTopicID = models.ForeignKey(
        SpecialTopicInfo, to_field='STI_ID', on_delete=models.CASCADE, verbose_name='专题ID')

    class Meta:
        verbose_name = 'IP记录'
        # 末尾不加s
        verbose_name_plural = '**3**专题阅读IP统计**3**'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.STR_IP

# 专题评论表


class SpecialTopicComment(models.Model):
    """docstring for ArticleComment"""
    Readstatus = (("Y", "已阅"), ("N", "未读"))

    STC_ID = models.UUIDField(
        primary_key=True, editable=False, auto_created=True, default=uuid.uuid4, verbose_name='专题评论ID')
    STC_SpecialTopicID = models.ForeignKey(
        SpecialTopicInfo, to_field='STI_ID', on_delete=models.CASCADE, verbose_name='专题ID')
    STC_Comment = models.TextField(verbose_name="评论内容")
    STC_Parent = models.CharField(
        max_length=100, editable=True, default='', verbose_name='父评论ID')
    #STC_Like = models.IntegerField(verbose_name='赞', default="0")
    #STC_Dislike = models.IntegerField(verbose_name='怼', default="0")
    STC_EditDate = models.DateTimeField(auto_now=True, verbose_name='编辑时间')
    STC_UserNickName = models.ForeignKey(
        User, to_field='username', default='flysafely', on_delete=models.CASCADE, verbose_name='用户名')
    STC_Readstatus = models.CharField(
        max_length=1, default="N", choices=Readstatus, verbose_name='是否阅读')

    class Meta:
        verbose_name = '评论'
        # 末尾不加s
        verbose_name_plural = '**3**专题评论**3**'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.STC_Comment