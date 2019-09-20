import django_filters
from .models import PermissionAll


class CheckPagePermissionFilter(django_filters.rest_framework.FilterSet):
    token = django_filters.CharFilter(method='get_token', required=True, help_text='token')

    def get_token(self, queryset, name, value):
        return queryset

    class Meta:
        model = PermissionAll
        fields = ['token', ]
