# coding: utf-8
"""
用户相关
"""
import json
from django.contrib.auth import authenticate
from django.utils import timezone
from django.contrib.auth.models import Group
from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions
from .serializers import (
    UsersRegisterSerializer,
    UsersLoginSerializer,
    UsersOperationsSerializer,
    UsersChangePasswordSerializer,
    UsersGroupSerializer,
    UsersAddSerializer,
    PersonalInfoSerializer,
    PersonalChangePasswordSerializer,
)
from .models import UsersAccount
from permission import perms
from permission.models import PermissionAll
from public.util import libs, rest_framwork_mixin
from message.send_message import sender
from apps.models import AppConnectorRel
from activity.business.models import AccessAlarmStrategy
from monitor.models import MonitorThirdPartyStrategy

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Create your views here.

logger = libs.get_logger('users')


class UsersRegisterViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
        用户注册
    """
    serializer_class = UsersRegisterSerializer
    queryset = UsersAccount.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.data
        del data['password']
        return Response(data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        user_data = serializer.data
        user = UsersAccount.objects.create_user(
            username=user_data['username'],
            password=user_data['password'],
            department=user_data['department'],
            email=user_data['email'],
            real_name=user_data['real_name'],
            position=user_data['position'],
            mobile=user_data['mobile']
        )
        self.notice_admin_when_register(user)
        # 默认分配到guest权限组
        user.groups.add(Group.objects.get(name='guest'))

    def notice_admin_when_register(self, user):
        username = user.username
        real_name = user.real_name
        password = user.password

        title = 'Ops 消息, 新用户注册'
        # 邮件消息
        mail_message = f'''
管理员 您好，请处理新用户权限:<br>
新用户信息：<br>
&nbsp;&nbsp;&nbsp;&nbsp;用户：{user.username} <br>
&nbsp;&nbsp;&nbsp;&nbsp;真实姓名：{user.real_name} <br>
&nbsp;&nbsp;&nbsp;&nbsp;部门：{user.department} <br>
&nbsp;&nbsp;&nbsp;&nbsp;岗位: {user.position} <br>
&nbsp;&nbsp;&nbsp;&nbsp;Email: {user.email} <br>
&nbsp;&nbsp;&nbsp;&nbsp;Mobile: {user.mobile} <br>
<br>
地址： <a href="http://new-ops.aiyuangong.com/#/setting/user">http://new-ops.aiyuangong.com/#/setting/user</a>
                '''
        user_obj_list = UsersAccount.objects.filter(is_superuser=1)
        sender(title, mail_message, [user_obj.id for user_obj in user_obj_list], send_type='mail', level='INFO')


class UsersLoginViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    create：
        用户登录
    """
    queryset = UsersAccount.objects.all()
    serializer_class = UsersLoginSerializer

    # 该方法未完成
    def login_position_check(self, instance, request):
        """
        对比最近3次登录地址是否一致
        :param instance: user obj
        :param request: request
        :return:  True 是常用登录地址， False 是反之
        """
        remote_ip = request.META['REMOTE_ADDR']
        try:
            login_ip_list = json.loads(instance.login_position)
        except Exception:
            instance.login_position = json.dumps([remote_ip])
            return
        if len(login_ip_list) >= 3:
            for old_ip in login_ip_list:
                if remote_ip != old_ip:
                    login_ip_list.pop()
                    login_ip_list.insert(0, remote_ip)
                    instance.login_position = json.dumps(login_ip_list)
                    return False
            return True

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user.last_login:
            self.first_time_login(serializer)
        user.last_login = timezone.now()
        payload = jwt_payload_handler(user)
        payload['is_superuser'] = user.is_superuser
        token = jwt_encode_handler(payload)
        self.perform_create(user)
        return Response(
            {'token': f'{token}', 'real_name': user.real_name}
        )

    def first_time_login(self, serializer):
        user = serializer.validated_data['user']
        real_name = user.real_name
        password = serializer.validated_data['password']

        title = 'Ops 消息'
        # 站内消息
        inner_message = f'''
        <p style='text-indent: 10px'>
        {real_name} 您好，欢迎首次登录Ops平台，有什么需求尽管说，但未必能实现...
        <i class="ivu-icon ivu-icon-ios-game-controller-b" style="font-size: 15px;"/></i>
        </p>
        '''
        # 邮件消息
        mail_message = f'''
        {real_name} 您好，欢迎首次登录Ops平台，请妥善保管好您的验证信息:<br>
        &nbsp;&nbsp;用户：{user.username} <br>
        &nbsp;&nbsp;密码：{password} <br>
        '''
        sender(title, inner_message, [user.id, ])
        sender(title, mail_message, [user.id, ], send_type='mail', level='INFO')


class UsersOperationsViewSet(ListModelMixin,
                             rest_framwork_mixin.PureUpdateModelMixin,
                             DestroyModelMixin,
                             viewsets.GenericViewSet):
    """
    list:
        获取用户列表
    update:
        更新指定用户信息，不包括密码
    destroy:
        删除指定用户
    """
    queryset = UsersAccount.objects.all()
    serializer_class = UsersOperationsSerializer
    permission_classes = [perms.IsSuperUser, permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def list(self, request, *args, **kwargs):
        logger.info('获取用户')
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        gid = serializer.validated_data.pop('gid')
        # 操作变更用户组
        instance.groups.clear()
        instance.groups.add(Group.objects.get(id=int(gid)))
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # 删除 app 与 user 的关系
        AppConnectorRel.objects.filter(user_id=instance.id).delete()

        # 删除 ngx access alarm 的发送人
        for model_obj in AccessAlarmStrategy.objects.all():
            send_user_ids = json.loads(model_obj.send_user_id)
            if instance.id in send_user_ids:
                send_user_ids.remove(instance.id)
                model_obj.send_user_id = json.dumps(send_user_ids)
                model_obj.save()

        # 删除 monitor third party strategy 的发送人ID
        for model_obj in MonitorThirdPartyStrategy.objects.all():
            send_user_ids = json.loads(model_obj.send_user_id)
            if instance.id in send_user_ids:
                send_user_ids.remove(instance.id)
                model_obj.send_user_id = json.dumps(send_user_ids)
                model_obj.save()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UsersOpenViewSet(ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取开放用户列表
    """
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def list(self, request, *args, **kwargs):
        model_obj_list = UsersAccount.objects.all()
        return Response([
            {
                'id': model_obj.id,
                'username': model_obj.username,
                'position': model_obj.position,
                'department': model_obj.department,
                'email': model_obj.email,
                'mobile': model_obj.mobile,
                'real_name': model_obj.real_name
            }
            for model_obj in model_obj_list
        ])


class UsersChangePasswordViewSet(rest_framwork_mixin.PureUpdateModelMixin,
                                 viewsets.GenericViewSet):
    """
    update:
        修改密码
    """
    queryset = UsersAccount.objects.all()
    serializer_class = UsersChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsSuperUser, perms.IsPagePermissionRW)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.set_password(serializer.validated_data['password'])
        instance.save()
        return Response({'code': '0'})


class UsersAddViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
        添加用户
    """
    queryset = UsersAccount.objects.all()
    serializer_class = UsersAddSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsSuperUser, perms.IsPagePermissionRW)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = UsersAccount.objects.create_user(
            username=data['username'],
            password=data['password'],
            department=data['department'],
            is_staff=data['is_staff'],
            is_superuser=data['is_superuser'],
            email=data['email'],
            real_name=data['real_name'],
            position=data['position'],
            mobile=data['mobile']
        )
        user.groups.add(Group.objects.get(name='guest'))
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UsersGroupViewSet(ListModelMixin,
                        CreateModelMixin,
                        DestroyModelMixin,
                        viewsets.GenericViewSet):
    """
    用户组
    list:
        用户组列表
    create:
        添加用户组
    destroy:
        删除用户组
    """
    queryset = Group.objects.all()
    serializer_class = UsersGroupSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsSuperUser, perms.IsPagePermissionRW)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # 建立权限
        print(json.dumps(perms.PAGE_PERMS_TEMPLATE))
        print(serializer.data['id'])
        PermissionAll.objects.create(group_id=int(serializer.data['id']),
                                     page_permission=json.dumps(perms.PAGE_PERMS_TEMPLATE))
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.name == 'admin' or instance.name == 'guest':
            return Response(status=status.HTTP_403_FORBIDDEN, data={'detail': '不允许删除 admin 或 guest 组。'})
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PersonalInfoViewSet(RetrieveModelMixin, rest_framwork_mixin.PureUpdateModelMixin, viewsets.GenericViewSet):
    """
    read:
        获取个人信息 (owner)
    update:
        更新个人信息 (owner)
    """
    queryset = UsersAccount.objects.all()
    serializer_class = PersonalInfoSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsOwnerOrReadOnly)


class PersonalChangePasswordViewSet(rest_framwork_mixin.PureUpdateModelMixin, viewsets.GenericViewSet):
    """
    update:
        更新个人密码 (owner)
    """
    queryset = UsersAccount.objects.all()
    serializer_class = PersonalChangePasswordSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsOwnerOrReadOnly)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        o_password = serializer.validated_data['origin_password']
        user = authenticate(username=instance.username, password=o_password)
        if user:
            instance.set_password(serializer.validated_data['password'])
            instance.save()
            return Response({'code': 0})
        return Response({'detail': '原始密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
