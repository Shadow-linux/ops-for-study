from rest_framework import views
from rest_framework.response import Response
from .ngx_access_alarm import ngx_access_launch
# Create your tests here.


class TestAccessAlarmStrategyView(views.APIView):
    """
    get:
        测试定时任务是否正常工作
    """
    def get(self, request):
        ngx_access_launch()
        return Response({'code': 0})

