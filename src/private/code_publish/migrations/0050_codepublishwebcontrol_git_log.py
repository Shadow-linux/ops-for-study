# Generated by Django 2.0.1 on 2019-08-30 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_publish', '0049_auto_20190828_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='codepublishwebcontrol',
            name='git_log',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
