from django.db import models
from ..User import *
import uuid

class RollCallInfo(models.Model):
    """docstring for RollCallInfo"""
    RCI_ID = models.UUIDField(
        primary_key=True, auto_created=True, default=uuid.uuid4, verbose_name='点名ID')
    RCI_Title = models.CharField(
        max_length=35, unique=True, verbose_name='点名标题')
    RCI_EditDate = models.DateField(auto_now=True, verbose_name='编辑时间')
    RCI_Publisher = models.ForeignKey(
        User, to_field='username', related_name='Publisher_User', on_delete=models.CASCADE, verbose_name='点名者')
    RCI_Target = models.ForeignKey(
        User, to_field='username', related_name='Target_User', on_delete=models.CASCADE, verbose_name='被点名者')
    RCI_LeftLike = models.IntegerField(
        default=0, blank=False, verbose_name='点名者支持数')
    RCI_RightLike = models.IntegerField(
        default=0, blank=False, verbose_name='被点名者支持数')
    RCI_Read = models.IntegerField(
        default=0, blank=False, verbose_name='点名阅读量')

    class Meta:
        verbose_name = '点名信息'
        # 末尾不加s
        verbose_name_plural = '**2**点名基础信息**2**'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.RCI_Title


class RollCallDialogue(models.Model):
    RCD_ID = models.ForeignKey(
        RollCallInfo, to_field='RCI_ID', on_delete=models.CASCADE, verbose_name='点名信息')
    RCD_EditDate = models.DateField(auto_now=True, verbose_name='编辑时间')
    RCD_Query = models.CharField(
        max_length=30, default='', blank=False, verbose_name='询问内容')
    RCD_Reply = models.CharField(
        max_length=30, default='', blank=False, verbose_name='回复内容')

    class Meta:
        verbose_name = '对话记录'
        # 末尾不加s
        verbose_name_plural = '**2**点名对话明细**2**'
        app_label = 'NTWebsite'

    def __str__(self):
        return str(self.RCD_ID.RCI_ID)


class RollCallReadsIP(models.Model):
    """docstring for RollCallReadsIP"""
    RCR_IP = models.CharField(max_length=100, null=True,
                              blank=True, verbose_name='IP')
    RCR_EditDate = models.DateField(auto_now=True, verbose_name='时间')
    # AR_ArticleID = models.CharField(max_length=100, null=True,
    #                                blank=True, verbose_name='文章ID')
    RCR_ArticleID = models.ForeignKey(
        RollCallInfo, to_field='RCI_Title', on_delete=models.CASCADE, verbose_name='围观ID')

    class Meta:
        verbose_name = 'IP记录'
        # 末尾不加s
        verbose_name_plural = '**2**围观IP统计**2**'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.RCR_IP


class UserCircuseeCollect(models.Model):
    UCC_UserNickName = models.ForeignKey(
        User, to_field='username', default='flysafely', on_delete=models.CASCADE, verbose_name='用户名')
    UCC_RollCall = models.ForeignKey(
        RollCallInfo, to_field='RCI_ID', on_delete=models.CASCADE, verbose_name='点名ID')
    UCC_CollectTime = models.DateField(auto_now=True, verbose_name='时间')

    class Meta:
        verbose_name = '围观'
        verbose_name_plural = '**2**用户围观**2**'
        app_label = 'NTWebsite'