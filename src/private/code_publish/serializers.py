# coding: utf-8
import json
from rest_framework import serializers
from .models import (CodePublishMainConf, CodePublishStatus, CodePublishDockerOpts, CodePublishMvnOpts,
                     CodePublishJarOpts, CodePublishJavaOpts, CodePublishSteps, CodePublishDockerFile,
                     CodePublishEnvMainConf, CodePublishWebControl, CodePublishLockEnv, CodePublishLockEnvApp,
                     CodePublishGradleOpts, CodePublishWebControlSteps)
from users.models import UsersAccount


class CodePublishJavaOptsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodePublishJavaOpts
        fields = '__all__'


class CodePublishJarOptsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodePublishJarOpts
        fields = '__all__'


class CodePublishDockerOptsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodePublishDockerOpts
        fields = '__all__'


class CodePublishMvnOptsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodePublishMvnOpts
        fields = '__all__'


class CodePublishGradleOptsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodePublishGradleOpts
        fields = '__all__'


class CodePublishDockerFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodePublishDockerFile
        fields = '__all__'


class CodePublishStepsSerializer(serializers.ModelSerializer):
    deploy_steps = serializers.SerializerMethodField(method_name='return_deploy_steps')
    rollback_steps = serializers.SerializerMethodField(method_name='return_rollback_steps')

    def return_deploy_steps(self, obj):
        return json.loads(obj.deploy_steps)

    def return_rollback_steps(self, obj):
        return json.loads(obj.rollback_steps)

    class Meta:
        model = CodePublishSteps
        fields = '__all__'


class CodePublishWebStepsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodePublishSteps
        fields = '__all__'


class CodePublishMainConfSerializer(serializers.ModelSerializer):
    publish_ip = serializers.SerializerMethodField(
        help_text='publish ip list',
        method_name='return_publish_ip',
        read_only=True
    )

    java_opts = serializers.SerializerMethodField(
        help_text='JAVA_OPTS',
        method_name='return_java_opts',
        read_only=True
    )

    jar_opts = serializers.SerializerMethodField(
        help_text='JAR_OPTS',
        method_name='return_jar_opts',
        read_only=True
    )

    docker_opts = serializers.SerializerMethodField(
        help_text='DOCKER_OPTS',
        method_name='return_docker_opts',
        read_only=True
    )
    dockerfile = serializers.SerializerMethodField(
        help_text='DOCKER_FILE',
        method_name='return_docker_file',
        read_only=True
    )

    mvn_opts = serializers.SerializerMethodField(
        help_text='MVN_OPTS',
        method_name='return_mvn_opts',
        read_only=True
    )

    gradle_opts = serializers.SerializerMethodField(
        help_text='GRADLE_OPTS',
        method_name='return_gradle_opts',
        read_only=True
    )

    steps = serializers.SerializerMethodField(
        help_text='steps',
        method_name='return_steps',
        read_only=True
    )

    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", help_text='str; 更新时间', required=False)

    def return_publish_ip(self, obj):
        return json.loads(obj.publish_ip)

    def return_java_opts(self, obj):
        if obj.java_opts_id:
            try:
                model_obj = CodePublishJavaOpts.objects.get(id=obj.java_opts_id)
                return CodePublishJavaOptsSerializer(model_obj).data
            except Exception:
                return {}
        return {}

    def return_jar_opts(self, obj):
        if obj.jar_opts_id:
            try:
                model_obj = CodePublishJarOpts.objects.get(id=obj.jar_opts_id)
                return CodePublishJarOptsSerializer(model_obj).data
            except Exception:
                return {}
        return {}

    def return_docker_opts(self, obj):
        if obj.docker_opts_id:
            try:
                model_obj = CodePublishDockerOpts.objects.get(id=obj.docker_opts_id)
                return CodePublishDockerOptsSerializer(model_obj).data
            except Exception:
                return {}
        return {}

    def return_docker_file(self, obj):
        if obj.dockerfile_id:
            try:
                model_obj = CodePublishDockerFile.objects.get(id=obj.dockerfile_id)
                return CodePublishDockerFileSerializer(model_obj).data
            except Exception:
                return {}
        return {}

    def return_mvn_opts(self, obj):
        if obj.mvn_opts_id:
            try:
                model_obj = CodePublishMvnOpts.objects.get(id=obj.mvn_opts_id)
                return CodePublishMvnOptsSerializer(model_obj).data
            except Exception:
                return {}

        return {}

    def return_gradle_opts(self, obj):
        if obj.gradle_opts_id:
            try:
                model_obj = CodePublishGradleOpts.objects.get(id=obj.gradle_opts_id)
                return CodePublishGradleOptsSerializer(model_obj).data
            except Exception:
                return {}

        return {}

    def return_steps(self, obj):
        if obj.steps_id:
            try:
                model_obj = CodePublishSteps.objects.get(id=obj.steps_id)
                return CodePublishStepsSerializer(model_obj).data
            except Exception:
                return {}
        return {}

    class Meta:
        model = CodePublishMainConf
        fields = ['app_name', 'env', 'pkg_name', 'java_opts', 'publish_ip', 'jar_opts', 'docker_opts', 'mvn_opts',
                  'steps', 'dockerfile', 'updated', 'jenkins_project', 'git_url', 'id', 'server_mode', 'web_tag',
                  'port', 'gradle_opts']


class CodePublishStatusSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    current_step = serializers.CharField(required=False, help_text='提前当前步骤')



class CodePublishWebMainConfSerializer(serializers.ModelSerializer):
    git_url = serializers.CharField(required=False, allow_blank=True)
    pkg_name = serializers.CharField(required=False, allow_blank=True)
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", help_text='str; 更新时间', required=False)

    class Meta:
        model = CodePublishMainConf
        fields = '__all__'


class CodePublishEnvMainConfSerializer(serializers.ModelSerializer):
    env = serializers.CharField(required=True, help_text='发布环境')

    class Meta:
        model = CodePublishEnvMainConf
        fields = '__all__'


class CodePublishReplaceIpSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    old_ip = serializers.CharField(max_length=24, required=True, help_text='旧IP')
    new_ip = serializers.CharField(max_length=24, required=True, help_text='新IP')
    env = serializers.CharField(max_length=64, required=True, help_text='环境')


class CodePublishBatchCopyConfSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    env = serializers.CharField(max_length=64, required=True, help_text='环境')
    app_ids = serializers.ListField(max_length=1024, required=True, help_text='app ids' )


class CodePublishCopyConfSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    envs = serializers.CharField(max_length=128, required=True, help_text='环境列表')


class CodePublishSetStepsSerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    publish_step = serializers.CharField(max_length=128, required=True, help_text='发布步骤')


class CodePublishTaskStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = CodePublishWebControl
        fields = '__all__'


class CodePublishWebControlCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CodePublishWebControl
        fields = '__all__'


class CodePublishWebControlListSerializer(serializers.ModelSerializer):
    steps_size = serializers.SerializerMethodField(method_name='return_steps_size', read_only=True)
    steps_status = serializers.SerializerMethodField(method_name='return_steps_status', read_only=True)
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", help_text='str; 更新时间', required=False)
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", help_text='str; 更新时间', required=False)
    creator = serializers.SerializerMethodField(method_name='return_creator', read_only=True)
    stander_steps = serializers.SerializerMethodField(method_name='return_stander_steps', read_only=True)

    def return_stander_steps(self, obj):
        try:
            model_obj = CodePublishWebControlSteps.objects.get(task_id=obj.id)
            return model_obj.stander_steps
        except Exception:
            return '[]'

    def return_creator(self, obj):
        try:
            model_obj = UsersAccount.objects.get(id=obj.creator)
            return model_obj.real_name
        except Exception:
            return 'null'

    def return_steps_size(self, obj):
        try:
            u_steps = json.loads(CodePublishWebControlSteps.objects.get(task_id=obj.id).upload_steps)
            return len(u_steps)
        except Exception:
            return 0

    def return_steps_status(self, obj):
        try:
            if obj.status == 2:
                return 'error'
            else:
                return 'finish'
        except Exception:
            return 'finish'

    class Meta:
        model = CodePublishWebControl
        fields = '__all__'


class CodePublishHasBeenPublishedSerializer(serializers.ModelSerializer):

    class Meta:
        model = CodePublishWebControl
        fields = '__all__'


class CodePublishEnvLockListSerializer(serializers.ModelSerializer):

    expired = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", help_text='str; 过期时间', required=False)
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", help_text='str; 更新时间', required=False)
    user_ids = serializers.SerializerMethodField(method_name='return_user_ids', read_only=True)
    app_ids = serializers.SerializerMethodField(method_name='return_app_ids', read_only=True)
    creator_info = serializers.SerializerMethodField(method_name='return_creator_info', read_only=True)

    def return_creator_info(self, obj):
        try:
            model_obj = UsersAccount.objects.get(id=obj.creator)
            return {
                'id': model_obj.id,
                'username': model_obj.username,
                'real_name': model_obj.real_name
            }
        except Exception:
            return {
                'id': 0,
                'username': None,
                'real_name': None
            }

    def return_user_ids(self, obj):
        model_obj_list = UsersAccount.objects.filter(id__in=json.loads(obj.user_ids))
        return [
            {
                'id': model_obj.id,
                'real_name': model_obj.real_name,
                'username': model_obj.username
            }
            for model_obj in model_obj_list
        ]

    def return_app_ids(self, obj):
        lea_model_obj_list = CodePublishLockEnvApp.objects.filter(lock_grp_id=obj.id)
        cpmc_model_obj_list = CodePublishMainConf.objects.filter(id__in=[
            mode_obj.app_name_id
            for mode_obj in lea_model_obj_list
        ])
        return [
            {
                'id': mode_obj.id,
                'app_name': mode_obj.app_name
            }
            for mode_obj in cpmc_model_obj_list
        ]

    class Meta:
        model = CodePublishLockEnv
        fields = '__all__'


class CodePublishEnvLockCreateSerializer(serializers.ModelSerializer):

    app_ids = serializers.ListField(help_text='app ids', required=True)
    user_ids = serializers.ListField(help_text='app ids', required=True)

    class Meta:
        model = CodePublishLockEnv
        fields = '__all__'
