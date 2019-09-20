import datetime
import numpy
import json
from django.db import transaction
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import permissions
from permission import perms
from public.util.rest_framwork_mixin import PureUpdateModelMixin
from public.util.libs import get_work_order
from .models import AccessAlarmStrategy, AccessAlarmResult
from .serializers import AccessAlarmStrategySerializer, AccessAlarmAvgSerializer
from .vars import NGX_ACCESS_FALCON_HG, NGX_ACCESS_FALCON_PREFIX
from monitor.components.falcon_api import (
    get_grp_hosts,
    add_endpoint_to_falcon_grp,
    del_endpoint_to_falcon_grp,
    del_endpoint_to_graph,
)
from .ngx_access_alarm import (filter_cost_to_time_range, get_current_fmt_time, get_ago_fmt_time)
# Create your views here.


class AccessAlarmStrategyViewSet(mixins.CreateModelMixin,
                                 mixins.ListModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.DestroyModelMixin,
                                 viewsets.GenericViewSet):
    """
    list:
        获取所有 access alarm 策略
    update:
        更新单个 access alarm 策略
    create:
        创建一个 access alarm 策略
    destroy:
        删除一个 access alarm 策略
    """
    queryset = AccessAlarmStrategy.objects.all()
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)
    serializer_class = AccessAlarmStrategySerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            # 获取原有的 EP 然后重新添加
            endpoint_list = get_grp_hosts(NGX_ACCESS_FALCON_HG)
            serializer.validated_data['work_order'] = get_work_order(work_type=NGX_ACCESS_FALCON_PREFIX)
            endpoint_list.append(f'''{NGX_ACCESS_FALCON_PREFIX}_{serializer.validated_data['work_order']}''')
            # 都怪falcon 的奇葩接口，Hosts 每次会覆盖该HostGroup内现有的Host List (sb)
            add_endpoint_to_falcon_grp(endpoint=endpoint_list,
                                       hg='ngx.access.hg')
            serializer.save()

    def perform_destroy(self, instance):
        with transaction.atomic():
            del_endpoint_to_falcon_grp(endpoint=f'''{NGX_ACCESS_FALCON_PREFIX}_{instance.work_order}''',
                                       hg=NGX_ACCESS_FALCON_HG)
            del_endpoint_to_graph(endpoint=f'''{NGX_ACCESS_FALCON_PREFIX}_{instance.work_order}''')
            AccessAlarmResult.objects.filter(work_order=instance.work_order).delete()
            instance.delete()


class AccessAlarmAvgViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
        查询 access url 一周内的平均耗时间
    """
    serializer_class = AccessAlarmAvgSerializer
    # permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def create(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        end_time = get_current_fmt_time(now)
        # 7天前的时间
        start_time = get_ago_fmt_time(now, 1440)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        where_condition = serializer.validated_data['where_condition']
        cost_time_list = filter_cost_to_time_range(start_time, end_time, json.loads(where_condition))
        avg_num = numpy.average(cost_time_list) if cost_time_list else 0
        return Response({'avg': round(avg_num, 2)})