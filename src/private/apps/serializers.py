import json
from urllib.parse import urljoin
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import AppDetail, AppHostRel, AppConnectorRel
from users.models import UsersAccount
from common.models import SettingConf
from .libs import get_app_rel_host
from cmdb.cmdb_common.libs import get_host_tags


class AppDetailSerializer(serializers.ModelSerializer):
    updated = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', help_text='更新时间', read_only=True)
    app_name = serializers.CharField(
        help_text='app 名字',
        validators=[UniqueValidator
                    (queryset=AppDetail.objects.all(),
                     message="app 名字已存在")
                    ],
        required=True
    )

    # app 对应的主机信息
    host_list = serializers.SerializerMethodField(
        help_text='关联的host',
        method_name='return_host_list',
        read_only=True
    )

    # 联系人信息
    connector_detail = serializers.SerializerMethodField(
        help_text='关联的用户(read)',
        method_name='return_connector',
        read_only=True
    )
    connector = serializers.JSONField(
        help_text='json; 关联的用户(write) [1,2,3,4]',
        write_only=True,
        required=False
    )
    hosts = serializers.JSONField(
        help_text='json; 关联的主机(write) ["1:aliyun", "2:native]',
        write_only=True,
        required=False
    )

    def return_connector(self, obj):

        user_account_obj_list = UsersAccount.objects.filter(id__in=[
            model_obj.user_id
            for model_obj in AppConnectorRel.objects.filter(app_id=obj.id)
        ])

        return [
            {
                'id': user_obj.id,
                'username': user_obj.username
            }
            for user_obj in user_account_obj_list
        ]

    def return_host_list(self, obj):
        # 获取环境名
        setting_conf_obj = SettingConf.objects.get(id=1)
        cmdb_setting = json.loads(setting_conf_obj.cmdb_setting)
        env_list = cmdb_setting['base']['env']
        # 寻找不同的资源列表
        app_rel_host_dict = get_app_rel_host(obj.id)
        # 待处理model obj
        wait2handle_obj_list = (
            (app_rel_host_dict['aliyun'], 'aliyun'),
            (app_rel_host_dict['native'], 'native'),
        )

        # 组合列表
        env_host_dict = {}
        for env in env_list:
            env_host_dict[env] = []
            for data_tuple in wait2handle_obj_list:
                model_obj_list = data_tuple[0]
                cmdb = data_tuple[1]
                for host_obj in model_obj_list:
                    # 绑定的机器所属环境 及 在被选中的监控环境
                    if host_obj.environment == env:
                        info = {
                            'id': host_obj.id,
                            'hostname': host_obj.hostname,
                            'cmdb': cmdb,
                            'tags': get_host_tags(host_obj.id, cmdb),
                            'private_ip': ','.join(json.loads(host_obj.private_ip)),
                            'public_ip': ','.join(json.loads(host_obj.public_ip)),
                        }
                        if host_obj.environment in obj.internal_check_api_env:
                            info['internal_check_api'] = urljoin(
                                f'http://{json.loads(host_obj.private_ip)[0]}:{obj.port}',
                                obj.internal_check_api) if obj.is_internal_check_api else ''
                        env_host_dict[env].append(info)

        """env_host_dict 数据格式
        {
            "undefined": [
                {
                    "id": 1,
                    "hostname": "hostname",
                    "private_ip": "[\"1.1.1.1\", \"2.2.2.2\"]"
                },
                {
                    "id": 2,
                    "hostname": "hostname2",
                    "private_ip": "[\"1.1.1.1\", \"2.2.2.2\"]"
                }
            ]
        }
        """
        return env_host_dict

    def validate(self, attrs):
        del attrs['connector']
        del attrs['hosts']
        return attrs

    class Meta:
        model = AppDetail
        fields = '__all__'


class AppHostRelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppHostRel
        fields = '__all__'


class AppAliveUrlookerSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    app_id = serializers.IntegerField(help_text='int; app id')
    env = serializers.CharField(max_length=50, help_text='str; 环境名', required=False)
    is_alarm = serializers.IntegerField(help_text='int; 是否告警', required=False)
    check_api = serializers.CharField(max_length=100, help_text='str; check api', required=False)