# Generated by Django 2.0.1 on 2019-07-24 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_publish', '0012_codepublishmainconf_server_mode'),
    ]

    operations = [
        migrations.AddField(
            model_name='codepublishmainconf',
            name='git_url',
            field=models.CharField(help_text='git url', max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='codepublishmainconf',
            name='server_mode',
            field=models.CharField(help_text='[docker|tomcat|jar|tc2docker]', max_length=32, null=True),
        ),
    ]
