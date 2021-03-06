# Generated by Django 2.0.1 on 2019-04-22 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_key', models.CharField(help_text='str; 标签名', max_length=100, null=True)),
                ('tag_value', models.CharField(help_text='str; 标签值', max_length=200, null=True)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='str; 建立时间')),
            ],
            options={
                'verbose_name': 'cmdb 资源标签',
                'db_table': 'cmdb_tags',
            },
        ),
        migrations.CreateModel(
            name='TagsAliyunEcsRel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_id', models.IntegerField(help_text='int; tag id', null=True)),
                ('target_id', models.IntegerField(help_text='int; aliyun ecs id', null=True)),
            ],
            options={
                'verbose_name': 'cmdb tag 与 阿里云 ecs 关系',
                'db_table': 'cmdb_tags_aliyunecs_rel',
            },
        ),
        migrations.CreateModel(
            name='TagsAppRel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_id', models.IntegerField(help_text='int; tag id', null=True)),
                ('target_id', models.IntegerField(help_text='int; app id', null=True)),
            ],
            options={
                'verbose_name': 'cmdb tag 与 标签与App关系',
                'db_table': 'cmdb_tags_app_rel',
            },
        ),
        migrations.CreateModel(
            name='TagsNativeHostRel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_id', models.IntegerField(help_text='int; tag id', null=True)),
                ('target_id', models.IntegerField(help_text='int; native host id', null=True)),
            ],
            options={
                'verbose_name': 'cmdb tag 与 标签与本地服务器 关系',
                'db_table': 'cmdb_tags_nativehost_rel',
            },
        ),
    ]
