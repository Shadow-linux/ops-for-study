from django.db import models


class MonitorDateTPMixin(models.Model):
    IS_MONITOR_CHOICE = [
        (1, '是'),
        (0, '否')
    ]
    compare_num = models.IntegerField(default=0, help_text='用于对比的数字，该数字通过不同类型的算法计算出来的')
    create_time = models.DateTimeField(null=True, help_text='创建时间')
    expire_time = models.DateTimeField(null=True, help_text='过期时间')
    updated = models.DateTimeField(auto_now=True, help_text='更新时间', null=True)
    is_monitor = models.BooleanField(default=1, help_text='1, 0; 是否监控', choices=IS_MONITOR_CHOICE)

    class Meta:
        abstract = True


class MonitorNumberTPMixin(models.Model):
    IS_MONITOR_CHOICE = [
        (1, '是'),
        (0, '否')
    ]
    work_order = models.CharField(max_length=128, null=True, help_text='工单 唯一ID')
    compare_num = models.IntegerField(default=0,
                                      help_text='用于对比的数字，该数字通过不同类型的算法计算出来的, 如 "剩余量" 等')
    updated = models.DateTimeField(auto_now=True, help_text='更新时间', null=True)
    is_monitor = models.BooleanField(default=1, help_text='1, 0; 是否监控', choices=IS_MONITOR_CHOICE)

    class Meta:
        abstract = True


class MonitorThirdPartyJitterStrategy(models.Model):

    monitor_item = models.CharField(max_length=50, null=True, help_text='监控项目')
    work_order = models.CharField(max_length=128, null=True, help_text='工单 唯一ID')
    alert_number = models.IntegerField(null=True, help_text='告警数量')
    op = models.CharField(max_length=10, help_text='操作符: >, <, >=, <=, ==', null=True)
    hours_ago = models.IntegerField(default=1, help_text='对比第几个个小时前的数据')
    note = models.CharField(max_length=128, help_text='告警内容', null=True)
    send_user_id = models.CharField(max_length=256, help_text='发送的user id 列表', null=True)
    created = models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True)
    updated = models.DateTimeField(auto_now=True, help_text='更新时间', null=True)
    is_alarm = models.BooleanField(default=True, help_text='是否告警')
    is_mail = models.BooleanField(default=0, help_text='发送email')
    is_message = models.BooleanField(default=0, help_text='发送短信')
    is_wechat = models.BooleanField(default=0, help_text='发送微信')

    def __str__(self):
        return f'{self.work_order}'

    class Meta:
        db_table = 'monitor_tp_jitter_strategy'
        verbose_name = '第三方服务抖动监控策略'


class MonitorThirdPartyStrategy(models.Model):

    monitor_item = models.CharField(max_length=50, null=True, help_text='监控项目')
    work_order = models.CharField(max_length=128, null=True, help_text='工单 唯一ID')
    alert_number = models.IntegerField(null=True, help_text='告警数量')
    op = models.CharField(max_length=10, help_text='操作符: >, <, >=, <=, ==', null=True)
    note = models.CharField(max_length=128, help_text='告警内容', null=True)
    send_user_id = models.CharField(max_length=256, help_text='发送的user id 列表', null=True)
    created = models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True)
    updated = models.DateTimeField(auto_now=True, help_text='更新时间', null=True)
    is_alarm = models.BooleanField(default=True, help_text='是否告警')
    is_mail = models.BooleanField(default=0, help_text='发送email')
    is_message = models.BooleanField(default=0, help_text='发送短信')
    is_wechat = models.BooleanField(default=0, help_text='发送微信')

    def __str__(self):
        return f'{self.note}'

    class Meta:
        db_table = 'monitor_tp_strategy'
        verbose_name = '第三方监控策略'


class MonitorECS(MonitorDateTPMixin):

    hostname = models.CharField(max_length=128, null=True, help_text='hostname')
    server_id = models.CharField(max_length=128, null=True, help_text='server id')
    status = models.CharField(max_length=50, null=True, help_text='status')

    class Meta:
        db_table = 'monitor_ecs'
        verbose_name = '监控-ECS'


class MonitorRDS(MonitorDateTPMixin):

    instance_id = models.CharField(max_length=128, help_text='instance id', null=True)
    instance_desc = models.CharField(max_length=128, null=True, help_text='instance description')
    status = models.CharField(max_length=50, help_text='状态', null=True, default='Running')

    class Meta:
        db_table = 'monitor_rds'
        verbose_name = '监控-RDS'


class MonitorNAS(MonitorDateTPMixin):

    system_id = models.CharField(max_length=128, help_text='system id', null=True)
    package_id = models.CharField(max_length=128, help_text='package id', null=True)
    desc = models.CharField(max_length=128, null=True, help_text='描述')

    class Meta:
        db_table = 'monitor_nas'
        verbose_name = '监控-NAS'


class MonitorVPN(MonitorDateTPMixin):

    vpc_id = models.CharField(max_length=128, help_text='vpc id', null=True)
    vpn_id = models.CharField(max_length=128, help_text='gateway id', null=True)
    desc = models.CharField(max_length=128, help_text='描述', null=True)
    status = models.CharField(max_length=50, help_text='状态', null=True)

    class Meta:
        db_table = 'monitor_vpn'
        verbose_name = '监控-VPN'


class MonitorDomain(MonitorDateTPMixin):

    domain = models.CharField(max_length=128, help_text='domain', null=True)
    status = models.CharField(max_length=50, help_text='状态', null=True)

    class Meta:
        db_table = 'monitor_domain'
        verbose_name = '监控-Domain'
        
        
class MonitorYueXinSms(MonitorNumberTPMixin):
    req_code = models.CharField(max_length=64, help_text='状态', null=True)
    req_message = models.CharField(max_length=64, help_text='查询信息', null=True)
    balance = models.IntegerField(default=0, null=True)
    username = models.CharField(max_length=32, help_text='用户名', null=True, unique=True)

    class Meta:
        db_table = 'monitor_yuexin_sms'
        verbose_name = '监控-阅信-SMS'


class MonitorXunChengEryaosu(MonitorNumberTPMixin):
    number = models.IntegerField(default=0, null=True, help_text='剩余量')
    key = models.CharField(max_length=64, help_text='key', null=True, unique=True)
    name_desc = models.CharField(max_length=64, help_text='项目描述', null=True)
    reason = models.CharField(max_length=64, help_text='返回信息', null=True)
    error_code = models.SmallIntegerField(default=0, help_text='错误码')

    class Meta:
        db_table = 'monitor_xuncheng_eryaosu'
        verbose_name = '监控-寻程-二要素验证'


class MonitorWanWeiYiYuanBankIdentity(MonitorNumberTPMixin):
    remain_unit = models.IntegerField(default=0, null=True, help_text='剩余量')
    total_unit = models.IntegerField(default=0, null=True, help_text='总量')
    api_name = models.CharField(max_length=64, help_text='api name', null=True, unique=True)

    class Meta:
        db_table = 'monitor_wanweiyiyuan_bankidentity'
        verbose_name = '监控-万维易源-银行卡身份证验证'


class MonitorTencentSms(MonitorNumberTPMixin):
    amount = models.IntegerField(default=0, null=True, help_text='总量')
    used = models.IntegerField(default=0, null=True, help_text='使用量')
    package_id = models.CharField(max_length=64, help_text='pkg_id', null=True, unique=True)

    class Meta:
        db_table = 'monitor_tencent_sms'
        verbose_name = '监控-腾讯-SMS'


class MonitorTPStrategyItemRel(models.Model):

    CURRENT_ALARM_CHOICE = [
        (1, '告警'),
        (0, '恢复')
    ]

    strategy_id = models.IntegerField(null=True, help_text='策略ID')
    monitor_item_id = models.IntegerField(null=True, help_text='监控项目 ID')
    monitor_item = models.CharField(max_length=64, help_text='监控项目')
    current_alarm = models.SmallIntegerField(default=0, help_text='是在告警', choices=CURRENT_ALARM_CHOICE)

    class Meta:
        db_table = 'monitor_tpstrategy_item_rel'
        verbose_name = '监控-第三方策略—监控项目-告警关系'