from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import (OpenApiMysqlQuerySerializer, OpenApiAnsibleHostSerializer, OpenApiAliyunSLBCtrlSerializer)
from .falcon.libs import analyze_endpoint
from public.util.libs import get_logger, local_mysql_conf
from public.util import call_mysql
from cmdb.cloud.models import AliyunEcs, AliyunKeys
from cmdb.native.models import NativeHost
from cmdb.cloud.aliyun.api import get_aliyun_resource
from common.models import AnsibleHost
from apps.libs import get_app_rel_host
from apps.models import AppDetail


logger = get_logger('openapi.views')


class OpenApiFalconAlarmViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        接受 open-falcon 告警回调
    """
    def list(self, request, *args, **kwargs):
        data = request.query_params
        logger.info(f'''falcon 回调信息: {data}''')
        try:
            if not data:
                return Response(data='I am working...')
            handle_class = analyze_endpoint(data['endpoint'])
            handle_obj = handle_class(query_params=data)
            handle_obj.launch()
        except Exception as e:
            logger.error(f'`{OpenApiFalconAlarmViewSet}` 发送通知失败')
            logger.exception(e)
        return Response(data)


class OpenApiMysqlQueryViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
        接受特定schema的sql，并执行返回结果
    """
    serializer_class = OpenApiMysqlQuerySerializer
    specific_schema = ['shadow_ops', 'ops']
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if data['schema'] not in self.specific_schema:
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'detail': 'schema 不在指定的数据库中'})
        with call_mysql.OpsMysqlClient(username=local_mysql_conf['username'],
                                       password=local_mysql_conf['password'],
                                       port=local_mysql_conf['port'],
                                       host=local_mysql_conf['host'],
                                       schema=data['schema']) as cursor:
            cursor.execute(data['query'])
            result_set = cursor.fetchall()
        return Response(result_set)


class OpenApiAnsibleHostViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
        更新 ansible host，并返回新的ansible host数据
    """
    # 需要通过连接 t.iyuangong.com.cn 这个动态域名访问的环境
    dynamic_domain = 't.iyuangong.com.cn'
    serializer_class = OpenApiAnsibleHostSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        aliyun_obj_list = AliyunEcs.objects.all()
        native_obj_list = NativeHost.objects.all()
        all_host_obj_list = (aliyun_obj_list, native_obj_list)
        # 先清空后重新生成
        AnsibleHost.objects.all().delete()
        for model_obj_list in all_host_obj_list:
            for model_obj in model_obj_list:
                ansible_host_obj = AnsibleHost()
                ansible_host_obj.hostname = model_obj.hostname
                ansible_host_obj.group_name = model_obj.environment
                ansible_host_obj.host = model_obj.ssh_ip
                ansible_host_obj.ansible_user = 'root'
                ansible_host_obj.ansible_port = model_obj.ssh_port
                ansible_host_obj.var_env = model_obj.environment
                ansible_host_obj.var_domain = self.dynamic_domain
                ansible_host_obj.save()
        return Response({'code': 0}, status=status.HTTP_201_CREATED)


class OpenApiAliyunSLBCtrlViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
        更新 aliyun lbs 权重
    """

    queryset = AliyunEcs.objects.all()
    serializer_class = OpenApiAliyunSLBCtrlSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        app_obj = AppDetail.objects.get(app_name=serializer.validated_data['app_name'])
        ecs_obj_list = get_app_rel_host(app_id=app_obj.id)['aliyun']
        ecs_obj = ecs_obj_list.get(private_ip__contains=serializer.validated_data['ip'],
                                      environment=serializer.validated_data['env'])
        aliyun_key_obj = AliyunKeys.objects.get(id=ecs_obj.ac_key_id)
        try:
            res = get_aliyun_resource(
                access_key=aliyun_key_obj.access_key,
                access_secret=aliyun_key_obj.access_secret,
                region_id=aliyun_key_obj.region_id,
                resource='adjust_slb',
                kwargs= {
                    'app_name': app_obj.app_name,
                    'weight': serializer.validated_data['weight'],
                    'server_id': ecs_obj.instance_id
                }
            )
        except Exception as e:
            logger.error('调整slb 失败')
            logger.exception(e)
            res = {}
        return Response(res, status=status.HTTP_200_OK)
