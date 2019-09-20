<template>
  <div>
    <Form :label-width="120">
    <!-- 当新增页面权限时，需要在此添加新的选项 -->
    <Divider orientation="left" class="inner-divider-text">首页</Divider>
      <FormItem label="是否可见">
        <Checkbox v-model="homeCheck" disabled>是</Checkbox>
      </FormItem>
      <FormItem label="首页">
        <RadioGroup v-model="formData.home">
          <Radio label='0'>无</Radio>
          <Radio label='1'>只读</Radio>
          <Radio label='2'>读写</Radio>
        </RadioGroup>
      </FormItem>
    <Divider orientation="left" class="inner-divider-text">CMDB</Divider>
      <FormItem label="是否可见">
        <Checkbox v-model="formData.cmdb">是</Checkbox>
      </FormItem>
      <FormItem label="资源 (aliyun)">
        <RadioGroup v-model="formData.cmdb_aliyun_resource">
          <Radio label='0' >无</Radio>
          <Radio label='1'>只读</Radio>
          <Radio label='2'>读写</Radio>
        </RadioGroup>
      </FormItem>
      <FormItem label="监控 (aliyun)">
        <RadioGroup v-model="formData.cmdb_aliyun_monitor">
          <Radio label='0' >无</Radio>
          <Radio label='1'>只读</Radio>
          <Radio label='2'>读写</Radio>
        </RadioGroup>
      </FormItem>
      <FormItem label="资源 (native)">
        <RadioGroup v-model="formData.cmdb_native_resource">
          <Radio label='0' >无</Radio>
          <Radio label='1'>只读</Radio>
          <Radio label='2'>读写</Radio>
        </RadioGroup>
      </FormItem>
      <FormItem label="监控 (native)">
        <RadioGroup v-model="formData.cmdb_native_monitor">
          <Radio label='0' >无</Radio>
          <Radio label='1'>只读</Radio>
          <Radio label='2'>读写</Radio>
        </RadioGroup>
      </FormItem>
      <FormItem label="标签">
        <RadioGroup v-model="formData.cmdb_tag">
          <Radio label='0' >无</Radio>
          <Radio label='1'>只读</Radio>
          <Radio label='2'>读写</Radio>
        </RadioGroup>
      </FormItem>
    <Divider orientation="left" class="inner-divider-text">App</Divider>
    <FormItem label="是否可见">
      <Checkbox v-model="formData.app">是</Checkbox>
    </FormItem>
    <FormItem label="App管理">
      <RadioGroup v-model="formData.app_management">
        <Radio label='0' >无</Radio>
        <Radio label='1'>只读</Radio>
        <Radio label='2'>读写</Radio>
      </RadioGroup>
    </FormItem>
    <FormItem label="App Alive 监控">
      <RadioGroup v-model="formData.app_aliveMonitor">
        <Radio label='0' >无</Radio>
        <Radio label='1'>只读</Radio>
        <Radio label='2'>读写</Radio>
      </RadioGroup>
    </FormItem>
    <Divider orientation="left" class="inner-divider-text">代码发布</Divider>
    <FormItem label="是否可见">
      <Checkbox v-model="formData.code_publish">是</Checkbox>
    </FormItem>
    <FormItem label="发布">
      <RadioGroup v-model="formData.code_publish_issue">
        <Radio label='0' >无</Radio>
        <Radio label='1'>只读</Radio>
        <Radio label='2'>读写</Radio>
      </RadioGroup>
    </FormItem>
    <FormItem label="发布配置">
      <RadioGroup v-model="formData.code_publish_config">
        <Radio label='0' >无</Radio>
        <Radio label='1'>只读</Radio>
        <Radio label='2'>读写</Radio>
      </RadioGroup>
    </FormItem>
    <FormItem label="模版配置">
      <RadioGroup v-model="formData.code_publish_template">
        <Radio label='0' >无</Radio>
        <Radio label='1'>只读</Radio>
        <Radio label='2'>读写</Radio>
      </RadioGroup>
    </FormItem>
    <Divider orientation="left" class="inner-divider-text">监控中心</Divider>
    <FormItem label="是否可见">
      <Checkbox v-model="formData.monitor">是</Checkbox>
    </FormItem>
    <FormItem label="[业务监控] 服务监控 (第三方)">
      <RadioGroup v-model="formData.monitor_thirdParty">
        <Radio label='0' >无</Radio>
        <Radio label='1'>只读</Radio>
        <Radio label='2'>读写</Radio>
      </RadioGroup>
    </FormItem>
    <FormItem label="[Kibana 信息统计] Pre Access Nginx">
      <RadioGroup v-model="formData.monitor_kibana_preAccessNginx">
        <Radio label='0' >无</Radio>
        <Radio label='1'>只读</Radio>
        <Radio label='2'>读写</Radio>
      </RadioGroup>
    </FormItem>
    <FormItem label="Docker">
      <RadioGroup v-model="formData.monitor_docker">
        <Radio label='0' >无</Radio>
        <Radio label='1'>只读</Radio>
        <Radio label='2'>读写</Radio>
      </RadioGroup>
    </FormItem>
    <FormItem label="API质量监控 (业务)">
      <RadioGroup v-model="formData.monitor_business_apiQuality">
        <Radio label='0' >无</Radio>
        <Radio label='1'>只读</Radio>
        <Radio label='2'>读写</Radio>
      </RadioGroup>
    </FormItem>
    <Divider orientation="left" class="inner-divider-text">审计</Divider>
    <FormItem label="是否可见">
      <Checkbox v-model="formData.audit">是</Checkbox>
    </FormItem>
    <FormItem label="全局操作记录">
      <RadioGroup v-model="formData.audit_operationLog">
        <Radio label='0' >无</Radio>
        <Radio label='1'>只读</Radio>
        <Radio label='2'>读写</Radio>
      </RadioGroup>
    </FormItem>
    <FormItem label="消息日志">
      <RadioGroup v-model="formData.audit_messageLog">
        <Radio label='0' >无</Radio>
        <Radio label='1'>只读</Radio>
        <Radio label='2'>读写</Radio>
      </RadioGroup>
    </FormItem>
    <Divider orientation="left" class="inner-divider-text">全局设置</Divider>
      <FormItem label="是否可见">
        <Checkbox v-model="formData.setting">是</Checkbox>
      </FormItem>
      <FormItem label="通用设置">
        <RadioGroup v-model="formData.setting_commonSetting">
          <Radio label='0' >无</Radio>
          <Radio label='1'>只读</Radio>
          <Radio label='2'>读写</Radio>
        </RadioGroup>
      </FormItem>
      <FormItem label="用户管理">
        <RadioGroup v-model="formData.setting_user">
          <Radio label='0'>无</Radio>
          <Radio label='1'>只读</Radio>
          <Radio label='2'>读写</Radio>
        </RadioGroup>
      </FormItem>
      <FormItem label="权限组">
        <RadioGroup v-model="formData.setting_permissionGroup">
          <Radio label='0' >无</Radio>
          <Radio label='1'>只读</Radio>
          <Radio label='2'>读写</Radio>
        </RadioGroup>
      </FormItem>
      <FormItem label="消息推送">
        <RadioGroup v-model="formData.setting_sendMessage">
          <Radio label='0' >无</Radio>
          <Radio label='1'>只读</Radio>
          <Radio label='2'>读写</Radio>
        </RadioGroup>
      </FormItem>
    </Form>
  </div>
</template>
<script>
export default {
  name: 'm_page_perm',
  data () {
    return {
      // 可视一级目录，新目录需要添加
      visiblePerm: ['setting', 'audit', 'cmdb', 'app', 'monitor', 'code_publish'],
      homeCheck: true,
      formData: {
        home: '1',
        audit: '0',
        audit_operationLog: '0',
        audit_messageLog: '0',
        setting: '0',
        setting_user: '0',
        setting_permissionGroup: '0',
        setting_sendMessage: '0',
        setting_commonSetting: '0',
        cmdb: '0',
        cmdb_aliyun_resource: '0',
        cmdb_aliyun_monitor: '0',
        cmdb_native_resource: '0',
        cmdb_native_monitor: '0',
        cmdb_tag: '0',
        app: '0',
        app_management: '0',
        app_aliveMonitor: '0',
        code_publish: '0',
        code_publish_issue: '0',
        code_publish_config: '0',
        code_publish_template: '0',
        monitor: '0',
        monitor_thirdParty: '0',
        monitor_docker: '0',
        monitor_business_apiQuality: '0',
        monitor_kibana_preAccessNginx: '0'
      },
      groupId: ''
    }
  },
  props: [
    'mPagePermData',
    'saveSignal'
  ],
  watch: {
    mPagePermData () {
      this.groupId = this.mPagePermData['group_id']
      this.formData = this.mPagePermData['page_permission']
      for (var permName in this.formData) {
        if (this.visiblePerm.indexOf(permName) !== -1) {
          if (this.formData[permName] !== 0) {
            this.formData[permName] = true
          } else {
            this.formData[permName] = false
          }
        } else {
          this.formData[permName] = String(this.formData[permName])
        }
      }
    },
    saveSignal () {
      var commitFormData = {}
      for (var permName in this.formData) {
        if (this.visiblePerm.indexOf(permName) !== -1) {
          if (this.formData[permName]) {
            commitFormData[permName] = 1
          } else {
            commitFormData[permName] = 0
          }
        } else {
          commitFormData[permName] = parseInt(this.formData[permName])
        }
      }
      var retData = {
        'group_id': this.groupId,
        'page_permission': JSON.stringify(commitFormData)
      }
      this.$emit('setPagePerm', retData)
    }
  },
  methods: {
  }
}
</script>
<style  scoped>
.inner-divider-text {
  font-size: 13px;
  color: #464c5b;
  font-weight: normal;
}
.ivu-form-item {
  margin-bottom: 0;
}
</style>
