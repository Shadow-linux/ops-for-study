import datetime
from django.db import models
# Create your models here.


class CMDBMixin(models.Model):
    # 公有 (所有cmdb model保持一致)
    STATUS_CHOICES = [
        ('Running', '运行中'),
        ('Starting', '启动中'),
        ('Stopping', '停止中'),
        ('Stopped', '已停止')
    ]
    IS_ACTIVE_CHOICES = [
        (0, '回收'),
        (1, '使用中')
    ]
    IS_ANSIBLE_CHOICES = [
        (0, '禁用'),
        (1, '激活')
    ]
    hostname = models.CharField(max_length=100, null=True, help_text='str; 主机名')
    serial_number = models.CharField(max_length=100, null=True, help_text='str;')
    cpu = models.IntegerField(null=True, help_text='int; cpu数量')
    memory = models.IntegerField(null=True, help_text='int; memory MB')
    os_type = models.CharField(max_length=20, null=True, help_text='str; 系统类型')
    os_name = models.CharField(max_length=50, null=True, help_text='str; 系统名')
    disk = models.CharField(max_length=500, null=True, help_text='str; 磁盘列表')
    private_ip = models.CharField(max_length=200, null=True, help_text='str; 内网IP')
    public_ip = models.CharField(max_length=100, null=True, help_text='str; 公网IP')
    status = models.CharField(max_length=20, null=True, help_text='str; status', choices=STATUS_CHOICES)
    environment = models.CharField(max_length=50, default='undefined', help_text='str; 环境名')
    is_active = models.BooleanField(default=1, choices=IS_ACTIVE_CHOICES, help_text='int; 是否使用中')
    updated = models.DateTimeField(auto_now=True, null=True, help_text='str; 更新时间')
    ssh_port = models.IntegerField(default=38333, null=True, help_text='int; ssh 端口')
    ssh_ip = models.CharField(max_length=50, null=True, help_text='str; ssh ip')
    swap = models.IntegerField(null=True, help_text='int; swap')
    is_ansible = models.BooleanField(default=0, choices=IS_ANSIBLE_CHOICES, help_text='int; 是否激活')

    class Meta:
        abstract = True


class Tags(models.Model):
    """
    标签表
    """
    tag_key = models.CharField(max_length=100, null=True, help_text='str; 标签名')
    tag_value = models.CharField(max_length=200, null=True, help_text='str; 标签值')
    created= models.DateTimeField(auto_now_add=True, help_text='str; 建立时间')

    class Meta:
        db_table = 'cmdb_tags'
        verbose_name = 'cmdb 资源标签'


class TagsAliyunEcsRel(models.Model):
    """
    标签与aliyun Ecs关系表
    """
    tag_id = models.IntegerField(null=True, help_text='int; tag id')
    target_id = models.IntegerField(null=True, help_text='int; aliyun ecs id')

    class Meta:
        db_table = 'cmdb_tags_aliyunecs_rel'
        verbose_name = 'cmdb tag 与 阿里云 ecs 关系'


class TagsNativeHostRel(models.Model):
    """
    标签与本地服务器 关系表
    """
    tag_id = models.IntegerField(null=True, help_text='int; tag id')
    target_id = models.IntegerField(null=True, help_text='int; native host id')

    class Meta:
        db_table = 'cmdb_tags_nativehost_rel'
        verbose_name = 'cmdb tag 与 标签与本地服务器 关系'
