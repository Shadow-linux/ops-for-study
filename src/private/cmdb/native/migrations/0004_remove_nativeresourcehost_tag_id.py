# Generated by Django 2.0.1 on 2019-04-21 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('native', '0003_auto_20190421_1641'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nativeresourcehost',
            name='tag_id',
        ),
    ]
