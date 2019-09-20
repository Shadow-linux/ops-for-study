<template>
  <div>
    <Modal
        v-model="ModalShow"
        title="页面权限"
        @on-ok="ok"
        @on-cancel="cancle"
        >
        <!-- 当新增页面权限时，需要在此添加新的选项 -->
        <Form :label-width="120" >
          <Divider orientation="left"  class="inner-divider-text">首页 <b class="none-perm-tag">( 可见 )</b></Divider>
          <FormItem label="首页"><span :class="{ 'rw-perm-tag': perm.home.rw,
           'ro-perm-tag': perm.home.ro,
           'none-perm-tag': perm.home.none
           }">{{ perm.home.tag }}</span>
          </FormItem>
          <Divider orientation="left" class="inner-divider-text">CMDB <b class="none-perm-tag">( {{ perm.cmdb.tag }} )</b></Divider>
          <FormItem label="资源 (aliyun)">
            <span :class="{ 'rw-perm-tag': perm.cmdb_aliyun_resource.rw,
              'ro-perm-tag': perm.cmdb_aliyun_resource.ro,
              'none-perm-tag': perm.cmdb_aliyun_resource.none
              }">{{ perm.cmdb_aliyun_resource.tag }}</span>
          </FormItem>
          <FormItem label="监控 (aliyun)">
            <span :class="{ 'rw-perm-tag': perm.cmdb_aliyun_monitor.rw,
              'ro-perm-tag': perm.cmdb_aliyun_monitor.ro,
              'none-perm-tag': perm.cmdb_aliyun_monitor.none
              }">{{ perm.cmdb_aliyun_monitor.tag }}</span>
          </FormItem>
          <FormItem label="资源 (native)">
            <span :class="{ 'rw-perm-tag': perm.cmdb_native_resource.rw,
              'ro-perm-tag': perm.cmdb_native_resource.ro,
              'none-perm-tag': perm.cmdb_native_resource.none
              }">{{ perm.cmdb_native_resource.tag }}</span>
          </FormItem>
          <FormItem label="监控 (native)">
            <span :class="{ 'rw-perm-tag': perm.cmdb_native_monitor.rw,
              'ro-perm-tag': perm.cmdb_native_monitor.ro,
              'none-perm-tag': perm.cmdb_native_monitor.none
              }">{{ perm.cmdb_native_monitor.tag }}</span>
          </FormItem>
          <FormItem label="标签">
            <span :class="{ 'rw-perm-tag': perm.cmdb_tag.rw,
              'ro-perm-tag': perm.cmdb_tag.ro,
              'none-perm-tag': perm.cmdb_tag.none
              }">{{ perm.cmdb_tag.tag }}</span>
          </FormItem>
          <Divider orientation="left" class="inner-divider-text">APP <b class="none-perm-tag">( {{ perm.app.tag }} )</b></Divider>
          <FormItem label="App管理">
            <span :class="{ 'rw-perm-tag': perm.app_management.rw,
              'ro-perm-tag': perm.app_management.ro,
              'none-perm-tag': perm.app_management.none
              }">{{ perm.app_management.tag }}</span>
          </FormItem>
          <FormItem label="App Alive 监控">
            <span :class="{ 'rw-perm-tag': perm.app_aliveMonitor.rw,
              'ro-perm-tag': perm.app_aliveMonitor.ro,
              'none-perm-tag': perm.app_aliveMonitor.none
              }">{{ perm.app_aliveMonitor.tag }}</span>
          </FormItem>
          <Divider orientation="left" class="inner-divider-text">代码发布 <b class="none-perm-tag">( {{ perm.code_publish.tag }} )</b></Divider>
          <FormItem label="发布">
            <span :class="{ 'rw-perm-tag': perm.code_publish_issue.rw,
              'ro-perm-tag': perm.code_publish_issue.ro,
              'none-perm-tag': perm.code_publish_issue.none
              }">{{ perm.code_publish_issue.tag }}</span>
          </FormItem>
          <FormItem label="发布配置">
            <span :class="{ 'rw-perm-tag': perm.code_publish_config.rw,
              'ro-perm-tag': perm.code_publish_config.ro,
              'none-perm-tag': perm.code_publish_config.none
              }">{{ perm.code_publish_config.tag }}</span>
          </FormItem>
          <FormItem label="模版配置">
            <span :class="{ 'rw-perm-tag': perm.code_publish_template.rw,
              'ro-perm-tag': perm.code_publish_template.ro,
              'none-perm-tag': perm.code_publish_template.none
              }">{{ perm.code_publish_template.tag }}</span>
          </FormItem>
          <Divider orientation="left" class="inner-divider-text">监控中心 <b class="none-perm-tag">( {{ perm.monitor.tag }} )</b></Divider>
          <FormItem label="[业务监控] 服务监控(第三方)">
            <span :class="{ 'rw-perm-tag': perm.monitor_thirdParty.rw,
              'ro-perm-tag': perm.monitor_thirdParty.ro,
              'none-perm-tag': perm.monitor_thirdParty.none
              }">{{ perm.monitor_thirdParty.tag }}</span>
          </FormItem>
          <FormItem label="[Kibana 信息统计] Pre Access Nginx">
            <span :class="{ 'rw-perm-tag': perm.monitor_kibana_preAccessNginx.rw,
              'ro-perm-tag': perm.monitor_kibana_preAccessNginx.ro,
              'none-perm-tag': perm.monitor_kibana_preAccessNginx.none
              }">{{ perm.monitor_kibana_preAccessNginx.tag }}</span>
          </FormItem>
          <FormItem label="Docker">
            <span :class="{ 'rw-perm-tag': perm.monitor_docker.rw,
              'ro-perm-tag': perm.monitor_docker.ro,
              'none-perm-tag': perm.monitor_docker.none
              }">{{ perm.monitor_docker.tag }}</span>
          </FormItem>
          <FormItem label="API质量监控 (业务)">
            <span :class="{ 'rw-perm-tag': perm.monitor_business_apiQuality.rw,
              'ro-perm-tag': perm.monitor_business_apiQuality.ro,
              'none-perm-tag': perm.monitor_business_apiQuality.none
              }">{{ perm.monitor_business_apiQuality.tag }}</span>
          </FormItem>
          <Divider orientation="left" class="inner-divider-text">审计 <b class="none-perm-tag">( {{ perm.audit.tag }} )</b></Divider>
          <FormItem label="全局操作记录">
            <span :class="{ 'rw-perm-tag': perm.audit_operationLog.rw,
              'ro-perm-tag': perm.audit_operationLog.ro,
              'none-perm-tag': perm.audit_operationLog.none
              }">{{ perm.audit_operationLog.tag }}</span>
          </FormItem>
          <FormItem label="消息日志">
            <span :class="{ 'rw-perm-tag': perm.audit_messageLog.rw,
              'ro-perm-tag': perm.audit_messageLog.ro,
              'none-perm-tag': perm.audit_messageLog.none
              }">{{ perm.audit_messageLog.tag }}</span>
          </FormItem>
          <Divider orientation="left" class="inner-divider-text">全局设置 <b class="none-perm-tag">( {{ perm.setting.tag }} )</b></Divider>
          <FormItem label="通用设置">
            <span :class="{ 'rw-perm-tag': perm.setting_commonSetting.rw,
              'ro-perm-tag': perm.setting_commonSetting.ro,
              'none-perm-tag': perm.setting_commonSetting.none
              }">{{ perm.setting_commonSetting.tag }}</span>
          </FormItem>
          <FormItem label="用户管理">
            <span :class="{ 'rw-perm-tag': perm.setting_user.rw,
            'ro-perm-tag': perm.setting_user.ro,
            'none-perm-tag': perm.setting_user.none
            }">{{ perm.setting_user.tag }}</span>
          </FormItem>
          <FormItem label="权限组">
            <span :class="{ 'rw-perm-tag': perm.setting_permissionGroup.rw,
              'ro-perm-tag': perm.setting_permissionGroup.ro,
              'none-perm-tag': perm.setting_permissionGroup.none
              }">{{ perm.setting_permissionGroup.tag }}</span>
          </FormItem>
          <FormItem label="消息推送">
            <span :class="{ 'rw-perm-tag': perm.setting_sendMessage.rw,
              'ro-perm-tag': perm.setting_sendMessage.ro,
              'none-perm-tag': perm.setting_sendMessage.none
              }">{{ perm.setting_sendMessage.tag }}</span>
          </FormItem>
        </Form>
    </Modal>
  </div>
</template>
<script>

export default {
  name: 'page_perm_modal',
  data () {
    return {
      // home 是不需要放在visiblePerm里，因为home是永远可见
      visiblePerm: ['setting', 'audit', 'cmdb', 'app', 'monitor', 'code_publish'],
      perm: {
        home: { tag: '无', ro: false, rw: false, none: true },
        setting: { tag: '无', ro: false, rw: false, none: true },
        setting_user: { tag: '无', ro: false, rw: false, none: true },
        setting_permissionGroup: { tag: '无', ro: false, rw: false, none: true },
        setting_sendMessage: { tag: '无', ro: false, rw: false, none: true },
        setting_commonSetting: { tag: '无', ro: false, rw: false, none: true },
        audit: { tag: '无', ro: false, rw: false, none: true },
        audit_operationLog: { tag: '无', ro: false, rw: false, none: true },
        audit_messageLog: { tag: '无', ro: false, rw: false, none: true },
        cmdb: { tag: '无', ro: false, rw: false, none: true },
        cmdb_aliyun_resource: { tag: '无', ro: false, rw: false, none: true },
        cmdb_aliyun_monitor: { tag: '无', ro: false, rw: false, none: true },
        cmdb_native_resource: { tag: '无', ro: false, rw: false, none: true },
        cmdb_native_monitor: { tag: '无', ro: false, rw: false, none: true },
        cmdb_tag: { tag: '无', ro: false, rw: false, none: true },
        app: { tag: '无', ro: false, rw: false, none: true },
        app_management: { tag: '无', ro: false, rw: false, none: true },
        app_aliveMonitor: { tag: '无', ro: false, rw: false, none: true },
        code_publish: { tag: '无', ro: false, rw: false, none: true },
        code_publish_issue: { tag: '无', ro: false, rw: false, none: true },
        code_publish_config: { tag: '无', ro: false, rw: false, none: true },
        code_publish_template: { tag: '无', ro: false, rw: false, none: true },
        monitor: { tag: '无', ro: false, rw: false, none: true },
        monitor_thirdParty: { tag: '无', ro: false, rw: false, none: true },
        monitor_docker: { tag: '无', ro: false, rw: false, none: true },
        monitor_business_apiQuality: { tag: '无', ro: false, rw: false, none: true },
        monitor_kibana_preAccessNginx: { tag: '无', ro: false, rw: false, none: true }
      }
    }
  },
  props: [
    'pagePermModal',
    'groupPermObj'
  ],
  watch: {
    groupPermObj () {
      var permsObj = this.groupPermObj['page_permission']
      for (var pname in permsObj) {
        if (this.visiblePerm.indexOf(pname) === -1) {
          this.permHandle(pname, permsObj[pname])
        } else {
          this.visiblePermHandle(pname, permsObj[pname])
        }
      }
    }
  },
  computed: {
    ModalShow: {
      get () {
        return this.pagePermModal
      },
      set (val) {
        this.$emit('switchPagePermModal', val)
      }
    }
  },
  methods: {
    visiblePermHandle (name, perm) {
      switch (perm) {
        case 0:
          this.perm[name] = { tag: '不可见', ro: false, rw: false, none: true }
          break
        default:
          this.perm[name] = { tag: '可见', ro: false, rw: false, none: true }
          break
      }
    },
    permHandle (name, perm) {
      switch (perm) {
        case 0:
          this.perm[name] = { tag: '无', ro: false, rw: false, none: true }
          break
        case 1:
          this.perm[name] = { tag: '只读', ro: true, rw: false, none: false }
          break
        case 2:
          this.perm[name] = { tag: '读写', ro: false, rw: true, none: false }
          break
        default:
          this.perm[name] = { tag: '无', ro: false, rw: false, none: true }
          break
      }
    },
    ok () {
    },
    cancle () {
    }
  }
}
</script>
<style  scoped>
.inner-divider-text {
  font-size: 13px;
  color: #515a6e;
}
.rw-perm-tag {
  margin-left: 15px; font-size: 12px; color: #ed4014
}
.ro-perm-tag {
  margin-left: 15px; font-size: 12px; color: #19be6b
}
.none-perm-tag {
  margin-left: 15px; font-size: 12px; color: #808695
}
.ivu-form-item {
  margin: 0;
}
</style>
