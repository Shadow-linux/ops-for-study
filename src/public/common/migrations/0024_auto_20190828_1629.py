# Generated by Django 2.0.1 on 2019-08-28 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0023_auto_20190828_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appalivebrief',
            name='success_rate',
            field=models.FloatField(default=0.0, help_text='成功率'),
        ),
    ]
