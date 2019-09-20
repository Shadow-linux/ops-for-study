# Generated by Django 2.0.1 on 2019-05-02 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('native', '0014_nativehost_is_ansible'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nativehost',
            name='description',
            field=models.CharField(help_text='str; 描述', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='nativehost',
            name='updated',
            field=models.DateTimeField(auto_now=True, help_text='str; 更新时间', null=True),
        ),
    ]
