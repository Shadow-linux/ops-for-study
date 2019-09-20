# Generated by Django 2.0.1 on 2019-04-14 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MessageInner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.TextField(help_text='接收用户的id')),
                ('title', models.CharField(help_text='标题', max_length=200)),
                ('content', models.TextField(help_text='内容')),
                ('is_succeed', models.BooleanField(default=False, help_text='是否发送成功')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='创建时间')),
            ],
            options={
                'verbose_name': '站内信息',
                'db_table': 'common_message_inner',
            },
        ),
        migrations.CreateModel(
            name='MessageMail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(help_text='用户id')),
                ('receiver', models.TextField(help_text='目标邮箱')),
                ('title', models.CharField(help_text='邮件标题', max_length=200)),
                ('content', models.TextField(help_text='邮件内容')),
                ('is_succeed', models.BooleanField(default=False, help_text='是否发送成功')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='创建时间')),
            ],
            options={
                'verbose_name': '邮件信息',
                'db_table': 'common_message_mail',
            },
        ),
    ]
