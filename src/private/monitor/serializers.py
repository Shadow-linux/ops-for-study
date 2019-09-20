from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import (
    MonitorTPStrategyItemRel,
    MonitorThirdPartyStrategy,
    MonitorThirdPartyJitterStrategy,
    MonitorECS,
    MonitorYueXinSms,
    MonitorRDS,
    MonitorNAS,
    MonitorDomain,
    MonitorVPN,
    MonitorTencentSms,
    MonitorWanWeiYiYuanBankIdentity,
    MonitorXunChengEryaosu,
)


class MonitorAppAliveLatestDataSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    http_method = serializers.CharField(help_text='GET')
    data = serializers.JSONField(help_text='''json; 
    数据格式: [
        {
            "app_id": 1000,
            "env": "undefined",
            "check_api": "http://10.81.126.19:8009/info"
        },
        {
            "app_id": 2,
            "env": "release",
            "check_api": "http://1.1.1.2:10001/info"
        }
    ]''')


class MonitorThirdPartyStrategyJitterSerializer(serializers.ModelSerializer):
    monitor_item = serializers.CharField(
        help_text=''''监控项目 
        ('yuexin_sms', 'xuncheng_eryaosu', 'wanweiyiyuan_bankid', 'tencent_sms')''',
        required=True)
    alert_number = serializers.IntegerField(help_text='告警数量', required=True)
    hours_ago = serializers.IntegerField(help_text='对比第几个个小时前的数据', required=True)
    work_order = serializers.CharField(read_only=True, help_text='工单 唯一ID')
    op = serializers.CharField(help_text='操作符: >, <, >=, <=, ==', required=True)
    note = serializers.CharField(help_text='告警内容', required=True)
    send_user_id = serializers.JSONField(help_text='发送的user id 列表', required=True)
    is_alarm = serializers.BooleanField(help_text='是否告警', required=True)
    is_mail = serializers.BooleanField(help_text='发送email', required=True)
    is_message = serializers.BooleanField(help_text='发送短信', required=True)
    is_wechat = serializers.BooleanField(help_text='发送微信', required=True)
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = MonitorThirdPartyJitterStrategy
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('monitor_item', 'op', 'alert_number')
            )
        ]


class MonitorThirdPartyStrategySerializer(serializers.ModelSerializer):
    monitor_item = serializers.CharField(
        help_text=''''监控项目 
    ('ecs', 'rds', 'nas', 'domain', 'vpn', 'yuexin_sms', 'xuncheng_eryaosu', 'wanweiyiyuan_bankid', 'tencent_sms')''',
        required=True)
    alert_number = serializers.IntegerField(help_text='告警数量', required=True)
    work_order = serializers.CharField(read_only=True, help_text='工单 唯一ID')
    op = serializers.CharField(help_text='操作符: >, <, >=, <=, ==', required=True)
    note = serializers.CharField(help_text='告警内容', required=True)
    send_user_id = serializers.JSONField(help_text='发送的user id 列表', required=True)
    is_alarm = serializers.BooleanField(help_text='是否告警', required=True)
    is_mail = serializers.BooleanField(help_text='发送email', required=True)
    is_message = serializers.BooleanField(help_text='发送短信', required=True)
    is_wechat = serializers.BooleanField(help_text='发送微信', required=True)
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)

    class Meta:
        model = MonitorThirdPartyStrategy
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('monitor_item', 'op', 'alert_number')
            )
        ]


class MonitorTPECSSerializer(serializers.ModelSerializer):
    expire_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    current_alarm = serializers.SerializerMethodField(method_name='return_current_alarm', read_only=True)

    def return_current_alarm(self, obj):
        if MonitorTPStrategyItemRel.objects.filter(monitor_item='ecs', monitor_item_id=obj.id, current_alarm=1):
            return True
        return False

    class Meta:
        model = MonitorECS
        fields = '__all__'


class MonitorTPNASSerializer(serializers.ModelSerializer):
    expire_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    current_alarm = serializers.SerializerMethodField(method_name='return_current_alarm', read_only=True)

    def return_current_alarm(self, obj):
        if MonitorTPStrategyItemRel.objects.filter(monitor_item='nas', monitor_item_id=obj.id, current_alarm=1):
            return True
        return False

    class Meta:
        model = MonitorNAS
        fields = '__all__'


class MonitorTPRDSSerializer(serializers.ModelSerializer):
    expire_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    current_alarm = serializers.SerializerMethodField(method_name='return_current_alarm', read_only=True)

    def return_current_alarm(self, obj):
        if MonitorTPStrategyItemRel.objects.filter(monitor_item='rds', monitor_item_id=obj.id, current_alarm=1):
            return True
        return False

    class Meta:
        model = MonitorRDS
        fields = '__all__'


class MonitorTPDomainSerializer(serializers.ModelSerializer):
    expire_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    current_alarm = serializers.SerializerMethodField(method_name='return_current_alarm', read_only=True)

    def return_current_alarm(self, obj):
        if MonitorTPStrategyItemRel.objects.filter(monitor_item='domain', monitor_item_id=obj.id, current_alarm=1):
            return True
        return False

    class Meta:
        model = MonitorDomain
        fields = '__all__'


class MonitorTPVpnSerializer(serializers.ModelSerializer):
    expire_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    current_alarm = serializers.SerializerMethodField(method_name='return_current_alarm', read_only=True)

    def return_current_alarm(self, obj):
        if MonitorTPStrategyItemRel.objects.filter(monitor_item='vpn', monitor_item_id=obj.id, current_alarm=1):
            return True
        return False

    class Meta:
        model = MonitorVPN
        fields = '__all__'


class MonitorTPYueXinSerializer(serializers.ModelSerializer):
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    current_alarm = serializers.SerializerMethodField(method_name='return_current_alarm', read_only=True)

    def return_current_alarm(self, obj):
        if MonitorTPStrategyItemRel.objects.filter(monitor_item='yuexin_sms', monitor_item_id=obj.id, current_alarm=1):
            return True
        return False

    class Meta:
        model = MonitorYueXinSms
        fields = '__all__'


class MonitorTPTencentSmsSerializer(serializers.ModelSerializer):
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    current_alarm = serializers.SerializerMethodField(method_name='return_current_alarm', read_only=True)

    def return_current_alarm(self, obj):
        if MonitorTPStrategyItemRel.objects.filter(monitor_item='tencent_sms', monitor_item_id=obj.id, current_alarm=1):
            return True
        return False

    class Meta:
        model = MonitorTencentSms
        fields = '__all__'


class MonitorTPWanweiyiyuanBankIdentitySerializer(serializers.ModelSerializer):
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    current_alarm = serializers.SerializerMethodField(method_name='return_current_alarm', read_only=True)

    def return_current_alarm(self, obj):
        if MonitorTPStrategyItemRel.objects.filter(monitor_item='wanweiyiyuan_bankid',
                                                   monitor_item_id=obj.id, current_alarm=1):
            return True
        return False

    class Meta:
        model = MonitorWanWeiYiYuanBankIdentity
        fields = '__all__'


class MonitorTPXunChengEryaosuSerializer(serializers.ModelSerializer):
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False)
    current_alarm = serializers.SerializerMethodField(method_name='return_current_alarm', read_only=True)

    def return_current_alarm(self, obj):
        if MonitorTPStrategyItemRel.objects.filter(monitor_item='xuncheng_eryaosu',
                                                   monitor_item_id=obj.id, current_alarm=1):
            return True
        return False

    class Meta:
        model = MonitorXunChengEryaosu
        fields = '__all__'
