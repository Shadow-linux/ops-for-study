from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.utils import model_meta
from rest_framework.serializers import raise_errors_on_nested_writes
from .models import AliyunKeys, AliyunEcs, AliyunRDS
from ..cmdb_common.models import Tags, TagsAliyunEcsRel
from apps.models import AppHostRel, AppDetail


# -------------------- 阿里云 --------------------
class AliyunPureKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = AliyunKeys
        fields = '__all__'


class AliyunKeysSerializer(serializers.ModelSerializer):
    key_name = serializers.CharField(help_text='str; key 名字',
                                     validators=[UniqueValidator(queryset=AliyunKeys.objects.all(),
                                                                 message="key 名字已存在")],
                                     required=True
                                     )
    access_key = serializers.CharField(help_text='access key', required=True)
    access_secret = serializers.CharField(help_text='access secret', write_only=True)
    region_id = serializers.CharField(help_text='region id', required=True)
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True, help_text='str; 更新时间')

    class Meta:
        model = AliyunKeys
        fields = '__all__'


class AliyunKeys2Serializer(serializers.ModelSerializer):

    class Meta:
        model = AliyunKeys
        fields = ('key_name', 'access_key', 'access_secret', 'region_id')


class AliyunEcsAutoSerializer(serializers.Serializer):
    key_name = serializers.CharField(help_text='str; access key 名字', required=True, write_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class TagsSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", help_text='str; 创建时间')

    class Meta:
        model = Tags
        fields = '__all__'


class AliyunRdsSerializer(serializers.ModelSerializer):
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", help_text='str; 更新时间', read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", help_text='str; 创建时间', read_only=True)
    expire_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", help_text='str; 过期时间', read_only=True)

    class Meta:
        model = AliyunRDS
        fields = '__all__'


class AliyunEcsSerializer(serializers.ModelSerializer):
    """
    基本操作ecs时使用该serializer
    """
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", help_text='str; 更新时间', required=False)
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", help_text='str; 创建时间', required=False)
    expired_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", help_text='str; 失效时间', required=False)
    tags = serializers.SerializerMethodField(
        help_text='关联的tag',
        method_name='return_tags',
        read_only=True
    )
    apps = serializers.SerializerMethodField(
        help_text='关联的App',
        method_name='return_apps',
        read_only=True
    )

    def return_tags(self, obj):
        tags_ecs_rel = TagsAliyunEcsRel.objects.filter(target_id=obj.id)
        tags_list_obj = Tags.objects.filter(id__in=[item.tag_id for item in tags_ecs_rel])
        serializer = TagsSerializer(tags_list_obj, many=True)
        return serializer.data

    def return_apps(self, obj):
        app_host_rel = AppHostRel.objects.filter(host_id=obj.id, owner='aliyun')
        app_detail_obj_list = AppDetail.objects.filter(id__in=[item.app_id for item in app_host_rel])
        return [
            {
                'id': app_obj.id,
                'app_name': app_obj.app_name,
                'is_active': app_obj.is_active
            }
            for app_obj in app_detail_obj_list
        ]

    class Meta:
        model = AliyunEcs
        fields = '__all__'


class AliyunEcsUpdateSerializer(serializers.ModelSerializer):
    """
    通过阿里云api更新时使用该serializer
    """

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        ignore_list = ['hostname', 'ssh_ip']

        for attr, value in validated_data.items():
            # 不更新hostname
            if attr in ignore_list:
                continue
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()

        return instance

    class Meta:
        model = AliyunEcs
        fields = '__all__'
