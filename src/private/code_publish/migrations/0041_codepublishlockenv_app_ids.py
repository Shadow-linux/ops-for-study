# Generated by Django 2.0.1 on 2019-08-23 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_publish', '0040_auto_20190822_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='codepublishlockenv',
            name='app_ids',
            field=models.CharField(default='[]', help_text='用户组', max_length=256, null=True),
        ),
    ]
