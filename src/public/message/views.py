"""
该 APP 用于关于消息的所有接口调用
"""
import json
import importlib
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from permission import perms
from util.rest_framwork_mixin import PureUpdateModelMixin
from .serializers import InnerMessageSerializer, InnerMessageOperationSerializer, MessagePushSerializer
from .models import MessageInner, MessagePush
from users.models import UsersAccount
from message.send_message import sender
from util import libs


class InnerMessageViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取消息列表 (unread, read, trash)
    retrieve:
        获取消息内容
    """
    queryset = MessageInner.objects.all()
    serializer_class = InnerMessageSerializer
    permission_classes = (IsAuthenticated, perms.IsOwnerOrReadOnly)

    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        trash_obj_list = MessageInner.objects.filter(status=0, user_id=user_id)
        unread_obj_list = MessageInner.objects.filter(status=1, user_id=user_id)
        read_obj_list = MessageInner.objects.filter(status=2, user_id=user_id)
        trash_list = [{
            'create_time': o.created.strftime("%Y-%m-%d %H:%M:%S"),
            'loading': False,
            'msg_id': o.id,
            'title': o.title
        } for o in trash_obj_list]
        unread_list = [{
            'create_time': o.created.strftime("%Y-%m-%d %H:%M:%S"),
            'msg_id': o.id,
            'title': o.title
        } for o in unread_obj_list]
        read_list = [{
            'create_time': o.created.strftime("%Y-%m-%d %H:%M:%S"),
            'msg_id': o.id,
            'title': o.title,
            'loading': False,
        } for o in read_obj_list]
        return Response({
            'readed': read_list,
            'unread': unread_list,
            'trash': trash_list
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data['content']
        return Response(data)


class InnerMessageUnreadCountViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取未读消息条数
    """
    queryset = MessageInner.objects.all()
    serializer_class = InnerMessageSerializer
    permission_classes = (IsAuthenticated, perms.IsOwnerOrReadOnly)

    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        count = MessageInner.objects.filter(status=1, user_id=user_id).count()
        return Response(count)


class InnerMessageOperationViewSet(PureUpdateModelMixin,
                                   viewsets.GenericViewSet):
    """
    update:
        更新个人消息状态
    """
    queryset = MessageInner.objects.all()
    serializer_class = InnerMessageOperationSerializer
    permission_classes = (IsAuthenticated, perms.IsOwnerOrReadOnly)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class MessagePushViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取推送消息记录
    create:
        推送消息
    """
    queryset = MessagePush.objects.all()
    serializer_class = MessagePushSerializer
    permission_classes = (IsAuthenticated, perms.IsPagePermissionRW)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        send_status_dict = {}
        username_dict = {}
        for item in serializer.data:
            user_id_list = json.loads(item['user_id_list'])
            users_count = len(user_id_list)
            username_list = [obj.username for obj in UsersAccount.objects.filter(id__in=user_id_list)]
            username_dict[item['work_order']] = username_list
            send_status_dict[item['work_order']] = {}
            send_type_list = json.loads(item['send_type_list'])
            for send_type in send_type_list:
                models = importlib.__import__('message.models', fromlist=(f'Message{send_type.capitalize()}',))
                model = eval(f'models.Message{send_type.capitalize()}')
                send_obj_list = model.objects.filter(work_order=item['work_order'])
                send_status_set = {s.is_succeed for s in send_obj_list}
                send_status_dict[item['work_order']][send_type] = self.is_send(send_status_set,
                                                                               len(send_obj_list),
                                                                               users_count)
        return Response({
            'data': serializer.data,
            'send_types': send_status_dict,
            'usernames': username_dict
        })

    def is_send(self, send_status_set: set, sends_count: int, users_count: int) -> int:
        """
        对比用户数量，及其状态
        :return: 0 是等待 1是成功 2是失败
        """
        if sends_count != users_count:
            return 0
        if len(send_status_set) == 0:
            return 0
        if len(send_status_set) == 2:
            return 2
        status = send_status_set.pop()
        if status == True:
            return 1
        if status == False:
            return 2

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['work_order'] = libs.get_work_order('message')
        self.push_msg(serializer)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'code': 0}, status=status.HTTP_201_CREATED, headers=headers)

    def push_msg(self, serializer):
        user_id_list = json.loads(serializer.validated_data['user_id_list'])
        send_type_list = json.loads(serializer.validated_data['send_type_list'])
        for send_type in send_type_list:
            sender(title=serializer.validated_data['title'],
                   content=serializer.validated_data['content'],
                   send_type=send_type,
                   receiver_user_id_list=user_id_list,
                   work_order=serializer.validated_data['work_order'])
