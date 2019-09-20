from django.db import models
from cmdb.cmdb_common.models import CMDBMixin

# Create your models here.

# class NativeHost(models.Model):
#     """
#     本地服务器资源
#     """
#     # 公有 (所有cmdb model保持一致)
#     STATUS_CHOICES = [
#         ('Running', '运行中'),
#         ('Starting', '启动中'),
#         ('Stopping', '停止中'),
#         ('Stopped', '已停止')
#     ]
#     IS_ACTIVE_CHOICES = [
#         (0, '回收'),
#         (1, '使用中')
#     ]
#     IS_ANSIBLE_CHOICES = [
#         (0, '禁用'),
#         (1, '激活')
#     ]
#     hostname = models.CharField(max_length=100, null=True, help_text='str; 主机名')
#     serial_number = models.CharField(max_length=100, null=True, help_text='str;')
#     cpu = models.IntegerField(null=True, help_text='int; cpu数量')
#     memory = models.IntegerField(null=True, help_text='int; memory MB')
#     os_type = models.CharField(max_length=20, null=True, help_text='str; 系统类型')
#     os_name = models.CharField(max_length=50, null=True, help_text='str; 系统名')
#     disk = models.CharField(max_length=500, null=True, help_text='str; 磁盘列表')
#     private_ip = models.CharField(max_length=200, null=True, help_text='str; 内网IP')
#     public_ip = models.CharField(max_length=100, null=True, help_text='str; 公网IP')
#     status = models.CharField(max_length=20, null=True, help_text='str; status', choices=STATUS_CHOICES)
#     environment = models.CharField(max_length=50, default='undefined', help_text='str; 环境名')
#     is_active = models.BooleanField(default=1, choices=IS_ACTIVE_CHOICES, help_text='int; 是否使用中')
#     updated = models.DateTimeField(auto_now=True, null=True, help_text='str; 更新时间')
#     ssh_port = models.IntegerField(default=38333, null=True, help_text='int; ssh 端口')
#     ssh_ip = models.CharField(max_length=50, null=True, help_text='str; ssh ip')
#     swap = models.IntegerField(null=True, help_text='int; swap')
#     is_ansible = models.BooleanField(default=1, choices=IS_ANSIBLE_CHOICES, help_text='int; 是否激活')
#     # 私有
#     idc = models.CharField(max_length=50, null=True, help_text='str; IDC')
#     description = models.CharField(max_length=500, default='none', null=True, help_text='str; 描述')
#
#     class Meta:
#         db_table = 'cmdb_native_host'
#         verbose_name = 'cmdb 本地服务器资源'


class NativeHost(CMDBMixin):
    # 私有
    idc = models.CharField(max_length=50, null=True, help_text='str; IDC')
    description = models.CharField(max_length=500, default='none', null=True, help_text='str; 描述')

    class Meta:
        db_table = 'cmdb_native_host'
        verbose_name = 'cmdb 本地服务器资源'

