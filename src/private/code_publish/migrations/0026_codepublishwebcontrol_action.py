# Generated by Django 2.0.1 on 2019-08-06 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_publish', '0025_remove_codepublishwebcontrol_steps'),
    ]

    operations = [
        migrations.AddField(
            model_name='codepublishwebcontrol',
            name='action',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
