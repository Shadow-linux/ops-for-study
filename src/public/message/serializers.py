from rest_framework import serializers
from .models import MessageInner, MessagePush


class InnerMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageInner
        fields = '__all__'


class InnerMessageOperationSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(help_text="int; 用户id", read_only=True)

    class Meta:
        model = MessageInner
        fields = ('user_id', 'status',)


class MessagePushSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", help_text='创建时间', read_only=True)
    work_order = serializers.CharField(help_text='str; 工单号', read_only=True)

    class Meta:
        model = MessagePush
        fields = '__all__'
