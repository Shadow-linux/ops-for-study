# Generated by Django 2.0.1 on 2019-05-01 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('native', '0011_nativehost_swap'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nativehost',
            name='hostname',
            field=models.CharField(help_text='str; 主机名', max_length=200, null=True),
        ),
    ]
