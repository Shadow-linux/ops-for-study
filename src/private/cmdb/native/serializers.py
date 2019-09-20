from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import NativeHost
from ..cmdb_common.models import Tags, TagsNativeHostRel


class TagsSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", help_text='str; 创建时间', read_only=True)

    class Meta:
        model = Tags
        fields = '__all__'

class NativeHostSerializer(serializers.ModelSerializer):
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", help_text='str; 更新时间', required=False)
    description = serializers.CharField(help_text='str; 描述', required=False)
    hostname = serializers.CharField(
        help_text='Hostname 名字',
        validators=[UniqueValidator
                    (queryset=NativeHost.objects.all(),
                     message="Hostname 名字已存在")],
        required=True
    )
    tags = serializers.SerializerMethodField(
        help_text='关联的tag',
        method_name='return_tags',
        read_only=True
    )

    def return_tags(self, obj):
        tags_ecs_rel = TagsNativeHostRel.objects.filter(target_id=obj.id)
        tags_list_obj = Tags.objects.filter(id__in=[item.tag_id for item in tags_ecs_rel])
        serializer = TagsSerializer(tags_list_obj, many=True)
        return serializer.data

    class Meta:
        model = NativeHost
        fields = '__all__'
