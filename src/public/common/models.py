from django.db import models

# Create your models here.


class SettingConf(models.Model):
    """
    基础设置
    """
    owner = models.CharField(max_length=50, help_text='str; 属主', null=True)
    is_mail = models.BooleanField(default=True, help_text='int; 是否启用mail')
    is_inner = models.BooleanField(default=True, help_text='int; 是否启用站内信息')
    """ message_setting 数据格式
    {
        "mail": {
            "smtp_host": "smtp.ym.163.com", 
            "smtp_port": 465, 
            "smtp_ssl": true, 
            "mail_user": "ops@ishouru.com", 
            "mail_password": "ayg99*OPS&"
        }
    }
    """
    message_setting = models.CharField(max_length=1024, help_text='json; 消息设置', null=True)
    """ cmdb_setting 数据格式
    {
        "base": {
            "idc": ["idc1", "idc2"],
            "env": ["release", "pre-release"]
            "ssh_proxy": {
                "aliyun": "AliyunEcs",
                "native": "NativeHost"
            }
        }
    }
    """
    cmdb_setting = models.CharField(max_length=1024, help_text='json; cmdb设置', null=True)

    """ app_setting 数据格式
    {
        "service": ["docker", "k8s", "java"]
        "env_monitor_agent": {"test92": "internal.ayg.gz", "default": "release"}
    }
    """
    app_setting = models.CharField(max_length=1024, help_text='json; app设置', null=True)

    """code_publish_setting
    {
        "server_mode": ["docker"],
        "jenkins_project": ["ops-deposit"],
        "git_info": {
            "username": "",
            "password": ""
        }
    }
    """
    code_publish_setting = models.TextField(help_text='json; code publish设置', default='{}', null=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'common_setting_conf'
        verbose_name = '基础设置'


class AnsibleHost(models.Model):

    hostname = models.CharField(max_length=128, null=True, blank=True, help_text='主机名')
    group_name = models.CharField(max_length=128, null=True, help_text='组名')
    host = models.CharField(max_length=20, null=True, help_text='ssh ip')
    ansible_port = models.IntegerField(null=True, help_text='ansible port')
    ansible_user = models.CharField(max_length=128, null=True, help_text='ansible user')
    var_env = models.CharField(max_length=128, null=True, help_text='env')
    var_domain = models.CharField(max_length=128, null=True, help_text='domain')

    def __str__(self):
        return self.hostname

    class Meta:
        db_table = 'common_ansible_host'
        verbose_name = 'ansible的inventory'


class AppAliveStatistics(models.Model):

    app_name = models.CharField(max_length=128, null=True, help_text='app name')
    failed_point_amount = models.IntegerField(default=0, help_text='失败的点总数， 5分钟一个点')
    created = models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True)

    def __str__(self):
        return self.app_name

    class Meta:
        db_table = 'common_app_alive_statistics'


class AppALiveBrief(models.Model):
    app_name = models.CharField(max_length=128, null=True, help_text='app name')
    success_rate = models.FloatField(default=0.0, help_text='成功率')
    days = models.SmallIntegerField(default=1, help_text='几天前')
    updated = models.DateTimeField(auto_now=True, help_text='更新时间', null=True)

    def __str__(self):
        return self.app_name

    class Meta:
        db_table = 'common_app_alive_brief'