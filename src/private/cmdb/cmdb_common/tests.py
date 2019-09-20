from rest_framework import viewsets, mixins
from rest_framework.response import Response
from .cron import ansible_host_update_status_cron, aliyun_ecs_update_cron, aliyun_rds_update_cron


class TestAnsibleUpdateCron(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        测试 ansible 更新主机状态（定时任务）
    """
    def list(self, request, *args, **kwargs):
        ansible_host_update_status_cron()
        return Response({'code': 0})


class TestAliyunUpdateCron(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        测试 aliyun 更新主机状态（定时任务）
    """
    def list(self, request, *args, **kwargs):
        aliyun_rds_update_cron()
        return Response({'code': 0})