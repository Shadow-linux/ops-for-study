# Generated by Django 2.0.1 on 2019-05-13 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_auto_20190513_1505'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AccessLogAlarm',
            new_name='AccessAlarmStrategy',
        ),
        migrations.AlterModelTable(
            name='accessalarmstrategy',
            table='business_access_alarm_strategy',
        ),
    ]
