# Generated by Django 2.0.6 on 2018-11-13 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NTWebsite', '0012_auto_20181112_1725'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rollcallinfo',
            name='RCI_Dialogue',
        ),
        migrations.RemoveField(
            model_name='rollcallinfo',
            name='RCI_IsRead',
        ),
    ]
