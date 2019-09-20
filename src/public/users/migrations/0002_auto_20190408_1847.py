# Generated by Django 2.0.1 on 2019-04-08 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersaccount',
            name='group_id',
        ),
        migrations.AlterField(
            model_name='usersaccount',
            name='department',
            field=models.CharField(blank=True, help_text='str: 部门', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='usersaccount',
            name='email',
            field=models.CharField(blank=True, help_text='str: 邮箱', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='usersaccount',
            name='login_position',
            field=models.CharField(blank=True, help_text='str: 登录位置', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='usersaccount',
            name='mobile',
            field=models.CharField(blank=True, help_text='str: 手机号', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='usersaccount',
            name='position',
            field=models.CharField(blank=True, help_text='str: 职位', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='usersaccount',
            name='real_name',
            field=models.CharField(blank=True, help_text='str: 真实姓名', max_length=100, null=True),
        ),
    ]
