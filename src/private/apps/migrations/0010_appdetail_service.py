# Generated by Django 2.0.1 on 2019-05-10 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0009_auto_20190510_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='appdetail',
            name='service',
            field=models.CharField(help_text='服务', max_length=100, null=True),
        ),
    ]
