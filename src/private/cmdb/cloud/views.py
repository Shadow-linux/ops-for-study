"""
aliyun 接口都在该文件下
"""
import json
import datetime
from rest_framework import viewsets, mixins, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework import permissions
from permission import perms
from .models import AliyunKeys, AliyunEcs, AliyunRDS
from ..cmdb_common.models import TagsAliyunEcsRel
from .serializers import (
    AliyunKeysSerializer,
    AliyunPureKeysSerializer,
    AliyunEcsAutoSerializer,
    AliyunEcsUpdateSerializer,
    AliyunEcsSerializer,
    AliyunKeys2Serializer,
    AliyunRdsSerializer
)
from .aliyun.libs import generate_aliyun_ecs
from .aliyun.api import get_aliyun_resource
from .filters import AliyunGraphFilter, AliyunKey2ECsFilter, AliyunRdsGraphFilter, AliyunKey2RdsFilter
from apps.models import AppHostRel, AppDetail
from public.util.libs import get_logger, local2utc, UTC_FORMAT_NO_SEC, utc2local, E_CHARTS_FORMAT, UTC_FORMAT_FULL
from public.util import rest_framwork_mixin


logger = get_logger('aliyun.views')


# -------------------- 阿里云 --------------------
class AliyunKeyViewSet(mixins.ListModelMixin,
                       rest_framwork_mixin.PureUpdateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    """
    list:
        获取 aliyun access keys 信息
    update:
        更新 aliyun access key的部分或所有信息
    delete:
        删除 aliyun access key 信息
    create:
        添加 aliyun access key 信息
    """
    queryset = AliyunKeys.objects.all()
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def get_serializer_class(self):
        if self.action == 'update':
            return AliyunKeys2Serializer
        return AliyunKeysSerializer


class AliyunECSViewSet(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       rest_framwork_mixin.PureUpdateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    """
    list:
        获取已记录的阿里云ECS信息
    update:
        更新已记录的阿里云ECS信息
    retrieve:
        获取单条阿里云ecs记录
    destroy:
        删除单条阿里云ecs记录
    create:
        手动添加阿里云ecs记录
    """
    queryset = AliyunEcs.objects.all()
    serializer_class = AliyunEcsSerializer
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        TagsAliyunEcsRel.objects.filter(target_id=instance.id).delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class AliyunEcsAutoViewSet(mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    """
    create:
        自动更新或添加阿里云ECS信息 (使用阿里云API)
    """
    serializer_class = AliyunEcsAutoSerializer
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def create(self, request, *args, **kwargs):
        logger.info('自动更新或添加阿里云ECS信息')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        aliyun_key_obj = AliyunKeys.objects.get(key_name=serializer.validated_data['key_name'])
        ecs_list = generate_aliyun_ecs(
            aliyun_key_obj.id,
            aliyun_key_obj.access_key,
            aliyun_key_obj.access_secret,
            aliyun_key_obj.region_id
        )
        for data in ecs_list:
            try:
                try:
                    ecs_obj = AliyunEcs.objects.get(instance_id=data['instance_id'])
                    update_serializer = AliyunEcsUpdateSerializer(ecs_obj, data=data)
                except Exception:
                    update_serializer = AliyunEcsUpdateSerializer(data=data)
                update_serializer.is_valid(raise_exception=True)
                update_serializer.save()
            except Exception as e:
                logger.error(f'''阿里云更新 {data['instance_id']} 失败''')
                logger.exception(e)
        return Response({'code': 0})


class AliyunEcsClassfiyViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        阿里云 ecs 分类获取 ('environment', 'ac_key_id')
    """
    queryset = AliyunEcs.objects.all()
    serializer_class = AliyunEcsSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('=environment', '=ac_key_id')
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]


class AliyunGraphViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    retrieve:
        获取 阿里云ecs graph 数据
    """
    queryset = AliyunKeys.objects.all()
    serializer_class = AliyunPureKeysSerializer
    lookup_field = 'key_name'
    filter_class = AliyunGraphFilter
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def retrieve(self, request, *args, **kwargs):
        aliyun_key_obj = self.get_object()
        serializer = self.get_serializer(aliyun_key_obj)
        graph_list = get_aliyun_resource(
            access_key=serializer.data['access_key'],
            access_secret=serializer.data['access_secret'],
            region_id=serializer.data['region_id'],
            resource=request.query_params['action'],
            kwargs=json.loads(request.query_params['kwargs'])
        )
        return Response(graph_list)


class AliyunKey2ECsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        通过access key 获取ecs列表
    """
    queryset = AliyunEcs.objects.all()
    serializer_class = AliyunEcsSerializer
    filter_class = AliyunKey2ECsFilter
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]


class AliyunKey2RdsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        通过access key 获取ecs列表
    """
    queryset = AliyunRDS.objects.all()
    serializer_class = AliyunRdsSerializer
    filter_class = AliyunKey2RdsFilter
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]


class AliyunRdsClassfiyViewSet(mixins.ListModelMixin,
                               mixins.UpdateModelMixin,
                               viewsets.GenericViewSet):
    """
    list:
        阿里云 RDS 分类获取 ('environment', 'ac_key_id')
    update:
        修改阿里云 RDS 信息
    """
    queryset = AliyunRDS.objects.all()
    serializer_class = AliyunRdsSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('=environment', '=ac_key_id')
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]


class AliyunRdsProcessListViewSet(mixins.RetrieveModelMixin,
                                  viewsets.GenericViewSet):
    """
    retrieve:
        获取aliyun rds 实时 Process list
    """
    queryset = AliyunRDS.objects.all()
    serializer_class = AliyunRdsSerializer
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        aliyu_key_obj = AliyunKeys.objects.get(id=serializer.data['ac_key_id'])
        res = get_aliyun_resource(
            access_key=aliyu_key_obj.access_key,
            access_secret=aliyu_key_obj.access_secret,
            region_id=aliyu_key_obj.region_id,
            resource='rds_process_list',
            kwargs={'db_instance_id': serializer.data['instance_id']}
        )
        return Response(data=res, status=status.HTTP_200_OK)


class AliyunEcsAppRelViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
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
            for ah_rel_obj in AppHostRel.objects.filter(host_id=host_id, owner='aliyun')
        ])
        return Response([
            {
                'id': model_obj.id,
                'app_name': model_obj.app_name,
                'is_active': model_obj.is_active
            }
            for model_obj in app_model_obj_list
        ])


class AliyunRdsGraphViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    retrieve:
        获取 RDS 监控图表信息
    """
    queryset = AliyunRDS.objects.all()
    serializer_class = AliyunRdsSerializer
    filter_class = AliyunRdsGraphFilter

    def retrieve(self, request, *args, **kwargs):
        def format_time(time_str: str) -> str:
            utc_time_obj = local2utc(datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M'))
            return utc_time_obj.strftime(UTC_FORMAT_NO_SEC)

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance_id = serializer.data['instance_id']
        metric_name = request.query_params['metric_name']
        start_time = format_time(request.query_params['start_time'])
        end_time = format_time(request.query_params['end_time'])
        aliyu_key_obj = AliyunKeys.objects.get(id=serializer.data['ac_key_id'])
        res = get_aliyun_resource(
            access_key=aliyu_key_obj.access_key,
            access_secret=aliyu_key_obj.access_secret,
            region_id=aliyu_key_obj.region_id,
            resource='rds_graph',
            kwargs={
                'metric_name': metric_name,
                'db_instance_id': instance_id,
                'start_time': start_time,
                'end_time': end_time
            }
        )
        res_data = [{
            "value": item["Value"],
            "date": utc2local(datetime.datetime.strptime(item["Date"], UTC_FORMAT_FULL)).strftime(E_CHARTS_FORMAT)
        } for item in res]
        return Response(data=res_data, status=status.HTTP_200_OK)
