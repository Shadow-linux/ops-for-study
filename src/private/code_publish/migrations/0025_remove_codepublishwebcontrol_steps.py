# Generated by Django 2.0.1 on 2019-08-06 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('code_publish', '0024_auto_20190806_1150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='codepublishwebcontrol',
            name='steps',
        ),
    ]
