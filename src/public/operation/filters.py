import datetime
import django_filters
from .models import OperationGlobalLog


class CheckPagePermissionFilter(django_filters.rest_framework.FilterSet):
    user = django_filters.CharFilter(field_name='user', required=False, help_text='用户名')
    method = django_filters.CharFilter(field_name='method', required=False, help_text='HTTP 方法')
    select_date = django_filters.CharFilter(method='select_date_filter', required=False, help_text='日期范围')
    data = django_filters.CharFilter(method='data_filter', required=False, help_text='提交的数据')

    def select_date_filter(self, queryset, name, value: str):
        start_date, end_date = value.split(',')
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        return queryset.filter(time__gte=start_date).filter(time__lte=end_date)

    def data_filter(self, queryset, name, value: str):
        return queryset.filter(data__contains=value)

    class Meta:
        model = OperationGlobalLog
        fields = ['user', 'method', 'select_date', 'data']


class GLobalSearchFilter(django_filters.rest_framework.FilterSet):
    sval = django_filters.CharFilter(method='return_sval', required=True, help_text='搜索内容')

    def return_sval(self, queryset, name, value: str):
        return queryset

    class Meta:
        model = OperationGlobalLog
        fields = ['sval']
