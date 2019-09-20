from django.db import models
# Create your models here.

from cmdb.cmdb_common.models import CMDBMixin
from django.db import models

class AliyunKeys(models.Model):

    class Meta:
        db_table = 'cmdb_cloud_aliyun_keys'
        verbose_name = 'cmdb阿里云keys'

    key_name = models.CharField(max_length=150, default=None, null=True, help_text='str; key名')
    access_key = models.CharField(max_length=100, default=None, null=True, help_text='str; access key')
    access_secret = models.CharField(max_length=100, default=None, null=True, help_text='str; access secret')
    region_id = models.CharField(max_length=50, default=None, help_text='str; 区域id', null=True)
    updated = models.DateTimeField(auto_now=True, help_text='更改时间')


class AliyunEcs(CMDBMixin):
    # 私有
    INSTANCE_CHARGE_TYPE_CHOICES = [
        ('PrePaid', '包年包月'),
        ('PostPaid', '按量计费')
    ]
    ac_key_id = models.IntegerField(help_text='int; access key id', null=True)
    disk_id = models.CharField(max_length=1024, null=True, help_text='str; disk_id')
    zone_id = models.CharField(max_length=50, null=True, help_text='str; 可用区')
    region_id = models.CharField(max_length=50, null=True, help_text='str; 区域ID')
    created = models.DateTimeField(null=True, help_text='str; 创建时间')
    expired_time = models.DateTimeField(null=True, help_text='str; 过期时间')
    instance_type = models.CharField(max_length=50, null=True, help_text='str; 实例类型')
    instance_name = models.CharField(max_length=100, null=True, help_text='str; 实例名字')
    instance_id = models.CharField(max_length=100, null=True, help_text='str; 实例ID')
    instance_charge_type = models.CharField(max_length=20, null=True, help_text='str; 付费方式',
                                            choices=INSTANCE_CHARGE_TYPE_CHOICES)

    class Meta:
        db_table = 'cmdb_cloud_aliyun_ecs'
        verbose_name = 'cmdb 阿里云 ECS'


class AliyunRDS(models.Model):

    instance_id = models.CharField(max_length=128, help_text='instance id', null=True)
    instance_desc = models.CharField(max_length=128, null=True, help_text='instance description')
    ac_key_id = models.IntegerField(help_text='int; access key id', null=True)
    environment = models.CharField(max_length=50, default='undefined', help_text='str; 环境名')
    is_active = models.BooleanField(default=1, help_text='是否在使用中')
    status = models.CharField(max_length=50, help_text='状态', null=True, default='Running')
    create_time = models.DateTimeField(null=True, help_text='创建时间')
    expire_time = models.DateTimeField(null=True, help_text='过期时间')
    updated = models.DateTimeField(auto_now=True, help_text='更新时间', null=True)

    class Meta:
        db_table = 'cmdb_cloud_aliyun_rds'
        verbose_name = 'cmdb 阿里云 RDS'
