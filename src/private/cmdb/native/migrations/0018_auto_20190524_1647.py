# Generated by Django 2.0.1 on 2019-05-24 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('native', '0017_auto_20190524_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nativehost',
            name='updated',
            field=models.DateTimeField(auto_now=True, help_text='str; 更新时间', null=True),
        ),
    ]
