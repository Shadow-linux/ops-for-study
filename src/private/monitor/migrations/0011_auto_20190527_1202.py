# Generated by Django 2.0.1 on 2019-05-27 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0010_auto_20190524_1824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monitorthirdpartystrategy',
            name='work_order',
        ),
        migrations.AddField(
            model_name='monitorthirdpartystrategy',
            name='is_mail',
            field=models.BooleanField(default=0, help_text='发送email'),
        ),
        migrations.AddField(
            model_name='monitorthirdpartystrategy',
            name='is_message',
            field=models.BooleanField(default=0, help_text='发送短信'),
        ),
        migrations.AddField(
            model_name='monitorthirdpartystrategy',
            name='is_wechat',
            field=models.BooleanField(default=0, help_text='发送微信'),
        ),
        migrations.AddField(
            model_name='monitorthirdpartystrategy',
            name='note',
            field=models.CharField(help_text='告警内容', max_length=128, null=True),
        ),
    ]
