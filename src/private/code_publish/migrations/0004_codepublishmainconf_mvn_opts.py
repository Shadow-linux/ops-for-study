# Generated by Django 2.0.1 on 2019-07-19 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_publish', '0003_codepublishmvnopts'),
    ]

    operations = [
        migrations.AddField(
            model_name='codepublishmainconf',
            name='mvn_opts',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
