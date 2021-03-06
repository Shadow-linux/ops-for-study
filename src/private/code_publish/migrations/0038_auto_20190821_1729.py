# Generated by Django 2.0.1 on 2019-08-21 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_publish', '0037_auto_20190821_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codepublishlockenv',
            name='expired',
            field=models.DateTimeField(help_text='过期时间', null=True),
        ),
        migrations.AlterField(
            model_name='codepublishlockenvapp',
            name='app_name_id',
            field=models.IntegerField(help_text='AppNameID from cp_main_conf', unique=True),
        ),
    ]
