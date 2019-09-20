from django_filters import rest_framework as filters
from apps.models import AppDetail
from monitor.models import MonitorThirdPartyStrategy

class MonitorAppAliveFilter(filters.FilterSet):

    env = filters.CharFilter(help_text='str; env name', method='return_origin_queryset', required=True)
    check_api = filters.CharFilter(help_text='str; check api', method='return_origin_queryset', required=True)

    def return_origin_queryset(self, queryset, name, value):
        return queryset

    class Meta:
        model = AppDetail
        fields = ['env', 'check_api']


class MonitorTPGraphFilter(filters.FilterSet):

    id = filters.NumberFilter(help_text='number; 第三方监控信息表的ID', method='return_origin_queryset', required=True)
    monitor_item = filters.CharFilter(help_text='str; 第三方监控表概要', method='return_origin_queryset', required=True)
    days = filters.NumberFilter(help_text='str; 日期', method='return_origin_queryset', required=True)

    def return_origin_queryset(self, queryset, name, value):
        return queryset

    class Meta:
        model = MonitorThirdPartyStrategy
        fields = ['id', 'monitor_item', 'days']


class MonitorDockerFilter(filters.FilterSet):

    counter = filters.CharFilter(help_text='str; 查询的counter 名', method='return_origin_queryset', required=True)
    hours = filters.NumberFilter(help_text='int; 小时', method='return_origin_queryset', required=True)
    hostname = filters.CharFilter(help_text='str; hostname 名', method='return_origin_queryset', required=True)

    def return_origin_queryset(self, queryset, name, value):
        return queryset

    class Meta:
        model = AppDetail
        fields = ['counter', 'hostname', 'hours']



