from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from .models import Tags, TagsAliyunEcsRel, TagsNativeHostRel
from rest_framework.utils import model_meta
from rest_framework.serializers import raise_errors_on_nested_writes
from ..cloud.models import AliyunEcs
from ..native.models import NativeHost


class TagsSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", help_text='str; 创建时间', read_only=True)
    tag_key = serializers.CharField(
        help_text='str; tag key',
        validators=[UniqueValidator(queryset=Tags.objects.all())]
    )

    class Meta:
        model = Tags
        fields = '__all__'


class TagsEcsRelSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField(
        method_name='return_tag',
        help_text='str; tag 信息',
        read_only=True,
    )

    def return_tag(self, obj):
        tags_obj = Tags.objects.get(id=obj.tag_id)
        serializer = TagsSerializer(tags_obj)
        return serializer.data

    class Meta:
        model = TagsAliyunEcsRel
        fields = ('id', 'tag_id', 'target_id', 'tag')
        validators = [
            UniqueTogetherValidator(
                queryset=TagsAliyunEcsRel.objects.all(),
                fields=('target_id', 'tag_id'),
                message='该tag已关联, 勿重复关联。'
            )
        ]


class TagsNativeHostRelSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField(
        method_name='return_tag',
        help_text='str; tag 信息',
        read_only=True,
    )

    def return_tag(self, obj):
        tags_obj = Tags.objects.get(id=obj.tag_id)
        serializer = TagsSerializer(tags_obj)
        return serializer.data

    class Meta:
        model = TagsNativeHostRel
        fields = ('id', 'tag_id', 'target_id', 'tag')
        validators = [
            UniqueTogetherValidator(
                queryset=TagsNativeHostRel.objects.all(),
                fields=('target_id', 'tag_id'),
                message='该tag已关联, 勿重复关联。'
            )
        ]


class AnisbleUpdateHostInfoSerializer(serializers.Serializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    cmdb = serializers.CharField(help_text='str; 选择更新的cmdb [aliyun|native]', required=True)
    single_host_id = serializers.IntegerField(help_text='int; 单个host的id', required=False)


class AnisbleUpdateAliyunEcsSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        update_list = ['hostname', 'swap']
        for attr, value in validated_data.items():
            if attr in update_list:
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


class AnsibleUpdateNativeHostSerializer(serializers.ModelSerializer):

    class Meta:
        model = NativeHost
        fields = '__all__'


class AnsibleAddHostInfoSerializer(serializers.Serializer):

    cmdb = serializers.CharField(help_text='str; [aliyun|native]', required=True)
    # 作为唯一从表中区分的参数，如idc ac_key_id
    uniq = serializers.CharField(help_text='str; 作为唯一从表中区分的参数，如idc, ac_key_id', required=True)
    ssh_ip = serializers.CharField(help_text='str; ssh ip', required=True)
    ssh_port = serializers.IntegerField(help_text='int; ssh port', required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
