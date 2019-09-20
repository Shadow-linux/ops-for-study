# coding: utf-8

from django_filters import rest_framework as filters
from .models import CodePublishMainConf, CodePublishWebSetting


class CodePublishMainConfFilter(filters.FilterSet):

    app_name = filters.CharFilter(method='return_query_set',
                                  required=False,
                                  help_text='str; app name')
    env = filters.CharFilter(method='return_query_set',
                             required=False,
                             help_text='str; env')

    def return_query_set(self, queryset, name, value):
        return queryset

    class Meta:
        model = CodePublishMainConf
        fields = ['app_name', 'env']


class CodePublishSetStepsFB(filters.DjangoFilterBackend):

    def get_filterset_class(self, view, queryset=None):
        if view.action == 'destroy':
            return CodePublishDeleteStepsFilter


class CodePublishDeleteStepsFilter(filters.FilterSet):

    publish_step = filters.CharFilter(method='return_query_set',
                                  required=False,
                                  help_text='str; 发布步骤')

    def return_query_set(self, queryset, name, value):
        return queryset

    class Meta:
        model = CodePublishWebSetting
        fields = ['publish_step']