# Generated by Django 2.0.1 on 2019-06-18 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0011_auto_20190618_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='aliyunrds',
            name='environment',
            field=models.CharField(default='undefined', help_text='str; 环境名', max_length=50),
        ),
    ]
