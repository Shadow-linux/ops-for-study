"""
该app，用于全局暂时不需要划分出独立app的接口
"""
import json
from django.conf import settings
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework import permissions
from permission import perms
from util.rest_framwork_mixin import PureUpdateModelMixin
from util import libs
from .models import SettingConf
from .serializers import (
    CommonSettingMessageSerializer,
    CommonSettingMessageTestSerializer,
    CommonSettingCmdbSerializer,
    CommonSettingAppSerializer,
    CommonSettingSshProxySerializer,
    CommonSettingCodePublishSerializer
)
from message import send_message
from cmdb.cloud.models import AliyunEcs
from cmdb.native.models import NativeHost
from .libs import render_ssh_config

logger = libs.get_logger('common')


class CommonSettingMessageViewSet(mixins.ListModelMixin, PureUpdateModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取消息设置信息
    update:
        更新消息设置信息
    """
    queryset = SettingConf.objects.all()
    serializer_class = CommonSettingMessageSerializer
    lookup_field = 'owner'
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        serializer.data[0]['message_setting'] = json.loads(serializer.data[0]['message_setting'])
        return Response(serializer.data)


class CommonSettingCmdbViewSet(mixins.ListModelMixin, PureUpdateModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取 cmdb_setting 设置信息
    update:
        更新 cmdb_setting 设置信息
    """
    queryset = SettingConf.objects.all()
    serializer_class = CommonSettingCmdbSerializer
    lookup_field = 'owner'
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        serializer.data[0]['cmdb_setting'] = json.loads(serializer.data[0]['cmdb_setting'])
        return Response(serializer.data)


class CommonSettingAppViewSet(mixins.ListModelMixin, PureUpdateModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取 app_setting 设置信息
    update:
        更新 app_setting 设置信息
    """
    queryset = SettingConf.objects.all()
    lookup_field = 'owner'
    serializer_class = CommonSettingAppSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        serializer.data[0]['app_setting'] = json.loads(serializer.data[0]['app_setting'])
        return Response(serializer.data)


class CommonSettingMessageTestViewSet(PureUpdateModelMixin, viewsets.GenericViewSet):
    """
    update:
        发送测试消息
    """
    serializer_class = CommonSettingMessageTestSerializer
    # 进行什么测试
    lookup_field = 'action'
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def update(self, request, *args, **kwargs):
        ta = kwargs.get('action')
        try:
            ta = eval(f'self.test_{ta}')
        except Exception:
            return Response({'detail': f'消息测试中未找到 {ta} 动作，请确认后再提交'},
                            status=status.HTTP_400_BAD_REQUEST)
        ta(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    # 测试邮件
    def test_mail(self, request):
        try:
            mail = request.data['mail_test']
            send_message.send_mail2target(
                title='Ops 测试邮件 Test Succeed',
                content='<p style="text-indent: 10px">This is a test email.</p>',
                receiver_list=[mail, ]
            )
        except Exception as e:
            logger.error('发送测试邮件失败。')
            raise e


class CommonSettingSshProxyViewSet(mixins.ListModelMixin,
                                   mixins.CreateModelMixin,
                                   viewsets.GenericViewSet):
    """
    create:
        更新需要通过ssh proxy连接的配置(如：aliyun 等云服务，需要通过跳板机代理)
    """
    serializer_class = CommonSettingSshProxySerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def list(self, request, *args, **kwargs):
        model_obj = SettingConf.objects.get(owner='global')
        data = json.loads(model_obj.cmdb_setting)['base']['ssh_proxy']
        return Response(data)

    def create(self, request, *args, **kwargs):
        idc_maps = {
            'aliyun': AliyunEcs,
            'native': NativeHost
        }
        all_model_obj_list = []
        if settings.DEPLOY_CONF.get('ssh_proxy', 'enable'):
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            for idc in json.loads(serializer.validated_data['proxy_idc']):
                model_obj_list = idc_maps[idc].objects.filter(is_active=1)
                for m_obj in model_obj_list:
                    all_model_obj_list.append(m_obj)
            render_ssh_config(all_model_obj_list)
        return Response(status=status.HTTP_201_CREATED)


class CommonSettingCodePublishViewSet(mixins.ListModelMixin,
                                      PureUpdateModelMixin,
                                      viewsets.GenericViewSet):
    """
    list:
        获取 code publish setting
    update:
        更新 code publish setting
    """
    queryset = SettingConf.objects.all()
    lookup_field = 'owner'
    serializer_class = CommonSettingCodePublishSerializer
    # permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        serializer.data[0]['code_publish_setting'] = json.loads(serializer.data[0]['code_publish_setting'])
        return Response(serializer.data)
