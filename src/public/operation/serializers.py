from rest_framework import serializers
from .models import OperationGlobalLog
from message.models import MessageMail


class GlobalOperatingLogSerializer(serializers.ModelSerializer):
    time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = OperationGlobalLog
        fields = '__all__'


class MessageMailLogSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = MessageMail
        fields = '__all__'