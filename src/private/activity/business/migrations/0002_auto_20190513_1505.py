# Generated by Django 2.0.1 on 2019-05-13 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accesslogalarm',
            old_name='time_ago',
            new_name='latest_time',
        ),
        migrations.RenameField(
            model_name='accesslogalarm',
            old_name='where_params',
            new_name='where_condition',
        ),
    ]
