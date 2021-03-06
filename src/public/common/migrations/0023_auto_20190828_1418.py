# Generated by Django 2.0.1 on 2019-08-28 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0022_appalivebrief_appalivestatistics'),
    ]

    operations = [
        migrations.AddField(
            model_name='appalivebrief',
            name='days',
            field=models.SmallIntegerField(default=1, help_text='几天前'),
        ),
        migrations.AlterField(
            model_name='appalivebrief',
            name='success_rate',
            field=models.IntegerField(default=0, help_text='成功率'),
        ),
    ]
