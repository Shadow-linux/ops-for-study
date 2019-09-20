from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from .components.third_party import save_third_party_data, push_status_graph_notice, push_graph_jitter_notice

class TestThirdPartySaveDataViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        测试 第三方监控保存数据接口
    """

    def list(self, request, *args, **kwargs):
        save_third_party_data()
        return Response({'code': 0})


class TestPushDataToFalcon(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        测试 第三方监控数据推送到falcon
    """
    def list(self, request, *args, **kwargs):
        push_status_graph_notice()
        return Response({'code': 0})


class TestTPPushJitterData(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        测试 第三方监 抖动数据告警
    """
    def list(self, request, *args, **kwargs):
        push_graph_jitter_notice()
        return Response({'code': 0})
