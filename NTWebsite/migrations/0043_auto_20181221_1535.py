# Generated by Django 2.0.6 on 2018-12-21 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NTWebsite', '0042_auto_20181218_1720'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='UT_CommentCount',
        ),
        migrations.AddField(
            model_name='user',
            name='UT_RollCallsCount',
            field=models.IntegerField(default=0, verbose_name='点名发布数量'),
        ),
        migrations.AddField(
            model_name='user',
            name='UT_RreplayCount',
            field=models.IntegerField(default=0, verbose_name='点名回复数量'),
        ),
        migrations.AddField(
            model_name='user',
            name='UT_SpecialTopicsCount',
            field=models.IntegerField(default=0, verbose_name='专题发布数量'),
        ),
        migrations.AddField(
            model_name='user',
            name='UT_SreplayCount',
            field=models.IntegerField(default=0, verbose_name='专题评论数量'),
        ),
        migrations.AddField(
            model_name='user',
            name='UT_TreplayCount',
            field=models.IntegerField(default=0, verbose_name='文章评论数量'),
        ),
        migrations.AlterField(
            model_name='user',
            name='UT_TopicsCount',
            field=models.IntegerField(default=0, verbose_name='文章发布数量'),
        ),
    ]
