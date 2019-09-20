# Generated by Django 2.0.1 on 2019-04-14 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190412_0047'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersaccount',
            name='ca',
            field=models.SmallIntegerField(choices=[(0, '不允许'), (1, '只读'), (2, '读写')], default=0, help_text='int: check api permission'),
        ),
    ]
