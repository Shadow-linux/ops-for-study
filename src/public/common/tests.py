from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from .cron import collect_app_alive_failed_point_cron, category_app_alive_brief_cron

class TestGetAppAliveStatistics(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        测试 alive 数据收集
    """
    def list(self, request, *args, **kwargs):
        collect_app_alive_failed_point_cron()
        return Response(data={'code': 0}, status=status.HTTP_200_OK)

