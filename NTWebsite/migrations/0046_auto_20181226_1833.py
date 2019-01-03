# Generated by Django 2.0.6 on 2018-12-26 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NTWebsite', '0045_auto_20181226_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationtable',
            name='NT_Sign',
            field=models.CharField(default='', max_length=30, verbose_name='标记'),
        ),
        migrations.AlterField(
            model_name='notificationtable',
            name='NT_Part',
            field=models.CharField(default='', max_length=30, verbose_name='板块'),
        ),
        migrations.AlterField(
            model_name='notificationtable',
            name='NT_URL',
            field=models.CharField(max_length=30, verbose_name='URL'),
        ),
    ]