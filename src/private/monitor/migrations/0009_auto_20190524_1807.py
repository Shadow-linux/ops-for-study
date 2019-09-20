# Generated by Django 2.0.1 on 2019-05-24 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0008_auto_20190524_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitorthirdpartystrategy',
            name='op',
            field=models.CharField(help_text='操作符: >, <, >=, <=, ==', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='monitorthirdpartystrategy',
            name='send_user_id',
            field=models.CharField(help_text='发送的user id 列表', max_length=256, null=True),
        ),
    ]
