from django_filters import rest_framework as filters
from .models import AppDetail


class AppAliveDataFilter(filters.FilterSet):

    env = filters.CharFilter(help_text='str; 环境名', method='return_origin_queryset', required=True)

    def return_origin_queryset(self, queryset, name, value):
        return queryset

    class Meta:
        model = AppDetail
        fields = ['env']
