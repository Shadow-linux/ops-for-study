# Generated by Django 2.0.1 on 2019-04-30 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('native', '0009_auto_20190422_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='nativehost',
            name='ssh_ip',
            field=models.CharField(help_text='str; ssh ip', max_length=50, null=True),
        ),
    ]
