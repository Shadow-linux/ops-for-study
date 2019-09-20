# Create your views here.
"""
记录入库的view set 都写在这里
"""
import json
import datetime
from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework import permissions
from permission import perms
from .models import OperationGlobalLog
from .serializers import GlobalOperatingLogSerializer, MessageMailLogSerializer
from .filters import CheckPagePermissionFilter, GLobalSearchFilter
from message.models import MessageMail
from cmdb.cloud.models import AliyunEcs
from cmdb.native.models import NativeHost
from apps.models import AppDetail
from apps.libs import get_app_rel_host


class GlobalOperatingLogViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取全局操作记录列表
    destroy:
        删除30天前全局操作记录
    """
    queryset = OperationGlobalLog.objects.all()
    serializer_class = GlobalOperatingLogSerializer
    filter_class = CheckPagePermissionFilter
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def destroy(self, request, *args, **kwargs):
        days_7_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        self.queryset.filter(time__lt=days_7_ago).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageMailLogViewSet(mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取 邮件消息记录列表
    destroy:
        删除30天前发送的邮件消息
    """
    queryset = MessageMail.objects.all()
    serializer_class = MessageMailLogSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def destroy(self, request, *args, **kwargs):
        days_7_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        self.queryset.filter(created__lt=days_7_ago).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GlobalSearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        全局搜索 host app
    """
    filter_class = GLobalSearchFilter
    host_modal_list = [('aliyun', AliyunEcs), ('native', NativeHost)]
    app_modal_list = (AppDetail,)

    def list(self, request, *args, **kwargs):
        def __cmdb_map(cmdb, model, sval):
            if cmdb == 'aliyun':
                return model.objects.filter(Q(hostname__contains=s_val) |
                                            Q(private_ip__contains=s_val) |
                                            Q(public_ip__contains=s_val) |
                                            Q(instance_id__contains=s_val))

            return model.objects.filter(Q(hostname__contains=s_val) |
                                        Q(private_ip__contains=s_val) |
                                        Q(public_ip__contains=s_val))

        s_val = request.query_params['sval']
        ret_dict = {
            'hosts': [],
            'apps': []
        }
        # host obj
        for cmdb, modal in self.host_modal_list:
            for host_obj in __cmdb_map(cmdb, modal, s_val):
                ret_dict['hosts'].append({
                    'id': host_obj.id,
                    'hostname': host_obj.hostname,
                    'private_ip': ",".join(json.loads(host_obj.private_ip)),
                    'public_ip': ",". join(json.loads(host_obj.public_ip)),
                    'env': host_obj.environment,
                    'is_active': host_obj.is_active,
                    'ssh_ip': host_obj.ssh_ip,
                    'ssh_port': host_obj.ssh_port,
                    'cmdb': cmdb
                })

        # app obj
        for modal_obj in self.app_modal_list:
            for app_obj in modal_obj.objects.filter(
                Q(app_name__contains=s_val) |
                Q(port__contains=s_val)):
                hosts_list = get_app_rel_host(app_obj.id)
                hosts_dict = {}
                for cmdb, host_obj_list in hosts_list.items():
                    hosts_dict[cmdb] = [
                        {
                            'id': host_obj.id,
                            'hostname': host_obj.hostname,
                            'private_ip': ",".join(json.loads(host_obj.private_ip)),
                            'public_ip': ",".join(json.loads(host_obj.public_ip)),
                            'env': host_obj.environment,
                            'cmdb': cmdb
                        }
                        for host_obj in host_obj_list
                    ]
                ret_dict['apps'].append({
                    'id': app_obj.id,
                    'app_name': app_obj.app_name,
                    'port': app_obj.port,
                    'desc': app_obj.description,
                    'is_active': app_obj.is_active,
                    'hosts_dict': hosts_dict,
                    'server': app_obj.service
                })

        return Response(ret_dict, status=status.HTTP_200_OK)
