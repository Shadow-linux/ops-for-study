import json
from rest_framework import serializers
from .models import PermissionAll


class CheckPermissionPageSerializer(serializers.ModelSerializer):
    page_permission = serializers.SerializerMethodField(
        method_name='return_page_permission',
        help_text='页面权限'
    )

    def return_page_permission(self, obj) -> object:
        return json.loads(obj.page_permission)

    class Meta:
        model = PermissionAll
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PermissionAll
        fields = ('page_permission', 'id')
