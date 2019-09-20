from django.db import models

# Create your models here.


class AppDetail(models.Model):
    IS_ACTIVE_CHOICES = [
        (1, '使用'),
        (0, '禁用')
    ]
    IS_LAUNCH = [
        (1, '是'),
        (0, '')
    ]
    IS_PUBLISH = [
        (1, '是'),
        (0, '否')
    ]
    CHOSE_AGENT = [
        ('default', '阿里与生产(c-shenzhen)'),
        ('internal.ayg.gz', '内部广州爱员工')
    ]
    app_name = models.CharField(max_length=100, help_text='app 名字', null=True, unique=True)
    port = models.CharField(help_text='启动端口', null=True, max_length=32)
    service = models.CharField(help_text='服务', null=True, max_length=100)
    description = models.CharField(max_length=500, help_text='描述', null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=True, help_text='更新时间', null=True)
    is_active = models.BooleanField(default=1, help_text='是否使用中', choices=IS_ACTIVE_CHOICES)
    is_publish = models.BooleanField(default=0, help_text='是否可发布')
    is_monitor = models.BooleanField(default=0, help_text='是否APP Alive监控')
    is_launch = models.BooleanField(default=0, help_text='是否可运行')
    is_internal_check_api = models.BooleanField(default=0, help_text='是否发起内部api检查')
    is_external_check_api = models.BooleanField(default=0, help_text='是否发起外部api检查')
    internal_check_api = models.CharField(max_length=128, null=True, help_text='app 内部检查API', blank=True)
    # 格式： ["release", "test92"]
    internal_check_api_env = models.CharField(max_length=256, null=True, blank=True,
                                              help_text='json; app 内部检查API使用的环境 ["release", "test92"]')
    # 格式: {"undefined": "default", "release": "default", "test92": "internal.ayg.gz"}
    chose_agent = models.CharField(max_length=512, blank=True,
                                   help_text='''str; 选择发送api请求的agent
                                    {"undefined": "default", "release": "default", "test92": "internal.ayg.gz"}''',
                                   null=True)
    external_check_api = models.CharField(max_length=128, blank=True, null=True, help_text='app 外部检查API')

    class Meta:
        db_table = 'app_detail'
        verbose_name = 'app 详情'


class AppHostRel(models.Model):
    OWNER_CHOICES = [
        ('aliyun', '阿里云'),
        ('native', '本地')
    ]

    app_id = models.IntegerField(null=True, help_text='app id')
    host_id = models.IntegerField(null=True, help_text='host id')
    owner = models.CharField(max_length=50, null=True, help_text='属于哪个资源表 [aliyun|native]')

    class Meta:
        db_table = 'app_host_rel'
        verbose_name = 'app host 关系'


class AppConnectorRel(models.Model):
    app_id = models.IntegerField(null=True, help_text='app id')
    user_id = models.IntegerField(null=True, help_text='user id')

    class Meta:
        db_table = 'app_user_rel'
        verbose_name = 'app user 关系'
