from django_filters import  rest_framework as filters
from .models import TagsNativeHostRel


class TagsNativeHostRelFB(filters.DjangoFilterBackend):
    def get_filterset_class(self, view, queryset=None):
        if view.action == 'list':
            return TagsNativeHostRelFilter


class TagsNativeHostRelFilter(filters.FilterSet):
    target_id = filters.NumberFilter(help_text='int; 目标id', required=True)

    class Meta:
        model = TagsNativeHostRel
        fields = ['target_id']
