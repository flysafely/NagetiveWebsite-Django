from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# 用户信息表
class User(AbstractUser):
    """docstring for UserTable"""

    UT_Nick = models.CharField(max_length=20, verbose_name='昵称')
    #UT_CheckInDate = models.CharField(max_length=50, verbose_name='注册时间', blank=True, null=False)
    UT_Sex = models.CharField(
        max_length=3, verbose_name='性别', default="未公开", blank=True, null=False)
    UT_Region = models.CharField(
        max_length=10, verbose_name='地区', blank=True, null=True, default="城市")
    UT_Description = models.TextField(
        max_length=50, verbose_name='简介', blank=True, null=True, default="简介")
    UT_Avatar = models.TextField(max_length=1000, verbose_name='头像URL',
                                 default='/static/media/DefaultLogo.jpg', blank=True, null=False)
    UT_Constellation = models.CharField(
        max_length=10, blank=True, null=True, default='天蝎座', verbose_name='星座')
    UT_FansCount = models.IntegerField(verbose_name='关注者数量', default=0)
    UT_FoucusCount = models.IntegerField(verbose_name='关注数量', default=0)
    UT_TopicsCount = models.IntegerField(verbose_name='文章发布数量', default=0)
    UT_SpecialTopicsCount = models.IntegerField(
        verbose_name='专题发布数量', default=0)
    UT_RollCallsCount = models.IntegerField(verbose_name='点名发布数量', default=0)
    UT_RreplayCount = models.IntegerField(verbose_name='点名回复数量', default=0)
    UT_TreplayCount = models.IntegerField(verbose_name='文章评论数量', default=0)
    UT_SreplayCount = models.IntegerField(verbose_name='专题评论数量', default=0)

    class Meta(AbstractUser.Meta):
        verbose_name = '用户'
        # 末尾不加s
        #verbose_name_plural = '用户'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.UT_Nick