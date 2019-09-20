from rest_framework import views
from rest_framework.response import Response
from .send_message import sender


class TestSenderView(views.APIView):
    """
    get:
        测试sender接口
    """
    def get(self, request):
        sender('hello',
               'worldworldworldworldworldworldworld',
               [1, ],
               level='INFO',
               send_type='inner'
               )
        return Response({'code': 0})
