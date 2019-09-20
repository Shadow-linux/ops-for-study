# coding: utf-8

import json
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import CheckPermissionPageSerializer, PermissionSerializer
from .filters import CheckPagePermissionFilter
from .models import PermissionAll
from users.models import UsersAccount
from util import jwt, rest_framwork_mixin
from . import perms


# Create your views here.


class CheckPagePermissionCheckViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        检测页面权限
    """
    queryset = PermissionAll.objects.all()
    serializer_class = CheckPermissionPageSerializer
    filter_class = CheckPagePermissionFilter

    def list(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        user_info = jwt.parseJWT(token)
        user_obj = UsersAccount.objects.get(id=user_info['user_id'])
        if not user_obj.groups.all():
            # 默认使用第一个权限组的页面权限
            queryset = PermissionAll.objects.get(group_id=1)
            allow_page_list = self.allow_page_list(queryset)
        else:
            queryset = PermissionAll.objects.get(group_id=user_obj.groups.first().id)
            allow_page_list = self.allow_page_list(queryset)
        return Response({'access': allow_page_list, 'user_id': user_obj.id, 'username': user_obj.username}, status=200)

    def allow_page_list(self, queryset: object) -> list:
        serializer = self.get_serializer(queryset)
        allow_list = []
        for key, value in serializer.data['page_permission'].items():
            if value != 0:
                allow_list.append(key)
        return allow_list


class PermissionGroupViewSet(mixins.RetrieveModelMixin,
                             mixins.DestroyModelMixin,
                             rest_framwork_mixin.PureUpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    retrieve:
        获取用户组权限
    update:
        更新用户组权限
    destroy:
        删除用户组权限
    """
    queryset = PermissionAll.objects.all()
    serializer_class = PermissionSerializer
    lookup_field = 'group_id'
    permission_classes = (permissions.IsAuthenticated, perms.IsSuperUser, perms.IsPagePermissionRW)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'group_id': instance.group_id,
            'page_permission': json.loads(serializer.data['page_permission'])
        })

# class PermissionPagePermShowViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
#     """
#         页面权限前端展示数据
#     """
#     queryset = Permission.objects.all()
#     serializer_class = PermissionSerializer
#     lookup_field = 'group_id'
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         page_perm_dict = json.loads(serializer.data['page_permission'])
#         for name, value in page_perm_dict.items():
#
#
#         return Response(serializer.data)
