# Generated by Django 2.0.1 on 2019-07-31 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0020_settingconf_code_publish_setting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settingconf',
            name='code_publish_setting',
            field=models.TextField(default='{}', help_text='json; code publish设置', null=True),
        ),
    ]
