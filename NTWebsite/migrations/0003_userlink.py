# Generated by Django 2.0.6 on 2018-10-24 09:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('NTWebsite', '0002_auto_20181024_1618'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UL_UserBeLinked', models.CharField(max_length=100, verbose_name='用户')),
                ('UL_LinkTime', models.DateField(auto_now=True, verbose_name='时间')),
                ('UL_UserLinking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username', verbose_name='关注用户')),
            ],
            options={
                'verbose_name_plural': '关注信息',
            },
        ),
    ]
