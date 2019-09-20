import json
import os
import time
import threading
import datetime
import random
from urllib.parse import urlparse
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework import permissions
from .libs import get_lock_info_collections
from permission import perms
from public.util.rest_framwork_mixin import PureUpdateModelMixin
from public.util.libs import get_logger, ExecuteCmd
from public.util.call_mysql import OpsMysqlClient
from apps.libs import get_app_rel_host
from apps.models import AppDetail
from .jenkins_api import OpsJenkinsController
from .models import (CodePublishMainConf, CodePublishSteps, CodePublishMvnOpts, CodePublishJavaOpts,
                     CodePublishJarOpts, CodePublishDockerFile, CodePublishDockerOpts, CodePublishEnvMainConf,
                     CodePublishWebSetting, CodePublishWebControl, CodePublishLockEnv, CodePublishLockEnvApp,
                     CodePublishGradleOpts, CodePublishWebControlSteps)
from .filters import CodePublishSetStepsFB
from .serializers import (CodePublishMainConfSerializer, CodePublishStatusSerializer, CodePublishWebMainConfSerializer,
                          CodePublishMvnOptsSerializer, CodePublishJarOptsSerializer, CodePublishJavaOptsSerializer,
                          CodePublishDockerFileSerializer, CodePublishDockerOptsSerializer,
                          CodePublishEnvMainConfSerializer, CodePublishReplaceIpSerializer,
                          CodePublishCopyConfSerializer, CodePublishSetStepsSerializer, CodePublishWebStepsSerializer,
                          CodePublishTaskStatusSerializer, CodePublishWebControlCreateSerializer,
                          CodePublishWebControlListSerializer, CodePublishBatchCopyConfSerializer,
                          CodePublishHasBeenPublishedSerializer, CodePublishEnvLockListSerializer,
                          CodePublishEnvLockCreateSerializer, CodePublishGradleOptsSerializer)
from common.models import SettingConf

LOGGER = get_logger('code_publish.view')


# Create your views here.


# ############################### app config ################################
class CodePublishMainConfViewSet(mixins.ListModelMixin,
                                 mixins.RetrieveModelMixin,
                                 viewsets.GenericViewSet):
    """
    list:
        获取app list 对应的参数配置
    retrieve:
        获取app 对应的参数配置
    """
    queryset = CodePublishMainConf.objects.all()
    serializer_class = CodePublishMainConfSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)
    filter_fields = ('env', 'app_name')


class CodePublishWebMainConfViewSet(mixins.ListModelMixin,
                                    mixins.CreateModelMixin,
                                    PureUpdateModelMixin,
                                    mixins.DestroyModelMixin,
                                    viewsets.GenericViewSet):
    """
    list:
        获取app 对应的发布参数配置
    create:
        创建 app 对应的发布参数配置
    update:
        更新 app 对应的发布参数配置
    destroy:
        删除 app 对应的发布参数配置
    """
    queryset = CodePublishMainConf.objects.all()
    serializer_class = CodePublishWebMainConfSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)
    filter_fields = ('web_tag', 'env')

    def git_clone_code(self, git_url):
        code_dir = git_url.split('/')[-1].replace('.git', '')

        if code_dir:
            # 切换目录
            os.chdir(settings.CLONE_DIR)
            # 如已有的code dir，则不重新clone
            if os.path.exists(os.path.join(settings.CLONE_DIR, code_dir)):
                return
            # 组装用户密码
            url_s = urlparse(git_url)
            publish_setting = json.loads(SettingConf.objects.get(owner='global').code_publish_setting)
            git_user = publish_setting['git_info']['username']
            git_password = publish_setting['git_info']['password']

            # clone 代码
            rel_git_url = f'{url_s.scheme}://{git_user}:{git_password}@{url_s.netloc}{url_s.path}'
            ExecuteCmd.run_wait(cmd=f'''git clone {rel_git_url}''', exception=True)
            return
        raise Exception('code_dir 不存在')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        git_url = serializer.validated_data['git_url']
        try:
            self.git_clone_code(git_url)
        except Exception as e:
            LOGGER.error('git clone 出错, 检查是否git地址错误或用户密码错误')
            LOGGER.exception(e)
            return Response(data={'detail': 'git clone 出错, 检查是否git地址错误或用户密码错误'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CodePublishReplaceIpViewSet(mixins.CreateModelMixin,
                                  viewsets.GenericViewSet):
    """
    create:
        转换 旧IP 到 新IP
    """
    queryset = CodePublishMainConf.objects.all()
    serializer_class = CodePublishReplaceIpSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_ip = serializer.validated_data['old_ip']
        new_ip = serializer.validated_data['new_ip']
        env = serializer.validated_data['env']
        obj_list = self.queryset.filter(publish_ip__contains=old_ip, env=env)
        for obj in obj_list:
            ip_list = json.loads(obj.publish_ip)
            ip_list.remove(old_ip)
            ip_list.append(new_ip)
            obj.publish_ip = json.dumps(ip_list)
            obj.save()
        return Response(status=status.HTTP_201_CREATED)


class CodePublishBatchCopyConfigViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
        批量复制配置
    """
    queryset = CodePublishMainConf.objects.all()
    serializer_class = CodePublishBatchCopyConfSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        env = serializer.validated_data['env']
        app_ids = serializer.validated_data['app_ids']
        config_list_obj = self.queryset.filter(id__in=app_ids)

        for instance in config_list_obj:
            # jar opts 是跟着环境走的，所以需要按着其环境名配置
            try:
                jar_opts_id = CodePublishJarOpts.objects.get(name=env).id
            except Exception:
                jar_opts_id = instance.jar_opts_id
            try:
                CodePublishMainConf.objects.create(
                    app_name=instance.app_name,
                    env=env,
                    port=instance.port,
                    publish_ip='[]',
                    pkg_name=instance.pkg_name,
                    mvn_opts_id=instance.mvn_opts_id,
                    gradle_opts_id=instance.gradle_opts_id,
                    java_opts_id=instance.java_opts_id,
                    jar_opts_id=jar_opts_id,
                    docker_opts_id=instance.docker_opts_id,
                    dockerfile_id=instance.dockerfile_id,
                    steps_id=instance.steps_id,
                    git_url=instance.git_url,
                    jenkins_project=instance.jenkins_project,
                    server_mode=instance.server_mode,
                    web_tag=instance.web_tag
                )
            except Exception as e:
                # 如果不是冲突引起的错误，则忽略
                if 'Duplicate' not in e.__str__():
                    raise e

        return Response(status=status.HTTP_200_OK)


class CodePublishCopyConfigViewSet(PureUpdateModelMixin, viewsets.GenericViewSet):
    """
    update:
        复制发布配置
    """
    queryset = CodePublishMainConf.objects.all()
    serializer_class = CodePublishCopyConfSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        envs = request.data['envs']
        # 原子性操作
        with transaction.atomic():
            for env in envs:
                # jar opts 是跟着环境走的，所以需要按着其环境名配置
                try:
                    jar_opts_id = CodePublishJarOpts.objects.get(name=env).id
                except Exception:
                    jar_opts_id = instance.jar_opts_id
                try:
                    main_conf_obj = CodePublishMainConf()
                    main_conf_obj.app_name = instance.app_name
                    main_conf_obj.env = env
                    main_conf_obj.port = instance.port
                    main_conf_obj.publish_ip = '[]'
                    main_conf_obj.pkg_name = instance.pkg_name
                    main_conf_obj.mvn_opts_id = instance.mvn_opts_id
                    main_conf_obj.gradle_opts_id = instance.gradle_opts_id
                    main_conf_obj.java_opts_id = instance.java_opts_id
                    main_conf_obj.jar_opts_id = jar_opts_id
                    main_conf_obj.docker_opts_id = instance.docker_opts_id
                    main_conf_obj.dockerfile_id = instance.dockerfile_id
                    main_conf_obj.steps_id = instance.steps_id
                    main_conf_obj.git_url = instance.git_url
                    main_conf_obj.jenkins_project = instance.jenkins_project
                    main_conf_obj.server_mode = instance.server_mode
                    main_conf_obj.web_tag = instance.web_tag
                    main_conf_obj.save()
                except Exception as e:
                    if 'Duplicate' not in e.__str__():
                        raise e

        return Response(status=status.HTTP_200_OK)


# ################################ 配置模版 ###################################
class CodePublishWebMvnOptsViewSet(mixins.ListModelMixin,
                                   mixins.CreateModelMixin,
                                   mixins.DestroyModelMixin,
                                   PureUpdateModelMixin,
                                   viewsets.GenericViewSet):
    """
    list:
        获取 mvn opts 参数模版配置
    create:
        创建 mvn opts 参数模版配置
    update:
        更新 mvn opts 参数模版配置
    destroy:
        删除 mvn opts 参数模版配置
    """
    queryset = CodePublishMvnOpts.objects.all()
    serializer_class = CodePublishMvnOptsSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)


class CodePublishWebGradleOptsViewSet(mixins.ListModelMixin,
                                      mixins.CreateModelMixin,
                                      mixins.DestroyModelMixin,
                                      PureUpdateModelMixin,
                                      viewsets.GenericViewSet):
    """
    list:
        获取 gradle opts 参数模版配置
    create:
        创建 gradle opts 参数模版配置
    update:
        更新 gradle opts 参数模版配置
    destroy:
        删除 gradle opts 参数模版配置
    """
    queryset = CodePublishGradleOpts.objects.all()
    serializer_class = CodePublishGradleOptsSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)


class CodePublishWebJavaOptsViewSet(mixins.ListModelMixin,
                                    mixins.CreateModelMixin,
                                    mixins.DestroyModelMixin,
                                    PureUpdateModelMixin,
                                    viewsets.GenericViewSet):
    """
    list:
        获取 java opts 模版配置
    create:
        创建 java opts 参数模版配置
    update:
        更新 java opts 参数模版配置
    destroy:
        删除 java opts 参数模版配置
    """
    queryset = CodePublishJavaOpts.objects.all()
    serializer_class = CodePublishJavaOptsSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)


class CodePublishWebJarOptsViewSet(mixins.ListModelMixin,
                                   mixins.CreateModelMixin,
                                   mixins.DestroyModelMixin,
                                   PureUpdateModelMixin,
                                   viewsets.GenericViewSet):
    """
    list:
        获取 jar opts 模版配置
    create:
        创建 jar opts 参数模版配置
    update:
        更新 jar opts 参数模版配置
    destroy:
        删除 jar opts 参数模版配置
    """
    queryset = CodePublishJarOpts.objects.all()
    serializer_class = CodePublishJarOptsSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)


class CodePublishWebDockerfileViewSet(mixins.ListModelMixin,
                                      mixins.CreateModelMixin,
                                      mixins.DestroyModelMixin,
                                      PureUpdateModelMixin,
                                      viewsets.GenericViewSet):
    """
    list:
        获取 dockerfile 模版配置
    create:
        创建 dockerfile 参数模版配置
    update:
        更新 dockerfile 参数模版配置
    destroy:
        删除 dockerfile 参数模版配置
    """
    queryset = CodePublishDockerFile.objects.all()
    serializer_class = CodePublishDockerFileSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)


class CodePublishWebDockerOptsViewSet(mixins.ListModelMixin,
                                      mixins.CreateModelMixin,
                                      mixins.DestroyModelMixin,
                                      PureUpdateModelMixin,
                                      viewsets.GenericViewSet):
    """
    list:
        获取 docker opts 模版配置
    create:
        创建 docker opts 参数模版配置
    update:
        更新 docker opts 参数模版配置
    destroy:
        删除 docker opts 参数模版配置
    """
    queryset = CodePublishDockerOpts.objects.all()
    serializer_class = CodePublishDockerOptsSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)


class CodePublishWebStepsOptsViewSet(mixins.ListModelMixin,
                                     mixins.CreateModelMixin,
                                     mixins.DestroyModelMixin,
                                     PureUpdateModelMixin,
                                     viewsets.GenericViewSet):
    """
    list:
        获取 steps opts 模版配置
    create:
        创建 steps opts 参数模版配置
    update:
        更新 steps opts 参数模版配置
    destroy:
        删除 steps opts 参数模版配置
    """
    queryset = CodePublishSteps.objects.all()
    serializer_class = CodePublishWebStepsSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)


class CodePublishSetStepsViewSet(mixins.ListModelMixin,
                                 mixins.CreateModelMixin,
                                 mixins.DestroyModelMixin,
                                 viewsets.GenericViewSet):
    """
    list:
        获取所有发布步骤
    create:
        创建发布步骤
    """
    queryset = CodePublishWebSetting.objects.all()
    serializer_class = CodePublishSetStepsSerializer
    filter_backends = (CodePublishSetStepsFB,)
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        model_obj = queryset.get(id=1)
        return Response(data=json.loads(model_obj.publish_steps), status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        publish_step = request.query_params['publish_step']
        model_obj = self.queryset.get(id=1)
        publish_steps_list = json.loads(model_obj.publish_steps)
        publish_steps_list.remove(publish_step)
        model_obj.publish_steps = json.dumps(publish_steps_list)
        model_obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        publish_step = serializer.validated_data['publish_step']
        model_obj = self.queryset.get(id=1)
        publish_steps_list = json.loads(model_obj.publish_steps)
        publish_steps_list.append(publish_step)
        model_obj.publish_steps = json.dumps(publish_steps_list)
        model_obj.save()
        return Response(status=status.HTTP_201_CREATED)


# ############################### app publish #######################################
class CodePublishStatusViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               PureUpdateModelMixin,
                               viewsets.GenericViewSet):
    """
    list:
        获取所有app发布状态
    update:
        更新app 发布步骤
    """

    queryset = CodePublishWebControlSteps.objects.all()
    serializer_class = CodePublishStatusSerializer
    lookup_field = 'task_id'
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        current_step = request.data['current_step']
        LOGGER.info(f'[Code Publish Steps] TaskID: {instance.task_id}, current upload step: {current_step}')
        upload_steps = json.loads(instance.upload_steps)
        upload_steps.append(current_step)
        instance.upload_steps = json.dumps(upload_steps)
        LOGGER.info(f'[Code Publish Steps] TaskID: {instance.task_id}, save upload step: {upload_steps}')
        instance.save()
        return Response(status=status.HTTP_200_OK, data={'id': instance.task_id})


class CodePublishEnvViewSet(mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            PureUpdateModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    """
    list:
        获取可发布环境的列表
    create:
        创建发布环境
    update:
        更新发布环境，并且更新发布主配置
    destroy:
        删除发布环境
    """
    queryset = CodePublishEnvMainConf.objects.all()
    serializer_class = CodePublishEnvMainConfSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        origin_env = instance.env
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # 更新发布主配置
        main_conf_obj_list = CodePublishMainConf.objects.filter(env=origin_env)
        for main_conf_obj in main_conf_obj_list:
            main_conf_obj.env = instance.env
            main_conf_obj.save()

        return Response(serializer.data)


class CodePublishAppDetailViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取 App IP
    """

    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def list(self, request, *args, **kwargs):
        app_detail_dict = {}
        app_obj_list = AppDetail.objects.filter(is_publish=1)
        for app_obj in app_obj_list:
            model_obj_dict = get_app_rel_host(app_obj.id)
            env_ip_dict = {}
            for _, model_obj_list in model_obj_dict.items():
                if model_obj_list:
                    for model_obj in model_obj_list:
                        for ip in json.loads(model_obj.public_ip):
                            env_ip_dict[ip] = f'{model_obj.environment} - (公)'
                        for ip in json.loads(model_obj.private_ip):
                            env_ip_dict[ip] = f'{model_obj.environment} - (私)'
            app_detail_dict[app_obj.app_name] = env_ip_dict
        return Response(data=app_detail_dict, status=status.HTTP_200_OK)


class CodePublishTaskStatusViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        通过jenkins api 更新发布状态
    """

    queryset = CodePublishWebControl.objects.all()
    serializer_class = CodePublishTaskStatusSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def list(self, request, *args, **kwargs):
        ops_jenkins_ctrl = OpsJenkinsController()
        model_obj_list = self.queryset.filter(Q(status=3) | Q(status=0))
        for model_obj in model_obj_list:
            if model_obj.build_num != 0:
                model_obj.status = ops_jenkins_ctrl.get_job_id_status(job=model_obj.jenkins_job,
                                                                      number=model_obj.build_num)
                model_obj.save()

        model_obj_list = self.queryset.filter(Q(status=3) | Q(status=0))
        serializer = self.get_serializer(model_obj_list, many=True)
        return Response(status=status.HTTP_200_OK)


class CodePublishRTTaskStatusViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取状态为执行中和未启动的列表
    """
    queryset = CodePublishWebControl.objects.all()
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def list(self, request, *args, **kwargs):
        now_date = datetime.datetime.now()
        expired_time = now_date - datetime.timedelta(minutes=20)
        model_obj_list = self.queryset.filter(Q(status=3) | Q(status=0)).filter(created__gt=expired_time)
        data = [
            {
                'app_name': model_obj.app_name,
                'env': model_obj.env,
                'publish_ip': model_obj.publish_ip,
                'branch': model_obj.branch,
                'status': model_obj.status
            }
            for model_obj in model_obj_list
        ]
        return Response(status=status.HTTP_200_OK, data=data)


class CodePublishMainConfAppDetailViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取 app 发布配置环境IP 信息
    """

    queryset = CodePublishMainConf.objects.all()
    filter_fields = ('app_name', 'env')
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = []
        for model_obj in queryset:
            data = json.loads(model_obj.publish_ip)

        return Response(data=[
            [item, False]
            for item in data
        ], status=status.HTTP_200_OK)


class CodePublishControlAppDetailViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取control app detail 信息
    """
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def list(self, request, *args, **kwargs):
        app_detail_dict = {}
        app_obj_list = AppDetail.objects.filter(is_publish=1, is_active=1)
        for app_obj in app_obj_list:
            model_obj_dict = get_app_rel_host(app_obj.id)
            env_dict = {}

            for _, model_obj_list in model_obj_dict.items():
                if model_obj_list:
                    for model_obj in model_obj_list:
                        # 先判断是否是列表， 没有则创建，用于组装信息
                        if not isinstance(env_dict.get(model_obj.environment.lower()), list):
                            env_dict[model_obj.environment.lower()] = []

                        for ip in json.loads(model_obj.public_ip):
                            env_dict[model_obj.environment.lower()].append(
                                (ip, f'{model_obj.environment} - (公)')
                            )

                        for ip in json.loads(model_obj.private_ip):
                            env_dict[model_obj.environment.lower()].append(
                                (ip, f'{model_obj.environment} - (私)')
                            )

            app_detail_dict[app_obj.app_name] = env_dict
        return Response(data=app_detail_dict, status=status.HTTP_200_OK)


class CodePublishControlViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.DestroyModelMixin,
                                viewsets.GenericViewSet):
    """
    list:
        获取所有任务信息
    create:
        创建发布任务
    destroy:
        删除发布任务记录
    """
    queryset = CodePublishWebControl.objects.all()
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW, perms.IsPublishCode)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset.all().order_by('-id'), many=True)
        return Response(serializer.data)

    def get_steps(self, data):
        cpmc_obj = CodePublishMainConf.objects.get(app_name=data['app_name'], env=data['env'])
        try:
            cps_obj = CodePublishSteps.objects.get(id=cpmc_obj.steps_id)
        except Exception:
            return '[]'

        if data['action'] == 'Rollback':
            return cps_obj.rollback_steps
        elif data['action'] == 'Deploy':
            return cps_obj.deploy_steps
        elif data['action'] == 'DeploySync':
            return cps_obj.deploy_sync_steps
        else:
            return '[]'

    def get_serializer_class(self):
        if self.action == 'list':
            return CodePublishWebControlListSerializer

        if self.action == 'create':
            return CodePublishWebControlCreateSerializer

    def __publish_version(self, app_name):
        tt = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
        return f'{app_name}_{tt}_{random.randrange(0, 99)}'

    def update_job_status(self, job, num, ops_jenkins_ctrl, control_id):
        """
        :param job: jenkins job
        :param num:  build number
        :param ops_jenkins_ctrl:
        :param control_id: control model id
        :return:
        """

        # 先写死是5秒，后面可以做到界面上设置
        time.sleep(5)
        build_status = ops_jenkins_ctrl.get_job_id_status(job=job, number=num)
        model_obj = self.queryset.get(id=control_id)
        model_obj.status = build_status
        model_obj.save()

    def __complete_publish(self, main_conf_obj, serializer, last_task_obj):
        """
        :param main_conf_obj:
        :param last_task_obj:
        :return:
        """
        has_been_published = []
        if last_task_obj:
            # 上次已完整发布
            if last_task_obj.is_done == 1:
                # 直接
                has_been_published.append(serializer.validated_data['publish_ip'])
            # 上次未完整发布
            elif last_task_obj.is_done == 0:
                # 先把当前发布ip 加入队列后再进行比较
                has_been_published = json.loads(last_task_obj.has_been_published)
                has_been_published.append(serializer.validated_data['publish_ip'])
        else:
            has_been_published.append(serializer.validated_data['publish_ip'])

        # 比较配置队列 和 已发布IP 队列
        if set(has_been_published) == set(json.loads(main_conf_obj.publish_ip)):
            # 已发布完整
            is_done = 1
        else:
            # 未发布完整
            is_done = 0

        return is_done, json.dumps(has_been_published)

    def get_git_log(self, app_name):
        instance = CodePublishMainConf.objects.filter(app_name=app_name).first()
        code_dir = instance.git_url.split('/')[-1].replace('.git', '')
        if code_dir:
            try:
                os.chdir(os.path.join(settings.CLONE_DIR, code_dir))
                result = ExecuteCmd.run_wait(cmd=f'''git log --pretty=oneline -10 |grep -v Merge| head -n 1''',
                                             exception=True)
                return result['stdout']
            except Exception as e:
                LOGGER.exception(e)
                return ''


    def sync_task(self, main_conf_obj, serializer, publish_version, dep_build_num, user_id, git_log):
        ops_jenkins_ctrl = OpsJenkinsController()

        # 10 分钟执行不完就不再同步到别的环境
        ttl = 600
        # 检查是否已经发布完成
        while True:
            try:
                # 如果已经生成了build info ，则继续检查是否还存在于 running 列表
                ops_jenkins_ctrl.get_build_info(main_conf_obj.jenkins_project, dep_build_num)
                running_builds_list = ops_jenkins_ctrl.get_running_builds()
                for build_dict in running_builds_list:
                    if build_dict['name'] == main_conf_obj.jenkins_project and \
                            build_dict['number'] == dep_build_num:
                        raise Exception
                break
            except Exception:
                if ttl <= 0:
                    return
                time.sleep(1)
                ttl -= 1
        sub_conf_obj = CodePublishMainConf.objects.get(app_name=serializer.validated_data['app_name'],
                                                       env=serializer.validated_data['sync_env'])
        # 更改为同步动作
        serializer.validated_data['action'] = 'DeploySync'
        control_obj = self.queryset.create(
            app_name=serializer.validated_data['app_name'],
            env=serializer.validated_data['sync_env'],
            action=serializer.validated_data['action'],
            jenkins_job=sub_conf_obj.jenkins_project,
            publish_version=publish_version,
            publish_ip=serializer.validated_data['sync_ip'],
            status=0,
            creator=user_id,
            branch=serializer.validated_data['branch'],
            git_log=git_log,
            is_sync=0,
            sync_env='',
            sync_ip=''
        )

        # 保存发布步骤
        CodePublishWebControlSteps.objects.create(
            task_id=control_obj.id,
            stander_steps=self.get_steps(serializer.validated_data),
        )

        # 标准接受的参数无论是前端还是后端project
        jenkins_params = json.loads(serializer.validated_data['jenkins_params'])
        jenkins_params['ProjectName'] = serializer.validated_data['app_name']
        jenkins_params['Action'] = 'DeploySync'
        jenkins_params['Version'] = publish_version
        jenkins_params['Environment'] = serializer.validated_data['sync_env']
        jenkins_params['PublishIP'] = serializer.validated_data['sync_ip']
        jenkins_params['ServerMode'] = sub_conf_obj.server_mode
        jenkins_params['Branch'] = serializer.validated_data['branch']
        jenkins_params['TaskID'] = control_obj.id

        console_url, build_number = ops_jenkins_ctrl.build_job(sub_conf_obj.jenkins_project, jenkins_params)
        if build_number == 0 or not build_number or not isinstance(build_number, int):
            control_obj.delete()
            raise Exception(f'创建jenkins build任务失败，检查网络连接问题。build number: {build_number}')
        time.sleep(1)
        LOGGER.info(f'''[同步任务] 启动 Jenkins Job：{sub_conf_obj.jenkins_project}, Build Number: {build_number},
        Jenkins Params: {jenkins_params}''')
        # 重新保存
        control_obj.jenkins_params = json.dumps(jenkins_params)
        control_obj.build_num = int(build_number)
        control_obj.console_url = console_url
        control_obj.save()

    def rollback_task(self, main_conf_obj, serializer, last_task_obj, user_id):
        ops_jenkins_ctrl = OpsJenkinsController()
        jenkins_params = json.loads(serializer.validated_data['jenkins_params'])
        # 判断是否完整发布
        is_done, has_been_published = self.__complete_publish(main_conf_obj, serializer, last_task_obj)
        serializer.validated_data['is_done'] = is_done
        serializer.validated_data['has_been_published'] = has_been_published
        serializer.validated_data['jenkins_job'] = main_conf_obj.jenkins_project
        model_obj = CodePublishWebControl.objects.filter(
            publish_version=serializer.validated_data['publish_version']).first()
        serializer.validated_data['branch'] = model_obj.branch
        serializer.validated_data['creator'] = user_id
        serializer.validated_data['git_log'] = self.get_git_log(app_name=serializer.validated_data['app_name'])
        control_obj = serializer.save()

        # 保存发布步骤
        CodePublishWebControlSteps.objects.create(
            task_id=control_obj.id,
            stander_steps=self.get_steps(serializer.validated_data),
        )

        # 标准接受的参数无论是前端还是后端project
        jenkins_params['ProjectName'] = serializer.validated_data['app_name']
        jenkins_params['Environment'] = serializer.validated_data['env']
        jenkins_params['Action'] = serializer.validated_data['action']
        jenkins_params['TaskID'] = control_obj.id
        jenkins_params['Version'] = serializer.validated_data['publish_version']
        jenkins_params['PublishIP'] = serializer.validated_data['publish_ip']
        jenkins_params['ServerMode'] = main_conf_obj.server_mode
        jenkins_params['Branch'] = serializer.validated_data['branch']

        # 调用 jenkins build job
        console_url, build_number = ops_jenkins_ctrl.build_job(main_conf_obj.jenkins_project, jenkins_params)
        LOGGER.info(f'''[回滚任务] 启动 Jenkins Job：{main_conf_obj.jenkins_project}, Build Number: {build_number},
        Jenkins Params: {jenkins_params}''')
        time.sleep(1)
        if build_number == 0 or not build_number or not isinstance(build_number, int):
            control_obj.delete()
            raise Exception(f'创建jenkins build任务失败，检查网络连接问题。build number: {build_number}')

        # 在此保存jenkins 信息
        control_obj.jenkins_params = json.dumps(jenkins_params)
        control_obj.build_num = int(build_number)
        control_obj.console_url = console_url
        control_obj.save()

        # make some times for Jenkins
        time.sleep(3)
        try:
            # 如果需要同步则进行同步
            if serializer.validated_data['is_sync'] == 1:
                sync_task = threading.Thread(target=self.sync_task,
                                             args=(
                                                 main_conf_obj,
                                                 serializer,
                                                 serializer.validated_data['publish_version'],
                                                 build_number,
                                                 user_id,
                                                 serializer.validated_data['git_log']
                                             ))
                sync_task.start()
        except Exception as e:
            LOGGER.error('同步发布任务失败')
            LOGGER.exception(e)

    def create_task(self, main_conf_obj, serializer, last_task_obj, user_id):
        ops_jenkins_ctrl = OpsJenkinsController()
        publish_version = self.__publish_version(serializer.validated_data['app_name'])
        jenkins_params = json.loads(serializer.validated_data['jenkins_params'])
        # 判断是否完整发布
        is_done, has_been_published = self.__complete_publish(main_conf_obj, serializer, last_task_obj)

        serializer.validated_data['is_done'] = is_done
        serializer.validated_data['has_been_published'] = has_been_published
        serializer.validated_data['jenkins_job'] = main_conf_obj.jenkins_project
        # 若未完整发布，则用上一次发布的版本
        if last_task_obj:
            if last_task_obj.is_done == 1:
                serializer.validated_data['publish_version'] = publish_version
            else:
                serializer.validated_data['publish_version'] = last_task_obj.publish_version
        else:
            serializer.validated_data['publish_version'] = publish_version
        serializer.validated_data['action'] = serializer.validated_data['action']
        serializer.validated_data['creator'] = user_id
        serializer.validated_data['git_log'] = self.get_git_log(app_name=serializer.validated_data['app_name'])
        control_obj = serializer.save()

        # 保存发布步骤
        CodePublishWebControlSteps.objects.create(
            task_id=control_obj.id,
            stander_steps=self.get_steps(serializer.validated_data),
        )

        # 标准接受的参数无论是前端还是后端project
        jenkins_params['ProjectName'] = serializer.validated_data['app_name']
        jenkins_params['Environment'] = serializer.validated_data['env']
        jenkins_params['Action'] = serializer.validated_data['action']
        jenkins_params['TaskID'] = control_obj.id
        jenkins_params['Version'] = serializer.validated_data['publish_version']
        jenkins_params['PublishIP'] = serializer.validated_data['publish_ip']
        jenkins_params['ServerMode'] = main_conf_obj.server_mode
        jenkins_params['Branch'] = serializer.validated_data['branch']

        # 调用 jenkins build job
        console_url, build_number = ops_jenkins_ctrl.build_job(main_conf_obj.jenkins_project, jenkins_params)
        LOGGER.info(f'''[创建任务] 启动 Jenkins Job：{main_conf_obj.jenkins_project}, Build Number: {build_number},
        Jenkins Params: {jenkins_params}''')
        time.sleep(1)
        if build_number == 0 or not build_number or not isinstance(build_number, int):
            control_obj.delete()
            raise Exception(f'创建jenkins build任务失败，检查网络连接问题。build number: {build_number}')

        # 在此保存jenkins 信息
        control_obj.jenkins_params = json.dumps(jenkins_params)
        control_obj.build_num = int(build_number)
        control_obj.console_url = console_url
        control_obj.save()

        try:
            # 如果需要同步则进行同步
            if serializer.validated_data['is_sync'] == 1:
                sync_task = threading.Thread(target=self.sync_task,
                                             args=(
                                                 main_conf_obj,
                                                 serializer,
                                                 serializer.validated_data['publish_version'],
                                                 build_number,
                                                 user_id,
                                                 serializer.validated_data['git_log']
                                             ))
                sync_task.start()
        except Exception as e:
            LOGGER.error('同步发布任务失败')
            LOGGER.exception(e)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = self.request.user.id
        try:
            data = serializer.validated_data
            main_conf_obj = CodePublishMainConf.objects.get(app_name=data['app_name'], env=data['env'])
        except Exception as e:
            LOGGER.error('创建发布任务失败, 没有找到该应用的发布配置')
            LOGGER.exception(e)
            return Response(data={'detail': '没有找到该应用的发布配置。'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            last_task_obj = self.queryset.filter(app_name=data['app_name'],
                                                 env=data['env'],
                                                 action=data['action']).order_by('-id').first()
        except Exception as e:
            LOGGER.warning('执行获取上次发布任务失败')
            last_task_obj = None

        try:
            if data['action'] == 'Deploy' or data['action'] == 'DeploySync':
                self.create_task(main_conf_obj, serializer, last_task_obj, user_id)
        except Exception as e:
            LOGGER.error('创建发布任务失败')
            LOGGER.exception(e)
            return Response(data={'detail': f'创建发布任务失败。{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            if data['action'] == 'Rollback':
                self.rollback_task(main_conf_obj, serializer, last_task_obj, user_id)
        except Exception as e:
            LOGGER.error('创建回滚任务失败')
            LOGGER.exception(e)
            return Response(data={'detail': f'创建回滚任务失败。{e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_200_OK)


class CodePublishHasBeenPublishedViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取已操作发布的IP
    """
    queryset = CodePublishWebControl.objects.all()
    serializer_class = CodePublishHasBeenPublishedSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)
    filter_fields = ('app_name', 'env', 'action')

    def list(self, request, *args, **kwargs):
        app_name = self.request.query_params['app_name']
        env = self.request.query_params['env']
        action = self.request.query_params['action']
        instance = self.queryset.filter(app_name=app_name, env=env, action=action).order_by('-id').first()
        data = []
        if instance:
            serializer = self.get_serializer(instance)
            if instance.is_done == 1:
                data = []
            else:
                data = json.loads(serializer.data['has_been_published'])
        return Response(data)


class CodePublishStopBuildViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    destroy:
        停止发布building中的任务
    """
    queryset = CodePublishWebControl.objects.all()
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        ops_jenkins_ctrl = OpsJenkinsController()
        ops_jenkins_ctrl.stop_build(instance.jenkins_job, instance.build_num)
        # make some times for Jenkins
        time.sleep(2)
        status_ = ops_jenkins_ctrl.get_job_id_status(instance.jenkins_job, instance.build_num)
        instance.status = status_
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CodePublishCheckCodeBranch(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    retrieve:
        获取应用分支名
    """
    queryset = CodePublishMainConf.objects.all()
    filter_fields = ('app_name', 'env')
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if queryset:
            instance = queryset[0]
            code_dir = instance.git_url.split('/')[-1].replace('.git', '')
            if code_dir:
                try:
                    print(os.path.join(settings.CLONE_DIR, code_dir))
                    os.chdir(os.path.join(settings.CLONE_DIR, code_dir))
                    ExecuteCmd.run_wait(cmd=f'''git pull''', exception=True)
                    result = ExecuteCmd.run_wait(cmd=f'''git branch -r |grep -v HEAD''', exception=True)
                    return Response(data=["/".join(item.split('/')[1:]) for item in result['stdout'].split()],
                                    status=status.HTTP_200_OK)
                except Exception as e:
                    LOGGER.exception(e)
                    return Response(data={'detail': '不存在git clone 目录, 无法查找分支'},
                                    status=status.HTTP_404_NOT_FOUND)
            return Response(data={'detail': '为配置git url 地址, 无法查找分支'},
                            status=status.HTTP_404_NOT_FOUND)
        return Response(data={'detail': '获取配置失败, 检查APP是否没有配置该环境'},
                        status=status.HTTP_404_NOT_FOUND)


class CodePublishGetRTSteps(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取实时进度
    """
    queryset = CodePublishWebControl.objects.all()
    serializer_class = CodePublishWebControlListSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        steps_size = len(json.loads(CodePublishWebControlSteps.objects.get(task_id=instance.id).upload_steps))
        status_ = 'error' if serializer.data['status'] == 2 else 'finish'
        return Response(data={
            'steps_size': steps_size,
            'status': status_,
        }, status=status.HTTP_200_OK)


class CodePublishAlreadyPublishedVerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取当前APP 历史发布的版本列表
    """
    queryset = CodePublishWebControl.objects.all()
    serializer_class = CodePublishWebControlListSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def list(self, request, *args, **kwargs):
        LOGGER.debug(f'''
        SELECT DISTINCT publish_version,
                app_name,
                branch
            FROM   cp_web_control
            WHERE  app_name = "{self.request.query_params['app_name']}"
               AND env = "{self.request.query_params['env']}"
               AND is_done = 1
               AND action = "Deploy"
               AND status = 1
            ORDER  BY id DESC
            LIMIT  2;
        ''')
        with OpsMysqlClient() as cursor:
            cursor.execute(f'''
            SELECT DISTINCT publish_version,
                app_name,
                branch
            FROM   cp_web_control
            WHERE  app_name = "{self.request.query_params['app_name']}"
               AND env = "{self.request.query_params['env']}"
               AND is_done = 1
               AND action = "Deploy"
               AND status = 1
            ORDER  BY id DESC
            LIMIT  2;
            ''')
            result_set = cursor.fetchall()
        # return Response()
        print(result_set)
        return Response(status=status.HTTP_200_OK, data={
            data['publish_version']: data['branch']
            for data in result_set
        })


class CodePublishAppEndpointViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取APP带endpoint 标记列表
    """
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)
    queryset = CodePublishMainConf.objects.all()
    filter_fields = ('web_tag', 'env')

    def list(self, request, *args, **kwargs):
        web_tag = self.request.query_params['web_tag']
        env = self.request.query_params['env']
        user_id = self.request.user.id
        model_obj_list = self.queryset.filter(web_tag=web_tag, env=env)
        _, owner_cplea_id_list, lock_cplea_id_list = get_lock_info_collections(user_id)

        result_set = []
        for model_obj in model_obj_list:
            # 该user id 存在的组 锁定的app
            if model_obj.id in owner_cplea_id_list:
                result_set.append([model_obj.app_name, False])
                continue
            # 其他组锁定的app
            if model_obj.id in lock_cplea_id_list:
                result_set.append([model_obj.app_name, True])
                continue
            # 未锁定的app
            result_set.append([model_obj.app_name, False])

        print(result_set)
        return Response(status=status.HTTP_200_OK, data=result_set)


class CodePublishUnlockPublishIp(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
        解锁发布IP
    """
    queryset = CodePublishWebControl.objects.all()
    serializer_class = CodePublishWebControlListSerializer
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        app_name = serializer.validated_data['app_name']
        env = serializer.validated_data['env']
        action = serializer.validated_data['action']
        model_obj = self.queryset.filter(app_name=app_name, env=env, action=action).order_by('-id').first()
        model_obj.is_done = 1
        model_obj.save()
        return Response(data={'code': 'ok'}, status=status.HTTP_200_OK)


# ############################# 环境锁 ###################################
class CodePublishEnvLockViewSet(mixins.ListModelMixin,
                                mixins.CreateModelMixin,
                                PureUpdateModelMixin,
                                viewsets.GenericViewSet):
    """
    list:
        获取env lock list
    create:
        创建环境锁
    update:
        更新环境锁
    """
    queryset = CodePublishLockEnv.objects.all()
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)

    def get_serializer_class(self):
        if self.action == 'list':
            return CodePublishEnvLockListSerializer

        if self.action == 'create':
            return CodePublishEnvLockCreateSerializer

        if self.action == 'update':
            return CodePublishEnvLockCreateSerializer

    def perform_create(self, serializer):
        with transaction.atomic():
            # 0 分钟定义为长期锁
            if serializer.validated_data['lock_time'] == 0:
                serializer.validated_data['expired'] = datetime.datetime.now() + datetime.timedelta(
                    days=3650)
            else:
                serializer.validated_data['expired'] = datetime.datetime.now() + datetime.timedelta(
                    minutes=serializer.validated_data['lock_time'])
            serializer.validated_data['user_ids'] = json.dumps(serializer.validated_data['user_ids'])
            serializer.validated_data['app_ids'] = json.dumps(serializer.validated_data['app_ids'])
            model_obj = serializer.save()
            for app_id in json.loads(serializer.validated_data['app_ids']):
                CodePublishLockEnvApp.objects.update_or_create(
                    app_name_id=app_id,
                    lock_grp_id=model_obj.id
                )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer.validated_data['user_ids'] = json.dumps(serializer.validated_data['user_ids'])
            serializer.validated_data['app_ids'] = json.dumps(serializer.validated_data['app_ids'])
            # 增加或减少锁定时间
            if serializer.validated_data['lock_time'] != instance.lock_time:
                serializer.validated_data['expired'] = instance.created + datetime.timedelta(
                    minutes=serializer.validated_data['lock_time'])
            model_obj = serializer.save()
            CodePublishLockEnvApp.objects.filter(lock_grp_id=model_obj.id).delete()
            for app_id in json.loads(serializer.validated_data['app_ids']):
                CodePublishLockEnvApp.objects.update_or_create(
                    app_name_id=app_id,
                    lock_grp_id=model_obj.id
                )
        return Response(serializer.data)


class CodePublishEnvUnLockViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    destroy:
        解锁环境
    """
    queryset = CodePublishLockEnv.objects.all()
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW, perms.IsReleaseEnvLock)

    def perform_destroy(self, instance):
        with transaction.atomic():
            CodePublishLockEnvApp.objects.filter(lock_grp_id=instance.id).delete()
            instance.delete()


class CodePublishEnvLockChoseEnvApp(mixins.ListModelMixin,
                                    mixins.RetrieveModelMixin,
                                    viewsets.GenericViewSet):
    """
    list:
        根据env获取对应的建锁app列表
    retrieve:
        根据组返回已绑定的app
    """
    queryset = CodePublishLockEnv.objects.all()
    permission_classes = (permissions.IsAuthenticated, perms.IsPagePermissionRW)
    filter_fields = ('env',)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        owner_cplea_id_list = [obj.app_name_id for obj in
                               CodePublishLockEnvApp.objects.filter(lock_grp_id=instance.id)]
        return Response(status=status.HTTP_200_OK, data=owner_cplea_id_list)

    def list(self, request, *args, **kwargs):
        env = request.query_params['env']
        model_obj_list = CodePublishMainConf.objects.filter(env=env)
        user_id = self.request.user.id
        _, owner_cplea_id_list, lock_cplea_id_list = get_lock_info_collections(user_id, creator=True)
        result_set = []
        for model_obj in model_obj_list:
            # 该user id 存在的组 锁定的app
            if model_obj.id in owner_cplea_id_list:
                result_set.append({'key': model_obj.id, 'label': model_obj.app_name, 'disabled': False})
                continue
            # 其他组锁定的app
            if model_obj.id in lock_cplea_id_list:
                result_set.append({'key': model_obj.id, 'label': model_obj.app_name, 'disabled': True})
                continue
            # 未锁定的app
            result_set.append({'key': model_obj.id, 'label': model_obj.app_name, 'disabled': False})

        return Response(status=status.HTTP_200_OK, data=result_set)
