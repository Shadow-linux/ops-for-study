# Generated by Django 2.0.1 on 2019-05-31 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0017_auto_20190529_1806'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonitorThirdPartyJitterStrategy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monitor_item', models.CharField(help_text='监控项目', max_length=50, null=True)),
                ('work_order', models.CharField(help_text='工单 唯一ID', max_length=128, null=True)),
                ('alert_number', models.IntegerField(help_text='告警数量', null=True)),
                ('op', models.CharField(help_text='操作符: >, <, >=, <=, ==', max_length=10, null=True)),
                ('note', models.CharField(help_text='告警内容', max_length=128, null=True)),
                ('send_user_id', models.CharField(help_text='发送的user id 列表', max_length=256, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True)),
                ('updated', models.DateTimeField(auto_now=True, help_text='更新时间', null=True)),
                ('is_alarm', models.BooleanField(default=True, help_text='是否告警')),
                ('is_mail', models.BooleanField(default=0, help_text='发送email')),
                ('is_message', models.BooleanField(default=0, help_text='发送短信')),
                ('is_wechat', models.BooleanField(default=0, help_text='发送微信')),
            ],
            options={
                'verbose_name': '第三方服务抖动监控策略',
                'db_table': 'monitor_tp_jitter_strategy',
            },
        ),
        migrations.AlterField(
            model_name='monitordomain',
            name='is_monitor',
            field=models.BooleanField(default=1, help_text='1, 0; 是否监控'),
        ),
        migrations.AlterField(
            model_name='monitorecs',
            name='is_monitor',
            field=models.BooleanField(default=1, help_text='1, 0; 是否监控'),
        ),
        migrations.AlterField(
            model_name='monitornas',
            name='is_monitor',
            field=models.BooleanField(default=1, help_text='1, 0; 是否监控'),
        ),
        migrations.AlterField(
            model_name='monitorrds',
            name='is_monitor',
            field=models.BooleanField(default=1, help_text='1, 0; 是否监控'),
        ),
        migrations.AlterField(
            model_name='monitortencentsms',
            name='is_monitor',
            field=models.BooleanField(default=1, help_text='1, 0; 是否监控'),
        ),
        migrations.AlterField(
            model_name='monitorvpn',
            name='is_monitor',
            field=models.BooleanField(default=1, help_text='1, 0; 是否监控'),
        ),
        migrations.AlterField(
            model_name='monitorwanweiyiyuanbankidentity',
            name='is_monitor',
            field=models.BooleanField(default=1, help_text='1, 0; 是否监控'),
        ),
        migrations.AlterField(
            model_name='monitorxunchengeryaosu',
            name='is_monitor',
            field=models.BooleanField(default=1, help_text='1, 0; 是否监控'),
        ),
        migrations.AlterField(
            model_name='monitoryuexinsms',
            name='is_monitor',
            field=models.BooleanField(default=1, help_text='1, 0; 是否监控'),
        ),
    ]
