# Generated by Django 2.0.1 on 2019-06-07 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0010_appdetail_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='appdetail',
            name='is_monitor',
            field=models.BooleanField(default=1, help_text='是否APP Alive监控'),
        ),
    ]
