# Generated by Django 2.0.1 on 2019-08-23 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_publish', '0041_codepublishlockenv_app_ids'),
    ]

    operations = [
        migrations.AddField(
            model_name='codepublishlockenv',
            name='delay_lock_time',
            field=models.IntegerField(default=0, help_text='延长锁定时间'),
        ),
    ]
