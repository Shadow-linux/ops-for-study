from rest_framework import viewsets, mixins
from rest_framework.response import Response
from .aliyun.api import get_aliyun_resource
from .models import AliyunKeys
# Create your tests here.


class TestAliyunEcsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取aliyun ecs 信息测试接口
    """

    def list(self, request, *args, **kwargs):
        aliyun_key_obj = AliyunKeys.objects.all().first()
        ecs_list = get_aliyun_resource(access_key=aliyun_key_obj.access_key,
                                       access_secret=aliyun_key_obj.access_secret,
                                       region_id=aliyun_key_obj.region_id)
        return Response(ecs_list)


class TestAliyunGraphViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        测试 获取图表数据接口
    """
    def list(self, request, *args, **kwargs):
        aliyun_key_obj = AliyunKeys.objects.all().first()
        ecs_graph_list = get_aliyun_resource(
            access_key=aliyun_key_obj.access_key,
            access_secret=aliyun_key_obj.access_secret,
            region_id=aliyun_key_obj.region_id,
            resource='disk_graph',
            kwargs={
               'disk_id': 'd-wz97bbyb81s63jfvitk0',
               'days': 1
            }
            )
        return Response(ecs_graph_list)
