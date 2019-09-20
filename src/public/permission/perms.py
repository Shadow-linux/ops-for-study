# coding: utf-8

"""
用户权限相关的公用模块
"""

import json
import hashlib
from rest_framework import permissions
from .models import PermissionAll
from code_publish.models import CodePublishLockEnv, CodePublishLockEnvApp, CodePublishMainConf

# 数据格式
#   key 格式: level1_level2_level3
#   value: 0 是不具有权限，1 只读， 2 读写
PAGE_PERMS_TEMPLATE = {
    # 首页 ----
    'home': 1,
    # CMDB ---
    'cmdb': 0,
    'cmdb_aliyun_resource': 0,
    'cmdb_aliyun_monitor': 0,
    'cmdb_native_resource': 0,
    'cmdb_native_monitor': 0,
    'cmdb_tag': 0,
    # APP ---
    'app': 0,
    'app_management': 0,
    'app_aliveMonitor': 0,
    # 代码发布 ---
    'code_publish': 0,
    'code_publish_issue': 0,
    'code_publish_config': 0,
    'code_publish_template': 0,
    # 监控中心 ----
    'monitor': 0,
    'monitor_thirdParty': 0,
    'monitor_docker': 0,
    'monitor_business_apiQuality': 0,
    'monitor_kibana_preAccessNginx': 0,
    # 审计 ----
    'audit': 0,
    'audit_operationLog': 0,
    'audit_messageLog': 0,
    # 全局设置 ----
    'setting': 0,
    'setting_user': 0,
    'setting_permissionGroup': 0,
    'setting_sendMessage': 0,
    'setting_commonSetting': 0,
}


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    属主或者只读权限, 需要查找对象中有user_id 字段，或重写该方法
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            return int(obj.user_id) == request.user.id
        except AttributeError:
            # 这是用于users_account
            return obj.id == request.user.id


class IsPagePermissionRW(permissions.BasePermission):
    """
    是否具有页面读写权限, 通过header 的 pp值来判断
    """
    def has_permission(self, request, view):
        # 特殊请求会在http_method, 这种特殊请求是以POST 代替 GET，大多数要传送比较多的数据上来
        if request.method in permissions.SAFE_METHODS or request.data.get('http_method', None) == 'GET':
            return True
        pp = request.META.get('HTTP_PP')
        group_obj = request.user.groups.first()
        if group_obj:
            perm_obj = PermissionAll.objects.get(group_id=group_obj.id)
            md5_page_perm_dict = {}
            page_perm_dict = json.loads(perm_obj.page_permission)
            for key, item in page_perm_dict.items():
                m2 = hashlib.md5()
                m2.update(key.encode())
                md5_page_perm_dict[m2.hexdigest()] = item
            if md5_page_perm_dict.get(pp, None) == 2:
                return True
        return False


class IsSuperUser(permissions.BasePermission):
    """
    是否具有super user 权限
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsPublishCode(permissions.BasePermission):
    """
    是否具有发布某个应用的权限
    """
    def __get_app_id(self, app_name, env):
        try:
            model_obj = CodePublishMainConf.objects.get(app_name=app_name, env=env)
            return model_obj.id
        except Exception:
            return 0

    def has_permission(self, request, view):
        # 获取main conf 中的 app_id
        if request.method in ('GET', 'HEAD', 'OPTIONS', 'DELETE'):
            return True

        app_id = self.__get_app_id(request.data.get('app_name'), request.data.get('env'))
        if not app_id:
            return False

        # 如果app_id 不存 在 CodePublishLockEnvApp 中，则可以直接发布
        if not CodePublishLockEnvApp.objects.filter(app_name_id=app_id):
            return True

        user_id = request.user.id
        for model_obj in CodePublishLockEnv.objects.all():
            if user_id in json.loads(model_obj.user_ids) or user_id == model_obj.creator:
                if app_id in json.loads(model_obj.app_ids):
                    return True
        return False


class IsReleaseEnvLock(permissions.BasePermission):
    """
    是否具有释放环境锁的权限
    """
    def has_permission(self, request, view):
        user_id = request.user.id
        lock_grp_id = view.kwargs['pk']
        model_obj = CodePublishLockEnv.objects.get(id=lock_grp_id)
        if user_id == model_obj.creator or request.user.is_superuser:
            return True
        return False
