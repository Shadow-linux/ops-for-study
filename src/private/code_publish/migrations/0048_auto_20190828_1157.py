# Generated by Django 2.0.1 on 2019-08-28 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_publish', '0047_auto_20190828_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codepublishdockerfile',
            name='name',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='codepublishdockeropts',
            name='name',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='codepublishgradleopts',
            name='name',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='codepublishjaropts',
            name='name',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='codepublishjavaopts',
            name='name',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='codepublishmvnopts',
            name='name',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='codepublishsteps',
            name='name',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
