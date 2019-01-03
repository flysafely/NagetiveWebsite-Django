from django.db import models

class ConfigParams(models.Model):
    """docstring for ConfigParams"""

    CP_Name = models.CharField(max_length=20, unique=True, verbose_name='配置名称')
    CP_ReadsThreshold = models.IntegerField(
        default=10, blank=False, verbose_name='上榜阅读量')
    CP_HotKeyWord = models.CharField(max_length=20,
                                     default='差评', blank=False, verbose_name='热搜关键字')
    CP_TopicsLimit = models.IntegerField(
        default=100, blank=False, verbose_name='文章获取数量')
    CP_CommentsLimit = models.IntegerField(
        default=100, blank=False, verbose_name='文章评论获取数量')
    CP_SecretKey = models.CharField(
        max_length=16, blank=False, verbose_name='加密秘钥')
    CP_SecretVI = models.CharField(
        max_length=16, blank=False, verbose_name='加密偏移量')
    CP_TopicsPageLimit = models.IntegerField(
        default=10, blank=False, verbose_name='每页文章数量')
    CP_SpecialTopicsPageLimit = models.IntegerField(
        default=10, blank=False, verbose_name='每页专题数量')
    CP_RollCallsPageLimit = models.IntegerField(
        default=10, blank=False, verbose_name='每页点名数量')
    CP_CommentsPageLimit = models.IntegerField(
        default=10, blank=False, verbose_name='每页评论数量')
    CP_AvatarResolution = models.IntegerField(
        default=102, blank=False, verbose_name='头像分辨率')

    class Meta:
        # 末尾不加s
        verbose_name = '配置参数'
        verbose_name_plural = '*****配置参数*****'
        app_label = 'NTWebsite'
        #app_label = "配置表"

    def __str__(self):
        return self.CP_Name


class PreferredConfigName(models.Model):
    PC_Name = models.ForeignKey(
        ConfigParams, to_field='CP_Name', on_delete=models.CASCADE, verbose_name='首选配置名称')

    class Meta:
        verbose_name = '首选配置'
        app_label = 'NTWebsite'
        # 末尾不加s

        verbose_name_plural = '*****首选配置设置*****'
        pass
