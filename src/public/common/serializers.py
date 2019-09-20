from rest_framework import serializers
from .models import SettingConf


class CommonSettingMessageSerializer(serializers.ModelSerializer):
    is_mail = serializers.BooleanField(required=True, help_text='bool; 是否启用mail')
    is_inner = serializers.BooleanField(required=True, help_text='bool; 是否启用站内信息')

    class Meta:
        model = SettingConf
        fields = ('message_setting', 'is_mail', 'is_inner')


class CommonSettingCmdbSerializer(serializers.ModelSerializer):

    class Meta:
        model = SettingConf
        fields = ('cmdb_setting',)


class CommonSettingAppSerializer(serializers.ModelSerializer):

    class Meta:
        model = SettingConf
        fields = ('app_setting',)


class CommonSettingMessageTestSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    mail_test = serializers.CharField(required=True,
                                      help_text='str;  测试邮箱 (当action 为 mail)',
                                      )

    class Meta:
        fields = ('mail_test',)


class CommonSettingSshProxySerializer(serializers.Serializer):
    proxy_idc = serializers.JSONField(help_text='list; 需要被代理的idc，如：["aliyun", "native"]')

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class CommonSettingCodePublishSerializer(serializers.ModelSerializer):

    class Meta:
        model = SettingConf
        fields = ('code_publish_setting',)