from rest_framework import serializers


class OpenApiMysqlQuerySerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    query = serializers.CharField(help_text='sql 语句', required=True)
    schema = serializers.CharField(help_text='需要执行的数据库', required=True)


class OpenApiAnsibleHostSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    action = serializers.CharField(help_text='start', required=True)


class OpenApiAliyunSLBCtrlSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    env = serializers.CharField(help_text='str; 环境名, 如： release', required=True)
    app_name = serializers.CharField(help_text='str; app 名', required=True)
    ip = serializers.CharField(help_text='str; ip', required=True)
    weight = serializers.IntegerField(help_text='int; 权重 [0 - 100]', required=True)

