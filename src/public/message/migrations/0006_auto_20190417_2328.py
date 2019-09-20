# Generated by Django 2.0.1 on 2019-04-17 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0005_auto_20190417_2300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messageinner',
            name='work_id',
        ),
        migrations.RemoveField(
            model_name='messagemail',
            name='work_id',
        ),
        migrations.RemoveField(
            model_name='messagepush',
            name='work_id',
        ),
        migrations.AddField(
            model_name='messageinner',
            name='work_order',
            field=models.CharField(default=None, help_text='int; 工单号', max_length=100),
        ),
        migrations.AddField(
            model_name='messagemail',
            name='work_order',
            field=models.CharField(default=None, help_text='int; 工单号', max_length=100),
        ),
        migrations.AddField(
            model_name='messagepush',
            name='work_order',
            field=models.CharField(default=None, help_text='int; 工单号', max_length=100),
        ),
    ]
