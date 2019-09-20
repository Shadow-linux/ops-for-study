from django_filters import rest_framework as filters
from .models import NativeHost

class MonitorNativeHostGraphFilter(filters.FilterSet):

    counter = filters.CharFilter(help_text='str; 查询的counter 名', method='return_origin_queryset', required=True)
    hours = filters.NumberFilter(help_text='int; 小时', method='return_origin_queryset', required=True)
    hostname = filters.CharFilter(help_text='str; hostname 名', method='return_origin_queryset', required=True)

    def return_origin_queryset(self, queryset, name, value):
        return queryset

    class Meta:
        model = NativeHost
        fields = ['counter', 'hostname', 'hours']


class MonitorNativeHostGraphCounterFilter(filters.FilterSet):

    counter = filters.CharFilter(help_text='str; 查询的counter 名', method='return_origin_queryset', required=True)
    hostname = filters.CharFilter(help_text='str; hostname 名', method='return_origin_queryset', required=True)

    def return_origin_queryset(self, queryset, name, value):
        return queryset

    class Meta:
        model = NativeHost
        fields = ['counter', 'hostname']