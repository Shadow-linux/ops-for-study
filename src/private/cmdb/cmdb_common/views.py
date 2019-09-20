import json
from django.conf import settings
from rest_framework import viewsets, mixins, status
from rest_framework import permissions
from permission import perms
from .models import Tags, TagsAliyunEcsRel, TagsNativeHostRel
from .serializers import (
    TagsSerializer, TagsEcsRelSerializer,
    TagsNativeHostRelSerializer,
    AnisbleUpdateHostInfoSerializer,
    AnsibleAddHostInfoSerializer,
    )
from ..cloud.models import AliyunEcs
from ..native.models import NativeHost
from public.util.libs import get_logger
from rest_framework.response import Response
from .libs import ansible_update_aliyun_ecs, ansible_update_native_host
from .filters import TagsNativeHostRelFB


logger = get_logger('cmdb_common.views')


# Create your views here.


class TagsViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    list:
        获取所有标签
    create:
        创建标签
    destroy:
        删除标签及其关系数据
    """
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def perform_destroy(self, instance):
        # 一并清除掉与其有关系的行
        TagsAliyunEcsRel.objects.filter(tag_id=instance.id).delete()
        TagsNativeHostRel.objects.filter(tag_id=instance.id).delete()
        instance.delete()


class TagsAliyunEcsRelViewSet(mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              mixins.CreateModelMixin,
                              viewsets.GenericViewSet):
    """
    list:
        获取对应target_id 的 tag 信息
    destroy:
        删除 阿里云ecs 与 tag 的关系
    create:
        创建 阿里云ecs 与 tag 的关系
    """
    queryset = TagsAliyunEcsRel.objects.all()
    serializer_class = TagsEcsRelSerializer
    filter_fields = ('target_id',)
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]


class TagsNativeHostRelViewSet(mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.CreateModelMixin,
                               viewsets.GenericViewSet):
    """
    list:
        获取 Native Host 对应的 tag 信息
    destroy:
        删除 Native Host 与 tag 的关系
    create:
        创建 Native Host 与 tag 的关系
    """
    queryset = TagsNativeHostRel.objects.all()
    serializer_class = TagsNativeHostRelSerializer
    filter_backends = (TagsNativeHostRelFB,)
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]


class AnisbleUpdateHostInfoViewSet(mixins.CreateModelMixin,
                                   viewsets.GenericViewSet):
    """
    create:
        通过ansible更新host信息 [aliyun|native]
    """
    CMDB_MAP = {
        'aliyun': AliyunEcs,
        'native': NativeHost
    }
    ANSIBLE_UPDATE_FUNC = {
        'aliyun': ansible_update_aliyun_ecs,
        'native': ansible_update_native_host
    }

    serializer_class = AnisbleUpdateHostInfoSerializer
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def create(self, request, *args, **kwargs):
        serializer = AnisbleUpdateHostInfoSerializer(data=request.data)
        serializer.is_valid()
        logger.info(f"ansible 更新信息 {serializer.validated_data}")
        cmdb = serializer.validated_data['cmdb']
        model = self.CMDB_MAP[cmdb]
        ansible_update_func = self.ANSIBLE_UPDATE_FUNC[cmdb]
        if serializer.validated_data.get('single_host_id', None):
            host_obj_list = model.objects.filter(id=serializer.validated_data['single_host_id'], is_ansible=1)
        else:
            host_obj_list = model.objects.filter(is_ansible=1)
        ret_status = status.HTTP_201_CREATED
        error_ssh_ip = {}
        for host_obj in host_obj_list:
            host_list = [
                [host_obj.ssh_ip, host_obj.ssh_port, 'root']
            ]
            try:
                ansible_update_func(host_list, host_obj)
            except Exception as e:
                ret_status = status.HTTP_500_INTERNAL_SERVER_ERROR
                error_ssh_ip[host_obj.hostname] = f'{host_obj.ssh_ip}:{host_obj.ssh_port}'
                logger.exception(e)

        detail = f'ansible 更新信息存在错误，Error Ip: {error_ssh_ip}' if ret_status == 500 else ''
        return Response({'detail': detail}, status=ret_status)


class AnsibleAddHostInfoViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
        通过ansible 自动添加机器信息
    """
    CMDB_MAP = {
        'aliyun': AliyunEcs,
        'native': NativeHost
    }

    serializer_class = AnsibleAddHostInfoSerializer
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def create(self, request, *args, **kwargs):
        serializer = AnsibleAddHostInfoSerializer(data=request.data)
        serializer.is_valid()
        cmdb = serializer.validated_data['cmdb']
        uniq = serializer.validated_data['uniq']
        ssh_ip = serializer.validated_data['ssh_ip']
        ssh_port = serializer.validated_data['ssh_port']
        model = self.CMDB_MAP[cmdb]
        try:
            if cmdb == 'native':
                self.add_native_host(model, uniq, ssh_ip, ssh_port, cmdb)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            data={'detail': 'ansible 自动添加信息失败, 检测是否已存在。'})

    # 验证资源表中是否已存在
    def __validator(self, model, uniq, ssh_ip, ssh_port, cmdb) -> bool:
        if cmdb == 'native':
            return model.objects.filter(idc=uniq, ssh_ip=ssh_ip, ssh_port=ssh_port).exists()

    # 通过ansible 自动添加本地机器信息
    def add_native_host(self, model, uniq, ssh_ip, ssh_port, cmdb):
        # 存在则raise
        if self.__validator(model, uniq, ssh_ip, ssh_port, cmdb):
            raise Exception(f'{uniq}, {ssh_ip}, {ssh_port}  已经存在 {cmdb}')

        model_obj = model(
            idc=uniq,
            ssh_ip=ssh_ip,
            ssh_port=ssh_port,
            status='Running',
            private_ip=json.dumps([ssh_ip]),
            public_ip=json.dumps([]),
        )
        ansible_update_native_host(
            [[ssh_ip, ssh_port, 'root']], model_obj
        )


class AllHostViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取所有host
    """
    permission_classes = [permissions.IsAuthenticated, perms.IsPagePermissionRW]

    def list(self, request, *args, **kwargs):
        aliyun_ecs_obj_list = AliyunEcs.objects.all()
        native_hosts_obj_list = NativeHost.objects.all()
        hadnle_tuple = ((aliyun_ecs_obj_list, 'aliyun'), (native_hosts_obj_list, 'native'))
        res_data = []
        for obj_list_cmdb in hadnle_tuple:
            obj_list, cmdb = obj_list_cmdb
            for model_obj in obj_list:
                res_data.append({
                    'id': model_obj.id,
                    'owner': cmdb,
                    'hostname': model_obj.hostname
                })

        return Response(res_data)
