from django.db import models


# Create your models here.

class CodePublishEnvMainConf(models.Model):
    env = models.CharField(max_length=128, null=True, unique=True)

    def __str__(self):
        return f'<CodePublishEnvMainConf {self.env}>'

    class Meta:
        db_table = 'cp_env_main_conf'


class CodePublishMainConf(models.Model):
    app_name = models.CharField(max_length=64, null=True)
    env = models.CharField(max_length=128, null=True)
    publish_ip = models.CharField(max_length=256, null=True, help_text='list', default='[]')
    pkg_name = models.CharField(max_length=64, null=True)
    port = models.IntegerField(default=0)
    mvn_opts_id = models.IntegerField(default=0)
    java_opts_id = models.IntegerField(default=0)
    jar_opts_id = models.IntegerField(default=0)
    docker_opts_id = models.IntegerField(default=0)
    dockerfile_id = models.IntegerField(default=0)
    steps_id = models.IntegerField(default=0)
    gradle_opts_id = models.IntegerField(default=0)
    git_url = models.CharField(max_length=64, help_text='git url', null=True)
    jenkins_project = models.CharField(max_length=64, help_text='jenkins project', null=True)
    server_mode = models.CharField(max_length=64, help_text='[docker|tomcat|jar|tc2docker]', null=True)
    web_tag = models.CharField(max_length=32, help_text='web 平台标记是前端还是后端 [font-end|backend]', null=True)
    updated = models.DateTimeField(auto_now=True, help_text='更新时间', null=True)

    def __str__(self):
        return f'<CodePublishMainConf {self.app_name}>'

    class Meta:
        db_table = 'cp_main_conf'
        unique_together = ['app_name', 'env']


class CodePublishMvnOpts(models.Model):
    SUB_TYPE = 'mvn_opts'

    mvn_opts = models.TextField(null=True)
    name = models.CharField(max_length=256, null=True)

    def __str__(self):
        return f'<CodePublishMvnOpts {self.id}>'

    class Meta:
        db_table = 'cp_mvn_opts'


class CodePublishGradleOpts(models.Model):
    SUB_TYPE = 'gradle_opts'

    name = models.CharField(max_length=256, null=True)
    gradle_opts = models.TextField(null=True)

    def __str__(self):
        return f'<CodePublishGradleOpts {self.id}>'

    class Meta:
        db_table = 'cp_gradle_opts'


class CodePublishJavaOpts(models.Model):
    SUB_TYPE = 'java_opts'

    java_opts = models.TextField(null=True)
    name = models.CharField(max_length=256, null=True)

    def __str__(self):
        return f'<CodePublishJavaOpts {self.id}>'

    class Meta:
        db_table = 'cp_java_opts'


class CodePublishJarOpts(models.Model):
    SUB_TYPE = 'jar_opts'

    jar_opts = models.TextField(null=True)
    name = models.CharField(max_length=256, null=True)

    def __str__(self):
        return f'<CodePublishJarOpts {self.id}>'

    class Meta:
        db_table = 'cp_jar_opts'


class CodePublishSteps(models.Model):
    SUB_TYPE = 'steps'

    deploy_steps = models.CharField(max_length=256, null=True, default='[]')
    deploy_sync_steps = models.CharField(max_length=256, null=True, default='[]')
    rollback_steps = models.CharField(max_length=256, null=True, default='[]')
    name = models.CharField(max_length=256, null=True)

    def __str__(self):
        return f'<CodePublishStep {self.id}>'

    class Meta:
        db_table = 'cp_steps'


class CodePublishDockerOpts(models.Model):
    SUB_TYPE = 'docker_opts'

    docker_opts = models.TextField(null=True)
    name = models.CharField(max_length=256, null=True)

    def __str__(self):
        return f'<CodePublishDockerOpts {self.id}>'

    class Meta:
        db_table = 'cp_docker_opts'


class CodePublishDockerFile(models.Model):
    SUB_TYPE = 'dockerfile'

    dockerfile = models.TextField(null=True)
    name = models.CharField(max_length=256, null=True)

    def __str__(self):
        return f'<CodePublishDockerFile {self.id}>'

    class Meta:
        db_table = 'cp_dockerfile'


class CodePublishWebSetting(models.Model):
    publish_steps = models.CharField(max_length=256, null=True, help_text='部署步骤', default='[]')

    def __str__(self):
        return f'<CodePublishWebSetting {self.id}>'

    class Meta:
        db_table = 'cp_web_setting'


class CodePublishStatus(models.Model):

    IS_FINISH_CHOICE = [
        (0, 'unfinished'),
        (1, 'finished')
    ]

    app_name = models.CharField(max_length=64, null=True)
    env = models.CharField(max_length=32, null=True)
    publish_version = models.CharField(max_length=64, null=True)
    publish_ip = models.CharField(max_length=32, null=True)
    build_num = models.IntegerField(null=True)
    action = models.CharField(max_length=32, null=True, help_text='[deploy|rollback]')
    is_finished = models.SmallIntegerField(default=0, choices=IS_FINISH_CHOICE)
    stander_steps = models.CharField(max_length=256, null=True)
    upload_steps = models.CharField(max_length=256, null=True)
    updated = models.DateTimeField(auto_now=True, help_text='更新时间', null=True)
    created = models.DateTimeField(auto_now_add=True, help_text='更新时间', null=True)

    def __str__(self):
        return f'<CodePublishStatus {self.id}>'

    class Meta:
        db_table = 'cp_status'


class CodePublishWebControl(models.Model):

    STATUS_CHOICE = [
        (0, 'null'),
        (1, 'success'),
        (2, 'failure'),
        (3, 'building'),
        (4, 'aborted')
    ]
    IS_DONE_CHOICE = [
        (0, '未完成'),
        (1, '完成')
    ]

    app_name = models.CharField(max_length=64, null=True)
    env = models.CharField(max_length=32, null=True)
    action = models.CharField(max_length=32, null=True)
    jenkins_job = models.CharField(max_length=64, help_text='jenkins project', null=True)
    jenkins_params = models.CharField(max_length=512, help_text='jenkins params', null=True)
    publish_version = models.CharField(max_length=64, null=True, blank=True)
    build_num = models.IntegerField(default=0)
    publish_ip = models.CharField(max_length=32, null=True)
    status = models.SmallIntegerField(default=0, choices=STATUS_CHOICE)
    branch = models.CharField(max_length=128, null=True, blank=True)
    git_log = models.CharField(max_length=128, null=True, blank=True)
    console_url = models.CharField(max_length=256, null=True, help_text='查看console log')
    is_sync = models.SmallIntegerField(default=0)
    sync_env = models.CharField(max_length=32, null=True, blank=True)
    sync_ip = models.CharField(max_length=24, null=True, blank=True)
    is_done = models.SmallIntegerField(default=1, help_text='0: 该环境未完整发布, 1: 是完整发布', choices=IS_DONE_CHOICE)
    has_been_published = models.CharField(max_length=128, null=True, help_text='已经发布的IP; list', default='[]')
    creator = models.IntegerField(default=0, help_text='发布者')
    updated = models.DateTimeField(auto_now=True, help_text='更新时间', null=True)
    created = models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True)

    def __str__(self):
        return f'<CodePublishWebControl {self.id}>'

    class Meta:
        db_table = 'cp_web_control'


class CodePublishWebControlSteps(models.Model):

    task_id = models.IntegerField(default=0, help_text='task id')
    stander_steps = models.CharField(max_length=512, null=True, default='[]', help_text='stander steps')
    upload_steps = models.CharField(max_length=512, null=True, default='[]', help_text='upload steps')

    def __str__(self):
        return f'<CodePublishWebControlSteps {self.id}>'

    class Meta:
        db_table = 'cp_web_control_steps'


class CodePublishLockEnv(models.Model):

    lock_grp_name = models.CharField(max_length=128, null=True, help_text='组名')
    user_ids = models.CharField(max_length=256, null=True, default='[]', help_text='用户组')
    app_ids = models.CharField(max_length=256, null=True, default='[]', help_text='用户组')
    env = models.CharField(max_length=64, null=True, help_text='env')
    lock_time = models.IntegerField(default=60, help_text='锁定时间')
    creator = models.IntegerField(default=0, help_text='创建用户ID')
    created = models.DateTimeField(auto_now_add=True, help_text='创建时间', null=True)
    expired = models.DateTimeField(help_text='过期时间', null=True)

    def __str__(self):
        return f'<CodePublishLockEnv {self.id}>'

    class Meta:
        db_table = 'cp_lock_env'
        unique_together = ('creator', 'env')


class CodePublishLockEnvApp(models.Model):

    app_name_id = models.IntegerField(help_text='AppNameID from cp_main_conf', unique=True)
    lock_grp_id = models.IntegerField(default=0)

    def __str__(self):
        return f'<CodePublishLockEnvApp {self.id}>'

    class Meta:
        db_table = 'cp_lock_env_app'
