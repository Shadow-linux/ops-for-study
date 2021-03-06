# Generated by Django 2.0.1 on 2019-05-27 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0011_auto_20190527_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitordomain',
            name='compare_num',
            field=models.IntegerField(default=0, help_text='用于对比的数字，该数字通过不同类型的算法计算出来的'),
        ),
        migrations.AddField(
            model_name='monitorecs',
            name='compare_num',
            field=models.IntegerField(default=0, help_text='用于对比的数字，该数字通过不同类型的算法计算出来的'),
        ),
        migrations.AddField(
            model_name='monitornas',
            name='compare_num',
            field=models.IntegerField(default=0, help_text='用于对比的数字，该数字通过不同类型的算法计算出来的'),
        ),
        migrations.AddField(
            model_name='monitorrds',
            name='compare_num',
            field=models.IntegerField(default=0, help_text='用于对比的数字，该数字通过不同类型的算法计算出来的'),
        ),
        migrations.AddField(
            model_name='monitorvpn',
            name='compare_num',
            field=models.IntegerField(default=0, help_text='用于对比的数字，该数字通过不同类型的算法计算出来的'),
        ),
    ]
