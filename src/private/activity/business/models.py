from django.db import models

# Create your models here.


class AccessAlarmStrategy(models.Model):
    """
    策略：
        1：最近（x）分钟，（什么）域名的（URI）的请求，平均请求时间，大于（设定）阈值，就进行告警。
        2：最近（x）分钟，（什么）域名的（URI）的请求，最大请求时间，大于（设定）阈值，就进行告警。
        3：最近（x）分钟，（什么）域名的（URI）的请求，超过（设定阈值）请求时间的请求数量的比例达到（告警比例阈值），就进行告警。
    """
    ALARM_STRATEGY_CHOICE = [
        ('average', '平均请求时间'),
        ('max', '最大请求时间'),
        ('cost_percent', '超过设定阀值的百分比')
    ]

    alarm_name = models.CharField(max_length=128, help_text='自定义告警名称', null=True)
    work_order = models.CharField(max_length=128, unique=True, help_text='strategy id', null=True)
    """where_params 数据格式
       {
           "http_host": "www.tokenworld.pro",
           "url": "/api.php/user/getOfficialAccount"
       }
       """
    where_condition = models.CharField(max_length=1024, help_text='检索条件', null=True)
    """alarm_strategy 数据格式
    {
        "strategy": "average", "cost": 10 // 策略， 花费时间(告警阀值)
    }
    {
        "strategy": "cost_percent", "cost": 2, "percent": 0.5  // 策略， 花费时间(告警阀值)，占比(超过占比告警)
    }
    """
    cost = models.FloatField(default=1.0, help_text='预设的秒数', null=True)
    alarm_strategy = models.CharField(max_length=1024, help_text='策略', null=True, choices=ALARM_STRATEGY_CHOICE)
    op = models.CharField(max_length=10, help_text='比较符: >, >=, ==, <, <=', null=True, default='>')
    latest_time = models.IntegerField(default=1, null=True, help_text='最近几分钟')
    is_mail = models.BooleanField(default=0, help_text='发送email')
    is_message = models.BooleanField(default=0, help_text='发送短信')
    is_wechat = models.BooleanField(default=0, help_text='发送微信')
    # 没有逆向过程，直接使用列表来关联用户
    """send_user_id 数据格式
    [1, 2, 3]
    """
    send_user_id = models.CharField(max_length=256, help_text='发送的user id 列表')
    is_alarm = models.BooleanField(default=1, help_text='是否发送告警')
    created = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    updated = models.DateTimeField(auto_now=True, help_text='更新时间')

    class Meta:
        db_table = 'business_access_alarm_strategy'
        verbose_name = 'access log url 花费时间监控'


class AccessAlarmResult(models.Model):
    ALARM_STRATEGY_CHOICE = [
        ('average', '平均请求时间'),
        ('max', '最大请求时间'),
        ('cost_percent', '超过设定阀值的百分比')
    ]

    work_order = models.CharField(max_length=128, unique=True, help_text='strategy uniq id', null=True)
    match_count = models.IntegerField(help_text='hit 的数目', default=0 ,null=True)
    cost = models.FloatField(default=1.0, help_text='预设的秒数', null=True)
    """result_set 数据结构
    {"average": 3}
    
    """
    result_set = models.CharField(max_length=1024, help_text='结果集', null=True)
    alarm_strategy = models.CharField(max_length=1024, help_text='策略', null=True, choices=ALARM_STRATEGY_CHOICE)
    where_condition = models.CharField(max_length=1024, help_text='检索条件', null=True)
    latest_time = models.IntegerField(default=1, null=True, help_text='最近几分钟')
    created = models.DateTimeField(auto_now_add=True, help_text='创建时间')
    updated = models.DateTimeField(auto_now=True, help_text='更新时间')

    class Meta:
        db_table = 'business_access_alarm_result'