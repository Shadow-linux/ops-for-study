# Generated by Django 2.0.1 on 2019-08-10 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_publish', '0028_auto_20190807_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='codepublishwebcontrol',
            name='has_been_published',
            field=models.CharField(help_text='已经发布的IP; list', max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='codepublishwebcontrol',
            name='is_done',
            field=models.SmallIntegerField(choices=[(0, '未完成'), (1, '完成')], default=1, help_text='0: 该环境未完整发布, 1: 是完整发布'),
        ),
        migrations.AlterField(
            model_name='codepublishwebcontrol',
            name='sync_env',
            field=models.CharField(default='[]', max_length=32, null=True),
        ),
    ]
