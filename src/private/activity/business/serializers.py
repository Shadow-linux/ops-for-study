from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import AccessAlarmStrategy


class AccessAlarmStrategyIsAlarmSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccessAlarmStrategy
        fields = ('is_alarm',)


class AccessAlarmStrategySerializer(serializers.ModelSerializer):
    alarm_name = serializers.CharField(help_text='监控名称',
                                       validators=[UniqueValidator(queryset=AccessAlarmStrategy.objects.all())],
                                       required=True)
    where_condition = serializers.JSONField(
        help_text='''
        {
           "http_host": "www.tokenworld.pro",
           "url": "/api.php/user/getOfficialAccount"
       }
       ''',
        required=True
    )
    alarm_strategy = serializers.JSONField(help_text='''
        {
            "strategy": "average"
        }
        {
            "strategy": "max"
        }
        {
            "strategy": "cost_percent", "percent": 0.5
        } // 策略， 花费时间(告警阀值)，占比(超过占比告警)
    ''', required=True)
    send_user_id = serializers.JSONField(help_text='''[1, 2, 3]''', required=True)
    work_order = serializers.CharField(max_length=128, help_text='独立工单号', read_only=True)
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = AccessAlarmStrategy
        fields = '__all__'


class AccessAlarmAvgSerializer(serializers.Serializer):
    http_method = serializers.CharField(required=True, help_text='GET')
    where_condition = serializers.JSONField(
        help_text='''
            {
               "http_host": "www.tokenworld.pro",
               "url": "/api.php/user/getOfficialAccount"
           }
           ''',
        required=True
    )