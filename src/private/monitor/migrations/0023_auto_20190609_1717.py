# Generated by Django 2.0.1 on 2019-06-09 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0022_auto_20190609_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitortpstrategyitemrel',
            name='current_alarm',
            field=models.SmallIntegerField(choices=[(1, '告警'), (0, '恢复')], default=0, help_text='是在告警'),
        ),
    ]
