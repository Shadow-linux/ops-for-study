import datetime
import json
from rest_framework import viewsets, mixins, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import permissions
from permission import perms
from .models import NativeHost
from .serializers import NativeHostSerializer
from util.rest_framwork_mixin import PureUpdateModelMixin
from ..cmdb_common.models import TagsNativeHostRel
from apps.models import AppHostRel, AppDetail
from monitor.components.falcon_api import (get_graph_data, get_endpoint_counter)
from public.util.libs import (timestamp2format_time, LOCAL_FORMAT)
from .filters import MonitorNativeHostGraphFilter, MonitorNativeHostGraphCounterFilter


class NativeHostViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        PureUpdateModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """
    list:
        获取所有本地服务器的信息
    retrieve:
        获取单个服务器的信息
    update:
        更新本地服务器单个实例的信息
    create:
        创建本地服务器实例信息
    destroy:
        删除单个实例的信息
    """
    queryset = NativeHost.objects.all()
    serializer_class = NativeHostSerializer
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # 删除关联的Tag
        TagsNativeHostRel.objects.filter(target_id=instance.id).delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class NativeClassifyViewSet(mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """
    list:
        本地服务器搜索 ('idc', 'environment)
    """
    queryset = NativeHost.objects.all()
    serializer_class = NativeHostSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('idc', 'environment')
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]


class NativeHostAppsRelViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    retrieve:
        获取单个主机 关联的App
    """
    queryset = AppHostRel.objects.all()
    lookup_field = 'host_id'

    def retrieve(self, request, *args, **kwargs):
        host_id = kwargs.get('host_id')
        app_model_obj_list = AppDetail.objects.filter(id__in=[
            ah_rel_obj.app_id
            for ah_rel_obj in AppHostRel.objects.filter(host_id=host_id, owner='native')
        ])
        return Response([
            {
                'id': model_obj.id,
                'app_name': model_obj.app_name,
                'is_active': model_obj.is_active
            }
            for model_obj in app_model_obj_list
        ])


class NativeHostGraphCounterViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取open-falcon [net|disk] counter
    """
    filter_class = MonitorNativeHostGraphCounterFilter

    def list(self, request, *args, **kwargs):
        data = request.query_params
        hostname, counter = data['hostname'], data['counter']
        counter_list = get_endpoint_counter(hostname, counter)
        return Response(data=counter_list, status=status.HTTP_200_OK)


class NativeHostGraphViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取 native host 监控图  (该方法还没对接前端，后续维护者，可以使用其来做前端监控信息) by Shadow-YD
    """
    filter_class = MonitorNativeHostGraphFilter

    def list(self, request, *args, **kwargs):
        data = request.query_params
        counter, hostname, hours = data['counter'], data['hostname'], int(data['hours'])
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(hours=hours)
        graph_data = get_graph_data(start_time, end_time, json.loads(hostname), [f"{counter}"], 60)
        ret_data = {
            'time': [timestamp2format_time(item['timestamp'], LOCAL_FORMAT) for item in graph_data[0]['Values']],
            'data': [
                {
                    'ep': graph['endpoint'],
                    'values': [item['value'] for item in graph['Values']]
                }
                for graph in graph_data
            ]
        }
        return Response(ret_data)
