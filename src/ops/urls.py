"""ops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
# 正式api
from users.views import (
    UsersLoginViewSet,
    UsersRegisterViewSet,
    UsersOperationsViewSet,
    UsersChangePasswordViewSet,
    UsersGroupViewSet,
    UsersAddViewSet,
    PersonalInfoViewSet,
    PersonalChangePasswordViewSet,
    UsersOpenViewSet,
)
from permission.views import (
    CheckPagePermissionCheckViewSet,
    PermissionGroupViewSet,
)
from operation.views import (
    GlobalOperatingLogViewSet,
    MessageMailLogViewSet,
    GlobalSearchViewSet,
)
from message.views import (
    InnerMessageViewSet,
    InnerMessageUnreadCountViewSet,
    InnerMessageOperationViewSet,
    MessagePushViewSet,
)
from common.views import (
    CommonSettingMessageViewSet,
    CommonSettingMessageTestViewSet,
    CommonSettingCmdbViewSet,
    CommonSettingAppViewSet,
    CommonSettingSshProxyViewSet,
    CommonSettingCodePublishViewSet,
)
from cmdb.cloud.views import (
    AliyunKeyViewSet,
    AliyunECSViewSet,
    AliyunEcsAutoViewSet,
    AliyunGraphViewSet,
    AliyunEcsClassfiyViewSet,
    AliyunKey2ECsViewSet,
    AliyunEcsAppRelViewSet,
    AliyunRdsClassfiyViewSet,
    AliyunRdsGraphViewSet,
    AliyunKey2RdsViewSet,
    AliyunRdsProcessListViewSet,
)
from cmdb.native.views import (
    NativeHostViewSet,
    NativeClassifyViewSet,
    NativeHostAppsRelViewSet,
    NativeHostGraphViewSet,
    NativeHostGraphCounterViewSet,
)
from cmdb.cmdb_common.views import (
    TagsViewSet,
    TagsAliyunEcsRelViewSet,
    TagsNativeHostRelViewSet,
    AnisbleUpdateHostInfoViewSet,
    AnsibleAddHostInfoViewSet,
    AllHostViewSet,
)
from apps.views import (
    AppDetailViewSet,
    AppHostRelViewSet,
    AppAliveUrlookerViewSet,
)
from monitor.views import (
    MonitorAppAliveGraphViewSet,
    MonitorAppAliveLatestDataViewSet,
    MonitorAppAliveTactics,
    MonitorThirdPartyStrategyViewSet,
    MonitorTPGraphViewSet,
    MonitorUpdateTPView,
    MonitorTPDomainViewSet,
    MonitorTPECSViewSet,
    MonitorTPNASViewSet,
    MonitorTPRDSViewSet,
    MonitorTPTencentSmsViewSet,
    MonitorTPVpnViewSet,
    MonitorTPXunChengEryaosuViewSet,
    MonitorTPWanweiyiyuanBankIdentityViewSet,
    MonitorTPYueXinSmsViewSet,
    MonitorThirdPartyJitterStrategyViewSet,
    MonitorTPBaseStrategyItemView,
    MonitorTPJitterStrategyItemView,
    MonitorDockerAppGraphViewSet,
)
from activity.business.views import (
    AccessAlarmStrategyViewSet,
    AccessAlarmAvgViewSet,
)
from openapi.views import (
    OpenApiFalconAlarmViewSet,
    OpenApiMysqlQueryViewSet,
    OpenApiAnsibleHostViewSet,
    OpenApiAliyunSLBCtrlViewSet
)
from code_publish.views import (
    CodePublishMainConfViewSet,
    CodePublishStatusViewSet,
    CodePublishWebMainConfViewSet,
    CodePublishWebDockerfileViewSet,
    CodePublishWebDockerOptsViewSet,
    CodePublishWebJarOptsViewSet,
    CodePublishWebStepsOptsViewSet,
    CodePublishWebJavaOptsViewSet,
    CodePublishWebMvnOptsViewSet,
    CodePublishWebGradleOptsViewSet,
    CodePublishEnvViewSet,
    CodePublishReplaceIpViewSet,
    CodePublishCopyConfigViewSet,
    CodePublishSetStepsViewSet,
    CodePublishAppDetailViewSet,
    CodePublishControlAppDetailViewSet,
    CodePublishTaskStatusViewSet,
    CodePublishControlViewSet,
    CodePublishStopBuildViewSet,
    CodePublishCheckCodeBranch,
    CodePublishBatchCopyConfigViewSet,
    CodePublishHasBeenPublishedViewSet,
    CodePublishGetRTSteps,
    CodePublishRTTaskStatusViewSet,
    CodePublishAlreadyPublishedVerViewSet,
    CodePublishAppEndpointViewSet,
    CodePublishUnlockPublishIp,
    CodePublishMainConfAppDetailViewSet,
    CodePublishEnvLockViewSet,
    CodePublishEnvUnLockViewSet,
    CodePublishEnvLockChoseEnvApp
)

# 测试api
from message.tests import (
    TestSenderView
)
from cmdb.cloud.tests import (
    TestAliyunEcsViewSet,
    TestAliyunGraphViewSet,
)
from cmdb.cmdb_common.tests import (
    TestAnsibleUpdateCron,
    TestAliyunUpdateCron,
)
from activity.business.tests import (
    TestAccessAlarmStrategyView,
)
from monitor.tests import (
    TestThirdPartySaveDataViewSet,
    TestPushDataToFalcon,
    TestTPPushJitterData,
)
from code_publish.tests import (
    TestCodePublishCron,
)
from common.tests import (
    TestGetAppAliveStatistics,
)

router_v1 = DefaultRouter()
api_v1_prefix = '^api/v1/'
# 用于ApiView，但是尽量使用ViewSet来定义api (基础代码中有足够的参考)
router_v1_view_urls = []
"""
以下url还没完全明确如何规范，暂时的想法: f'^{app_name}/[{target_range}|{target}]/target'
至于需要连写直接使用横杠即可，如 users/change-passwd
"""

# 用户相关
router_v1.register(r'^users/register', UsersRegisterViewSet, base_name='users_register')
router_v1.register(r'^users/login', UsersLoginViewSet, base_name='users_login')
router_v1.register(r'^users/operations', UsersOperationsViewSet, base_name='users_operations')
router_v1.register(r'^users/change-passwd', UsersChangePasswordViewSet, base_name='users_changePassword')
router_v1.register(r'^users/group', UsersGroupViewSet, base_name='users_group')
router_v1.register(r'^users/add', UsersAddViewSet, base_name='users_add')
router_v1.register(r'^users/open', UsersOpenViewSet, base_name='users_open_list')

# 个人信息相关
router_v1.register(r'^personal/info', PersonalInfoViewSet, base_name='personal_info')
router_v1.register(r'^personal/password', PersonalChangePasswordViewSet, base_name='personal_password')

# 权限相关
router_v1.register(r'^permission/page/check', CheckPagePermissionCheckViewSet, base_name='permission_page_check')
router_v1.register(r'^permission/group', PermissionGroupViewSet, base_name='permission_group')

# 操作记录相关
router_v1.register(r'^operation/log/global', GlobalOperatingLogViewSet, base_name='operation_log_global')
router_v1.register(r'^operation/log/message/mail', MessageMailLogViewSet, base_name='op_log_message_mail')
# 全局搜索
router_v1.register(r'^operation/global-search', GlobalSearchViewSet, base_name='operation_global_search')

# 消息相关
router_v1.register(r'^message/inner', InnerMessageViewSet, base_name='inner_message')
router_v1.register(r'^message/count', InnerMessageUnreadCountViewSet, base_name='inner_message_unread_count')
router_v1.register(r'^message/operation', InnerMessageOperationViewSet, base_name='inner_message_operation')
router_v1.register(r'^message/push', MessagePushViewSet, base_name='message_push')

# 通用设置相关
router_v1.register(r'^common/setting/message', CommonSettingMessageViewSet, base_name='common_setting_message')
router_v1.register(r'^common/setting/message/test', CommonSettingMessageTestViewSet,
                   base_name='common_setting_message_mail_test')
router_v1.register(r'^common/setting/cmdb', CommonSettingCmdbViewSet, base_name='common_setting_cmdb')
router_v1.register(r'^common/setting/app', CommonSettingAppViewSet, base_name='common_setting_app')
router_v1.register(r'^common/setting/ssh-proxy', CommonSettingSshProxyViewSet, base_name='common_setting_sshProxy')
router_v1.register(r'^common/setting/code-publish', CommonSettingCodePublishViewSet,
                   base_name='common_setting_codePublish')

# cmdb Aliyun 相关
router_v1.register(r'^cmdb/aliyun/keys', AliyunKeyViewSet, base_name='cmdb_aliyun_keys')
router_v1.register(r'^cmdb/aliyun/ecs', AliyunECSViewSet, base_name='cmdb_aliyun_ecs')
router_v1.register(r'^cmdb/aliyun/ecs-auto', AliyunEcsAutoViewSet, base_name='cmdb_aliyun_ecsAuto')
router_v1.register(r'^cmdb/aliyun/graph', AliyunGraphViewSet, base_name='cmdb_aliyun_graph')
router_v1.register(r'^cmdb/aliyun/classify', AliyunEcsClassfiyViewSet, base_name='cmdb_aliyun_classify')
router_v1.register(r'^cmdb/aliyun/key2ecs', AliyunKey2ECsViewSet, base_name='cmdb_aliyun_key2ecs')
router_v1.register(r'^cmdb/aliyun/rel/ecs-app', AliyunEcsAppRelViewSet, base_name='cmdb_aliyun_rel_ecsApp')
router_v1.register(r'^cmdb/aliyun/rds/classify', AliyunRdsClassfiyViewSet, base_name='cmdb_aliyun_rds_classify')
router_v1.register(r'^cmdb/aliyun/rds/graph', AliyunRdsGraphViewSet, base_name='cmdb_aliyun_rds_graph')
router_v1.register(r'^cmdb/aliyun/key2rds', AliyunKey2RdsViewSet, base_name='cmdb_aliyun_key2rds')
router_v1.register(r'^cmdb/aliyun/rds/processlist', AliyunRdsProcessListViewSet,
                   base_name='cmdb_aliyun_rds_processlist')

# cmdb native 相关
router_v1.register(r'^cmdb/native/host', NativeHostViewSet, base_name='cmdb_native_host')
router_v1.register(r'^cmdb/native/classify', NativeClassifyViewSet, base_name='cmdb_native_classify')
router_v1.register(r'^cmdb/native/rel/host-app', NativeHostAppsRelViewSet, base_name='cmdb_native_rel_hostApp')
router_v1.register(r'^cmdb/native/graph', NativeHostGraphViewSet, base_name='cmdb_native_graph')
router_v1.register(r'^cmdb/native/graph-counter', NativeHostGraphCounterViewSet, base_name='cmdb_native_graphCounter')

# cmdb tag相关
router_v1.register(r'^cmdb/tags', TagsViewSet, base_name='cmdb_native_tags')
router_v1.register(r'^cmdb/tags-rel/aliyun-ecs', TagsAliyunEcsRelViewSet, base_name='cmdb_aliyunEcs_rel')
router_v1.register(r'^cmdb/tags-rel/native-host', TagsNativeHostRelViewSet, base_name='cmdb_nativeHost_rel')

# cmdb ansible Api 相关
router_v1.register(r'^cmdb/ansible/update', AnisbleUpdateHostInfoViewSet, base_name='cmdb_ansible_update')
router_v1.register(r'^cmdb/ansible/add', AnsibleAddHostInfoViewSet, base_name='cmdb_ansible_add')

# cmdb 通用
router_v1.register(r'^cmdb/common/all-hosts', AllHostViewSet, base_name='cmdb_common_all_hosts')

# app 相关
router_v1.register(r'^app/detail', AppDetailViewSet, base_name='app_detail')
router_v1.register(r'^app/rel/host', AppHostRelViewSet, base_name='app_host_rel')
router_v1.register(r'^app/alive/urlooker', AppAliveUrlookerViewSet, base_name='app_alive_urlooker')

# monitor 相关
router_v1.register(r'^monitor/app/alive-graph', MonitorAppAliveGraphViewSet, base_name='monitor_app_alive')
router_v1.register(r'^monitor/app/alive-data/latest', MonitorAppAliveLatestDataViewSet,
                   base_name='monitor_app_alive_latest_data')
router_v1.register(r'^monitor/app/tactics', MonitorAppAliveTactics, base_name='monitor_app_tactics')
router_v1.register(r'^monitor/third-party/strategy', MonitorThirdPartyStrategyViewSet, base_name='monitor_tp_strategy')
router_v1.register(r'^monitor/third-party/graph', MonitorTPGraphViewSet, base_name='monitor_tp_graph')
router_v1.register(r'^monitor/third-party/info/ecs', MonitorTPECSViewSet, base_name='monitor_tp_info_ecs')
router_v1.register(r'^monitor/third-party/info/rds', MonitorTPRDSViewSet, base_name='monitor_tp_info_rds')
router_v1.register(r'^monitor/third-party/info/nas', MonitorTPNASViewSet, base_name='monitor_tp_info_nas')
router_v1.register(r'^monitor/third-party/info/domain', MonitorTPDomainViewSet, base_name='monitor_tp_info_domain')
router_v1.register(r'^monitor/third-party/info/vpn', MonitorTPVpnViewSet, base_name='monitor_tp_info_vpn')
router_v1.register(r'^monitor/third-party/info/yuexin-sms', MonitorTPYueXinSmsViewSet,
                   base_name='monitor_tp_info_yuexin_sms')
router_v1.register(r'^monitor/third-party/info/xuncheng-eryaosu', MonitorTPXunChengEryaosuViewSet,
                   base_name='monitor_tp_info_xuncheng_eryaosu')
router_v1.register(r'^monitor/third-party/info/wanweiyiyuan-bankidentity', MonitorTPWanweiyiyuanBankIdentityViewSet,
                   base_name='monitor_tp_info_wanweiyiyuan_bankIdentity')
router_v1.register(r'^monitor/third-party/info/tencent-sms', MonitorTPTencentSmsViewSet,
                   base_name='monitor_tp_info_tencent_sms')
router_v1.register(r'^monitor/third-party/jitter-strategy', MonitorThirdPartyJitterStrategyViewSet,
                   base_name='monitor_tp_jitter_strategy')
monitor_update_tp_url = url(
    f'{api_v1_prefix}monitor/third-party/data',
    MonitorUpdateTPView.as_view(), name="monitor_update_tp")
monitor_tp_base_item_url = url(
    f'{api_v1_prefix}monitor/third-party/item/strategy-base',
    MonitorTPBaseStrategyItemView.as_view(), name="monitor_tp_item_strategyBase")
monitor_tp_jitter_item_url = url(
    f'{api_v1_prefix}monitor/third-party/item/strategy-jitter',
    MonitorTPJitterStrategyItemView.as_view(), name="monitor_tp_item_jitterBase")
router_v1.register(r'^monitor/docker/graph', MonitorDockerAppGraphViewSet, base_name="monitor_docker_graph")

# business 业务相关
router_v1.register(r'^business/access-alarm/strategy',
                   AccessAlarmStrategyViewSet,
                   base_name='business_access_alarm_strategy')
router_v1.register(r'^business/access-alarm/avg', AccessAlarmAvgViewSet, base_name='business_access_alarm_ayg')

# open api 相关
router_v1.register(r'^openapi/falcon/alarm', OpenApiFalconAlarmViewSet, base_name='openapi_falcon_alarm')
router_v1.register(r'^openapi/mysql/excute', OpenApiMysqlQueryViewSet, base_name='openapi_mysql_excute')
router_v1.register(r'^openapi/ansible/host', OpenApiAnsibleHostViewSet, base_name='openapi_ansible_host')
router_v1.register(r'^openapi/aliyun/lbs', OpenApiAliyunSLBCtrlViewSet, base_name='openapi_aliyun_lbs')

# code_publish
router_v1.register(r'^code-publish/get/main-conf', CodePublishMainConfViewSet, base_name='code_publish_main_conf')
router_v1.register(r'^code-publish/status', CodePublishStatusViewSet, base_name='code_publish_status')
router_v1.register(r'^code-publish/web/main-conf', CodePublishWebMainConfViewSet,
                   base_name='code_publish_web_main_conf')
router_v1.register(r'^code-publish/web/steps', CodePublishWebStepsOptsViewSet, base_name='code_publish_steps_opts')
router_v1.register(r'^code-publish/web/jar-opts', CodePublishWebJarOptsViewSet, base_name='code_publish_jar_opts')
router_v1.register(r'^code-publish/web/java-opts', CodePublishWebJavaOptsViewSet, base_name='cp_java_opts')
router_v1.register(r'^code-publish/web/docker-opts', CodePublishWebDockerOptsViewSet, base_name='cp_docker_opts')
router_v1.register(r'^code-publish/web/dockerfile', CodePublishWebDockerfileViewSet, base_name='cp_dockerfile')
router_v1.register(r'^code-publish/web/mvn-opts', CodePublishWebMvnOptsViewSet, base_name='cp_mvn_opts')
router_v1.register(r'^code-publish/web/gradle-opts', CodePublishWebGradleOptsViewSet, base_name='cp_gradle_opts')
router_v1.register(r'^code-publish/web/env', CodePublishEnvViewSet, base_name='cp_web_env')
router_v1.register(r'^code-publish/web/replace-ip', CodePublishReplaceIpViewSet, base_name='cp_web_replaceIp')
router_v1.register(r'^code-publish/web/copy-conf', CodePublishCopyConfigViewSet, base_name='cp_web_copyConf')
router_v1.register(r'^code-publish/web/setting/steps', CodePublishSetStepsViewSet, base_name='cp_setting_setSteps')
router_v1.register(r'^code-publish/web/app-detail', CodePublishAppDetailViewSet, base_name='cp_appDetail')
router_v1.register(r'^code-publish/web/control/app-detail', CodePublishControlAppDetailViewSet,
                   base_name='cp_control_app_detail')
router_v1.register(r'^code-publish/web/control/main-conf', CodePublishMainConfAppDetailViewSet,
                   base_name='cp_control_mainConf')
router_v1.register(r'^code-publish/web/control/task-status', CodePublishTaskStatusViewSet,
                   base_name='cp_ctrl_taskStatus')
router_v1.register(r'^code-publish/web/control/main', CodePublishControlViewSet, base_name='cp_control_main')
router_v1.register(r'^code-publish/web/stop-building', CodePublishStopBuildViewSet, base_name='cp_stopBuilding')
router_v1.register(r'^code-publish/web/get-branch', CodePublishCheckCodeBranch, base_name='cp_getBranch')
router_v1.register(r'^code-publish/web/batch/copy-config', CodePublishBatchCopyConfigViewSet,
                   base_name='cp_batch_copyConfig')
router_v1.register(r'^code-publish/web/has-been-published', CodePublishHasBeenPublishedViewSet,
                   base_name='cp_hasBeenPublished')
router_v1.register(r'^code-publish/web/real-time/steps', CodePublishGetRTSteps, base_name='cp_realTime_steps')
router_v1.register(r'^code-publish/web/real-time/task-status', CodePublishRTTaskStatusViewSet,
                   base_name='cp_realTime_taskStatus')
router_v1.register(r'^code-publish/web/already-version', CodePublishAlreadyPublishedVerViewSet,
                   base_name='cp_already_ver')
router_v1.register(r'^code-publish/web/app-name/endpoint', CodePublishAppEndpointViewSet,
                   base_name='cp_appName_endPoint')
router_v1.register(r'^code-publish/web/unlock/publish-ip', CodePublishUnlockPublishIp, base_name='cp_unlock_publishIp')
router_v1.register(r'^code-publish/web/lock-env', CodePublishEnvLockViewSet, base_name='cp_env_lock')
router_v1.register(r'^code-publish/web/unlock-env', CodePublishEnvUnLockViewSet, base_name='cp_env_unlock')
router_v1.register(r'^code-publish/web/lock-env-app', CodePublishEnvLockChoseEnvApp, base_name='cp_lock_env_app')


# 测试接口
router_v1.register(r'^test/aliyun/ecs', TestAliyunEcsViewSet, base_name='test_aliyun_ecs')
router_v1.register(r'^test/aliyun/ecs-graph', TestAliyunGraphViewSet, base_name='test_aliyun_ecs_graph')
router_v1.register(r'^test/cmdb/cron/ansible', TestAnsibleUpdateCron, base_name='test_ansible_update_cron')
router_v1.register(r'^test/cmdb/cron/aliyun', TestAliyunUpdateCron, base_name='test_aliyun_update_cron')
router_v1.register(r'^test/monitor/third-party/save-data', TestThirdPartySaveDataViewSet,
                   base_name='test_thirdParty_saveData')
router_v1.register(r'^test/monitor/third-party/push-data', TestPushDataToFalcon, base_name='test_thirdParty_pushData')
router_v1.register(r'^test/monitor/third-party/push-jitter-data', TestTPPushJitterData,
                   base_name='test_thirdParty_pushJitterData')
router_v1.register(r'^test/code-publish/cron', TestCodePublishCron, base_name='test_cp_cron')
router_v1.register(r'^test/common/collect-failed-point', TestGetAppAliveStatistics, base_name='common_failed_point')

# 生产的ApiView
router_v1_product_url = [
    monitor_update_tp_url,
    monitor_tp_base_item_url,
    monitor_tp_jitter_item_url,
]

test_url = [
    # 消息发送接口
    url(f'{api_v1_prefix}test/sender', TestSenderView.as_view(), name="test_sender"),
    url(f'{api_v1_prefix}test/business/ngx-access-alarm',
        TestAccessAlarmStrategyView.as_view(),
        name='test_business_alarm_strategy')
]

urlpatterns = [
    url(f'{api_v1_prefix}', include(router_v1.urls)),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^api/docs/', include_docs_urls(title="Shadow Ops"))
]

urlpatterns.extend(router_v1_view_urls)
urlpatterns.extend(router_v1_product_url)
urlpatterns.extend(test_url)
