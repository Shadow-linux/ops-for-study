import json
import datetime
from django.db import transaction
from rest_framework import viewsets, mixins, status, views
from rest_framework.response import Response
from rest_framework import permissions
from permission import perms
from .models import (
    MonitorTPStrategyItemRel,
    MonitorThirdPartyStrategy,
    MonitorThirdPartyJitterStrategy,
    MonitorECS,
    MonitorYueXinSms,
    MonitorRDS,
    MonitorNAS,
    MonitorDomain,
    MonitorVPN,
    MonitorTencentSms,
    MonitorWanWeiYiYuanBankIdentity,
    MonitorXunChengEryaosu
)
from .filters import MonitorAppAliveFilter, MonitorTPGraphFilter, MonitorDockerFilter
from .components.app_alive import AppAliveGraph
from apps.models import AppDetail
from apps.sql import select_urlooker_app_alive
from .serializers import (
    MonitorAppAliveLatestDataSerializer,
    MonitorThirdPartyStrategySerializer,
    MonitorTPECSSerializer,
    MonitorTPNASSerializer,
    MonitorTPDomainSerializer,
    MonitorTPRDSSerializer,
    MonitorTPVpnSerializer,
    MonitorTPYueXinSerializer,
    MonitorTPTencentSmsSerializer,
    MonitorTPWanweiyiyuanBankIdentitySerializer,
    MonitorTPXunChengEryaosuSerializer,
    MonitorThirdPartyStrategyJitterSerializer,
)
from public.util.libs import (
    get_logger,
    datetime2timestamp,
    local_mysql_conf,
    get_work_order,
    timestamp2format_time,
    LOCAL_FORMAT)

from public.util import call_mysql
from public.util.rest_framwork_mixin import PureUpdateModelMixin
from .components.third_party.vars import (
    MONITOR_MODALS,
    MONITOR_GRAPH_ITEMS,
    THIRD_PARTY_GRAPH_PREFIX,
    MONITOR_ITEMS)

from monitor.components.falcon_api import get_graph_data
from .components.third_party import save_third_party_data
from monitor.components.falcon_api import del_endpoint_to_graph

logger = get_logger('monitor.views')


# Create your views here.


class MonitorAppAliveGraphViewSet(mixins.RetrieveModelMixin,
                                  viewsets.GenericViewSet):
    """
    retrieve:
        获取单个APP alive 12 个小时的监控信息
    """
    filter_class = MonitorAppAliveFilter
    queryset = AppDetail.objects.all()

    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        env = request.query_params.get('env')
        check_api = request.query_params.get('check_api')
        app_alive_graph_obj = AppAliveGraph(app_id=instance.id, environment=env, check_api=check_api)
        data = app_alive_graph_obj.monitor_info()
        return Response(data, status=status.HTTP_200_OK)


# 由于担心query_params 长度有限，传不了数据过来所以只能用POST 方法来代替
class MonitorAppAliveLatestDataViewSet(mixins.CreateModelMixin,
                                       viewsets.GenericViewSet):
    """
    create:
        获取App alive data 列表 (忽略权限)
    """
    queryset = AppDetail.objects.all()
    serializer_class = MonitorAppAliveLatestDataSerializer

    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data_list = json.loads(serializer.data['data'])
        ret_list = []
        print(data_list)
        for data_obj in data_list:
            with call_mysql.OpsMysqlClient(
                    username=local_mysql_conf['username'],
                    password=local_mysql_conf['password'],
                    host=local_mysql_conf['host'],
                    port=local_mysql_conf['port'],
                    schema='urlooker'
            ) as cursor:
                sql = select_urlooker_app_alive(app_id=data_obj['app_id'], environment=data_obj['env'],
                                                check_api=data_obj['check_api'], select_args='max_step')
                cursor.execute(sql)
                result = cursor.fetchone()
                if result is not None:
                    data_obj['is_alarm'] = result['max_step']
                else:
                    data_obj['is_alarm'] = 0
            try:
                app_alive_graph_obj = AppAliveGraph(app_id=data_obj['app_id'],
                                                    environment=data_obj['env'],
                                                    check_api=data_obj['check_api'],
                                                    hours=0.1)
                # 直接获取前一分钟的监控数据
                data_obj['alive_data'] = app_alive_graph_obj.monitor_info()[0]['values'][-2]
                ret_list.append(data_obj)
            except Exception as e:
                data_obj['alive_data'] = {
                    "timestamp": datetime2timestamp(),
                    "value": 2
                }
                ret_list.append(data_obj)
                logger.warning('获取最新app alive 监控数据错误')
                logger.exception(e)
        """ret_dict 数据格式
        {
            "1000": {
                "timestamp": 1557222000,
                "value": 0
            },
            ...
        }
        """
        return Response(ret_list)


# 使用post的理由同上
class MonitorAppAliveTactics(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
        统计 app alive [成功，失败，不可达] (忽略权限)
    """
    queryset = AppDetail.objects.all()
    serializer_class = MonitorAppAliveLatestDataSerializer
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def create(self, request, *args, **kwargs):
        # 成功，失败，不可达
        ret_list = {
            'success': 0,
            'failed': 0,
            'unreachable': 0,
        }
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data_list = json.loads(serializer.data['data'])
        for data_obj in data_list:
            try:
                app_alive_graph_obj = AppAliveGraph(app_id=data_obj['app_id'],
                                                    environment=data_obj['env'],
                                                    check_api=data_obj['check_api'],
                                                    hours=0.1)
                # 直接获取前一分钟的监控数据
                try:
                    num = app_alive_graph_obj.monitor_info()[0]['values'][-2]['value']
                except Exception:
                    # 无效number
                    num = 2
                if num == 0:
                    ret_list['success'] += 1
                elif num == 1:
                    ret_list['failed'] += 1
                else:
                    ret_list['unreachable'] += 1

            except Exception as e:
                logger.error('获取最新app alive 监控数据错误')
                logger.exception(e)

        return Response(ret_list)


class MonitorThirdPartyStrategyViewSet(mixins.CreateModelMixin,
                                       mixins.DestroyModelMixin,
                                       mixins.ListModelMixin,
                                       PureUpdateModelMixin,
                                       viewsets.GenericViewSet):
    """
    list:
        获取第三方监控策略
    update:
        更新第三方监控策略
    create:
        创建第三方监控策略
    destroy:
        删除第三方监控策略
    """
    queryset = MonitorThirdPartyStrategy.objects.all()
    serializer_class = MonitorThirdPartyStrategySerializer
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    # 建立策略与数据告警关系
    def __create_strategy_alarm_rel(self, monitor_item, strategy_id):
        try:
            monitor_modal = MONITOR_MODALS[monitor_item]
            for m_obj in monitor_modal.objects.all():
                MonitorTPStrategyItemRel.objects.get_or_create(
                    monitor_item=monitor_item,
                    monitor_item_id=m_obj.id,
                    strategy_id=strategy_id
                )
        except Exception as e:
            logger.exception(e)
            raise e

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['work_order'] = get_work_order('third_party')
            model_obj = serializer.save()
            self.__create_strategy_alarm_rel(serializer.validated_data['monitor_item'], model_obj.id)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        monitor_item = serializer.validated_data['monitor_item']
        model_obj = serializer.save()
        self.__create_strategy_alarm_rel(serializer.validated_data['monitor_item'], model_obj.id)


    def destroy(self, request, *args, **kwargs):
        with transaction.atomic():
            instance = self.get_object()
            MonitorTPStrategyItemRel.objects.filter(monitor_item=instance.monitor_item, strategy_id=instance.id).delete()
            self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class MonitorThirdPartyJitterStrategyViewSet(mixins.CreateModelMixin,
                                             mixins.ListModelMixin,
                                             mixins.DestroyModelMixin,
                                             PureUpdateModelMixin,
                                             viewsets.GenericViewSet):
    """
    list:
        获取第三方监控数值抖动策略
    update:
        更新第三方监控数值抖动策略
    create:
        创建第三方监控数值抖动策略
    destroy:
        删除第三方监控数值抖动策略
    """
    queryset = MonitorThirdPartyJitterStrategy.objects.all()
    serializer_class = MonitorThirdPartyStrategyJitterSerializer
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['work_order'] = get_work_order('third_party')
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MonitorTPECSViewSet(mixins.ListModelMixin,
                          mixins.DestroyModelMixin,
                          PureUpdateModelMixin,
                          viewsets.GenericViewSet):
    """
    list:
        获取ecs 第三方监控信息
    destroy:
        删除 ecs 第三方监控信息
    update:
        更新 ecs 第三方监控信息 是否监控
    """
    serializer_class = MonitorTPECSSerializer
    queryset = MonitorECS.objects.all()
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]


class MonitorTPRDSViewSet(mixins.ListModelMixin,
                          mixins.DestroyModelMixin,
                          PureUpdateModelMixin,
                          viewsets.GenericViewSet):
    """
    list:
        获取 rds 第三方监控信息
    destroy:
        删除 rds 第三方监控信息
    update:
        更新 rds 第三方监控信息 是否监控
    """
    serializer_class = MonitorTPRDSSerializer
    queryset = MonitorRDS.objects.all()
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]


class MonitorTPNASViewSet(mixins.ListModelMixin,
                          mixins.DestroyModelMixin,
                          PureUpdateModelMixin,
                          viewsets.GenericViewSet):
    """
    list:
        获取 nas 第三方监控信息
    destroy:
        删除 nas 第三方监控信息
    update:
        更新 nas 第三方监控信息 是否监控
    """
    serializer_class = MonitorTPNASSerializer
    queryset = MonitorNAS.objects.all()
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]


class MonitorTPDomainViewSet(mixins.ListModelMixin,
                             mixins.DestroyModelMixin,
                             PureUpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    list:
        获取 domain 第三方监控信息
    destroy:
        删除 domain 第三方监控信息
    update:
        更新 domain 第三方监控信息 是否监控
    """
    serializer_class = MonitorTPDomainSerializer
    queryset = MonitorDomain.objects.all()
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]


class MonitorTPVpnViewSet(mixins.ListModelMixin,
                          mixins.DestroyModelMixin,
                          PureUpdateModelMixin,
                          viewsets.GenericViewSet):
    """
    list:
        获取 vpn 第三方监控信息
    destroy:
        删除 vpn 第三方监控信息
    update:
        更新 vpn 第三方监控信息 是否监控
    """
    serializer_class = MonitorTPVpnSerializer
    queryset = MonitorVPN.objects.all()
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]


class MonitorTPYueXinSmsViewSet(mixins.ListModelMixin,
                                mixins.DestroyModelMixin,
                                PureUpdateModelMixin,
                                viewsets.GenericViewSet):
    """
    list:
        获取 yuexin 短信 第三方监控信息
    destroy:
        删除 yuexin 第三方监控信息
    update:
        更新 yuexin 第三方监控信息 是否监控
    """
    serializer_class = MonitorTPYueXinSerializer
    queryset = MonitorYueXinSms.objects.all()
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def perform_destroy(self, instance):
        del_endpoint_to_graph(f"{THIRD_PARTY_GRAPH_PREFIX}_{instance.work_order}")
        instance.delete()


class MonitorTPXunChengEryaosuViewSet(mixins.ListModelMixin,
                                      mixins.DestroyModelMixin,
                                      PureUpdateModelMixin,
                                      viewsets.GenericViewSet):
    """
    list:
        获取 寻程二要素 第三方监控信息
    destroy:
        删除 寻程二要素 第三方监控信息
    update:
        更新 寻程二要素 第三方监控信息 是否监控
    """
    queryset = MonitorXunChengEryaosu.objects.all()
    serializer_class = MonitorTPXunChengEryaosuSerializer
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def perform_destroy(self, instance):
        del_endpoint_to_graph(f"{THIRD_PARTY_GRAPH_PREFIX}_{instance.work_order}")
        instance.delete()


class MonitorTPWanweiyiyuanBankIdentityViewSet(mixins.ListModelMixin,
                                               mixins.DestroyModelMixin,
                                               PureUpdateModelMixin,
                                               viewsets.GenericViewSet):
    """
    list:
        获取 万维易源 银行卡身份证实名认证 第三方监控信息
    destroy:
        删除 万维易源 银行卡身份证实名认证  第三方监控信息
    update:
        更新 万维易源 银行卡身份证实名认证 第三方监控信息 是否监控
    """
    queryset = MonitorWanWeiYiYuanBankIdentity.objects.all()
    serializer_class = MonitorTPWanweiyiyuanBankIdentitySerializer
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def perform_destroy(self, instance):
        del_endpoint_to_graph(f"{THIRD_PARTY_GRAPH_PREFIX}_{instance.work_order}")
        instance.delete()


class MonitorTPTencentSmsViewSet(mixins.ListModelMixin,
                                 mixins.DestroyModelMixin,
                                 PureUpdateModelMixin,
                                 viewsets.GenericViewSet):
    """
    list:
        获取 腾讯 短信 第三方监控信息
    destroy:
        获取 腾讯 短信 第三方监控信息
    update:
        更新 腾讯 短信 第三方监控信息 是否监控
    """
    queryset = MonitorTencentSms.objects.all()
    serializer_class = MonitorTPTencentSmsSerializer
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def perform_destroy(self, instance):
        del_endpoint_to_graph(f"{THIRD_PARTY_GRAPH_PREFIX}_{instance.work_order}")
        instance.delete()


class MonitorUpdateTPView(views.APIView):
    """
    put:
        更新本地第三方监控信息, 不推送到falcon
    """
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def put(self, request, *args, **kwargs):
        save_third_party_data()
        return Response({'code': 0}, status=status.HTTP_200_OK)


class MonitorTPBaseStrategyItemView(views.APIView):
    """
    get:
        获取第三方基础监控项目
    """
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def get(self, request, *args, **kwargs):
        return Response(MONITOR_ITEMS)


class MonitorTPJitterStrategyItemView(views.APIView):
    """
    get:
        获取第三方抖动监控项目
    """
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def get(self, request, *args, **kwargs):
        return Response(MONITOR_GRAPH_ITEMS)


class MonitorTPGraphViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取第三方监控图表信息
    """
    filter_class = MonitorTPGraphFilter
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def list(self, request, *args, **kwargs):
        data = request.query_params
        item_id = data['id']
        monitor_item = data['monitor_item']
        days = data['days']
        if monitor_item in MONITOR_GRAPH_ITEMS:
            monitor_item_modal = MONITOR_MODALS[monitor_item]
            monitor_item_modal_obj = monitor_item_modal.objects.get(id=item_id)
            start_time, end_time = self.handle_days(days)
            counter = f"value/item={monitor_item},item_id={monitor_item_modal_obj.id}"
            ep = f"{THIRD_PARTY_GRAPH_PREFIX}_{monitor_item_modal_obj.work_order}"
            return Response(get_graph_data(start_time, end_time, [ep], [counter], 3600)[0]['Values'])
        return Response([])

    def handle_days(self, days: int):
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(days=int(days))
        return start_time, end_time


class MonitorDockerAppGraphViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    获取 docker app 监控图
    """
    filter_class = MonitorDockerFilter

    def list(self, request, *args, **kwargs):
        data = request.query_params
        counter, hostname, hours = data['counter'], data['hostname'], int(data['hours'])
        end_time = datetime.datetime.now()
        start_time = end_time - datetime.timedelta(hours=hours)
        graph_data = get_graph_data(start_time, end_time, json.loads(hostname), [f"{counter}"], 60)
        ret_data = {
            'time': [timestamp2format_time(item['timestamp'], LOCAL_FORMAT) for item in graph_data[0]['Values']],
            'data': [
                {
                    'ep': graph['endpoint'],
                    'values': [item['value'] for item in  graph['Values']]
                }
                for graph in graph_data
            ]
        }
        return Response(ret_data)
