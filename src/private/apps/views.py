import json
from urllib.parse import urljoin
from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework import permissions
from permission import perms
from public.util import rest_framwork_mixin, call_mysql
from public.util.libs import get_logger, local_mysql_conf
from .models import AppDetail, AppHostRel, AppConnectorRel
from cmdb.cloud.models import AliyunEcs
from cmdb.native.models import NativeHost
from .serializers import AppDetailSerializer, AppHostRelSerializer, AppAliveUrlookerSerializer
from .libs import get_app_rel_host
from .sql import (
    create_urlooker_app_alive,
    update_urlooker_app_alive,
    delete_urlooker_app_alive,
    select_urlooker_app_alive,
    select_urlooker)
from monitor.components.falcon_api import del_endpoint_to_graph


logger = get_logger('apps.view')

# Create your views here.


class AppDetailViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.CreateModelMixin,
                       rest_framwork_mixin.PureUpdateModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):
    """
    list:
        获取所有 app 详情列表
    retrieve:
        获取单个 app 详情
    create:
        创建 app
    update:
        更新 app
    destroy:
        删除 app
    """
    queryset = AppDetail.objects.all()
    serializer_class = AppDetailSerializer
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def __handle_rel(self, app_id, data):
        # 建立app 与 user 关系
        connector = data['connector']
        AppConnectorRel.objects.filter(app_id=app_id).delete()
        for conn_id in connector:
            model_obj = AppConnectorRel()
            model_obj.user_id = conn_id
            model_obj.app_id = app_id
            model_obj.save()

        # 建立 app 与 host 关系
        hosts = data['hosts']
        AppHostRel.objects.filter(app_id=app_id).delete()
        for host in hosts:
            host_id, owner = host.split(':')
            model_obj = AppHostRel()
            model_obj.host_id = int(host_id)
            model_obj.app_id = app_id
            model_obj.owner = owner
            model_obj.save()

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            self.__handle_rel(instance.id, request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        with transaction.atomic():
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            self.__handle_rel(instance.id, request.data)
            return Response(serializer.data)

    def perform_destroy(self, instance):
        with transaction.atomic():
            # 删除 与 user 和 host 的关联关系
            AppHostRel.objects.filter(app_id=instance.id).filter(Q(owner='aliyun') | Q(owner='native')).delete()
            AppConnectorRel.objects.filter(app_id=instance.id).delete()
            instance.delete()


class AppHostRelViewSet(mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """
    retrieve:
        获取单个 app 与 host 关系
    destroy：
        删除单个 app 与 host 关系
    """
    queryset = AppHostRel.objects.all()
    serializer_class = AppHostRelSerializer
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def retrieve(self, request, *args, **kwargs):
        res_data = []
        queryset = AppHostRel.objects.filter(app_id=kwargs['pk'])
        for model_obj in queryset:
            if model_obj.owner == 'aliyun':
                res_data.append((AliyunEcs.objects.get(id=model_obj.host_id), 'aliyun'))
                continue
            if model_obj.owner == 'native':
                res_data.append((NativeHost.objects.get(id=model_obj.host_id), 'native'))
                continue

        return Response([
            {
                'id': host_tuple[0].id,
                'hostname': host_tuple[0].hostname,
                'owner': host_tuple[1]
            }
            for host_tuple in res_data
        ])


# 连接至urlooker
class AppAliveUrlookerViewSet(mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              rest_framwork_mixin.PureUpdateModelMixin,
                              viewsets.GenericViewSet):
    """
    create:
        创建一个 app alive 检查
    destroy:
        删除单个 app alive 检查
    update:
        更新单个 app alive 是否告警
    """
    serializer_class = AppAliveUrlookerSerializer
    mysql_username = local_mysql_conf['username']
    mysql_password = local_mysql_conf['password']
    mysql_port = local_mysql_conf['port']
    mysql_host = local_mysql_conf['host']
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def __check_app_alive_exists(self, app_id, env) -> bool:
        sql = select_urlooker_app_alive(app_id=app_id, environment=env, select_args='id')
        with call_mysql.OpsMysqlClient(username=self.mysql_username,
                                       password=self.mysql_password,
                                       host=self.mysql_host,
                                       port=self.mysql_port,
                                       schema='urlooker') as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
        if result:
            return True
        return False

    def __get_app_alive_api(self, app_obj: AppDetail) -> list:
        insert_sql_list = []
        # 内部检测
        if app_obj.is_internal_check_api == 1:
            app_rel_host_dict = get_app_rel_host(app_obj.id)
            wait2handle_obj_list = (app_rel_host_dict['aliyun'], app_rel_host_dict['native'])
            # 判断是否是指定环境的host
            env_list = json.loads(app_obj.internal_check_api_env)
            for model_obj_list in wait2handle_obj_list:
                for model_obj in model_obj_list:
                    if model_obj.environment in env_list:
                        # 判断是否存在记录
                        if not self.__check_app_alive_exists(app_obj.id, model_obj.environment):
                            # 这里默认使用了私有IP，感觉以后还是会出问题
                            host = json.loads(model_obj.private_ip)[0]
                            insert_sql_list.append(create_urlooker_app_alive(
                                url=urljoin(f'http://{host}:{app_obj.port}', app_obj.internal_check_api),
                                ip=f'{host}',
                                app_id=app_obj.id,
                                environment=model_obj.environment,
                                idc=json.loads(app_obj.chose_agent)[model_obj.environment],
                                note=f'app-alive:{app_obj.app_name}:{model_obj.hostname}:{model_obj.environment}',
                                is_monitor=0
                            ))
        # app入口检测，外部检测 , 外部环境定义为external
        if app_obj.is_external_check_api == 1:
            if not self.__check_app_alive_exists(app_obj.id, 'external'):
                insert_sql_list.append(create_urlooker_app_alive(
                    url=app_obj.external_check_api,
                    app_id=app_obj.id,
                    # 硬编码 这是前置nginx的私有IP
                    ip='10.30.210.30',
                    environment='external',
                    idc='default',
                    note=f'app-alive:{app_obj.app_name}:external',
                    is_monitor=app_obj.is_monitor
                ))
        return insert_sql_list

    # urlooker 使用的账户: ops-admin  密码: ayg123456
    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            app_id = data['app_id']
            app_detail_obj = AppDetail.objects.get(id=app_id)
            try:
                insert_sql_list = self.__get_app_alive_api(app_detail_obj)
            except Exception as e:
                logger.exception(e)
                return Response({'detail': 'app 关联信息不完整。'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            with call_mysql.OpsMysqlClient(username=self.mysql_username,
                                           password=self.mysql_password,
                                           host=self.mysql_host,
                                           port=self.mysql_port,
                                           schema='urlooker') as cursor:
                for insert_sql in insert_sql_list:
                    cursor.execute(insert_sql)
            return Response({'code': 0}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            app_id = kwargs.get('pk')
            urlooker_id_sql = select_urlooker(app_id=app_id, select_args='id')
            with call_mysql.OpsMysqlClient(username=self.mysql_username,
                                           password=self.mysql_password,
                                           host=self.mysql_host,
                                           port=self.mysql_port,
                                           schema='urlooker') as cursor:
                cursor.execute(urlooker_id_sql)
                result_set = cursor.fetchall()
                falcon_endpoints = [f'''urlooker_{result['id']}''' for result in result_set]
            # 删除falcon graph 信息
            del_endpoint_to_graph(falcon_endpoints)
            sql_list = delete_urlooker_app_alive(app_id=app_id)
            # 删除 urlooker 信息
            with call_mysql.OpsMysqlClient(username=self.mysql_username,
                                           password=self.mysql_password,
                                           host=self.mysql_host,
                                           port=self.mysql_port,
                                           schema='urlooker') as cursor:
                for sql in sql_list:
                    cursor.execute(sql)
            return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            app_id = data.get('app_id', None)
            env = data.get('env', None)
            is_alarm = data.get('is_alarm', None)
            check_api = data.get('check_api', 0)
            sql = update_urlooker_app_alive(app_id=app_id,
                                            environment=env,
                                            check_api=check_api,
                                            update_kwargs=f'max_step = {is_alarm}')
            logger.debug(sql)
            with call_mysql.OpsMysqlClient(username=self.mysql_username,
                                           password=self.mysql_password,
                                           host=self.mysql_host,
                                           port=self.mysql_port,
                                           schema='urlooker') as cursor:
                cursor.execute(sql)
            return Response({'code': 0}, status=status.HTTP_200_OK)
