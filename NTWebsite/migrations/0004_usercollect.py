# Generated by Django 2.0.6 on 2018-10-26 09:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('NTWebsite', '0003_userlink'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCollect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UC_CollectTime', models.DateField(auto_now=True, verbose_name='时间')),
                ('UC_Article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NTWebsite.TopicArticleStatistic', to_field='TAS_Title', verbose_name='文章ID')),
                ('UC_UserNickName', models.ForeignKey(default='flysafely', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username', verbose_name='用户名')),
            ],
            options={
                'verbose_name_plural': '用户收藏',
            },
        ),
    ]
