# Generated by Django 2.0.1 on 2019-07-22 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('code_publish', '0010_auto_20190722_1826'),
    ]

    operations = [
        migrations.RenameField(
            model_name='codepublishdockerfile',
            old_name='c',
            new_name='docker_file',
        ),
    ]
