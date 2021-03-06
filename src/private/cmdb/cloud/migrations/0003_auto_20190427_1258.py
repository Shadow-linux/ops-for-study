# Generated by Django 2.0.1 on 2019-04-27 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0002_remove_aliyunecs_tag_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='aliyunecs',
            name='disk_id',
            field=models.CharField(help_text='str; disk_id', max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='aliyunecs',
            name='ac_key_id',
            field=models.IntegerField(help_text='str; access key id', null=True),
        ),
    ]
