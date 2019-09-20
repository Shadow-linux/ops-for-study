<template>
  <div>
    <Modal
      v-model="createModal"
      @on-cancel="switchTaskModal"
      :mask-closable="false"
      title="创建发布任务"
      :styles="{top: '20px'}"
      >
      <!-- <Card v-show="createModal"> -->
        <!-- <p slot="title">创建发布任务</p> -->
        <Alert show-icon>什么是发布周期? 发布周期指的是该APP 其所属的IP上都发布了同一个版本称为一个周期。 PS: "<b style="color: red; font-size: 13x">*</b>" 号必填</Alert>
        <Tabs type="card" @on-click="handleEndpointChange">
          <TabPane label="Backend（后端）" name="backend">
            <Alert type="warning" show-icon v-show="backendReleaseWarn">现在您选择的环境为<b style="color: red">线上环境(Release)</b>, 请确认发布环境。</Alert>
            <Form ref="backendForm" :model="backendForm" :rules="ruleBackendForm" :label-width="100">
              <FormItem label="动作:" prop="action">
                <Select v-model="backendForm.action" style="width: 300px" @on-change="() => { backendAction = backendForm.action }">
                  <Option v-for="action in actionList" :value="action[0]" :key="action[0]">{{ action[1] }}
                    <span style="float:right;color:#ccc">{{ action[0] }}</span>
                  </Option>
                </Select>
              </FormItem>
              <FormItem label="环境:" prop="env">
                <Select v-model="backendForm.env" filterable style="width: 300px" @on-change="handleEnvChange">
                  <Option v-for="env in publishEnvList" :value="env" :key="env">{{ env }}</Option>
                </Select>
              </FormItem>
              <FormItem label="应用名:" prop="app_name">
                <Select v-model.trim="backendForm.app_name" filterable style="width: 300px"
                @on-change="handleAppNameChange" @on-open-change="handleOpenAppName">
                  <Option v-for="app in appNameBackendList" :value="app[0]" :key="app[0]" :disabled="app[1]">{{ app[0] }}
                    <!-- <span style="float:right;color:#ccc" v-show="app[1]">LOCK</span>
                    <span style="float:right;color:#ccc" v-show="!app[1]">UNLOCK</span> -->
                  </Option>
                </Select>
              </FormItem>
              <FormItem label="发布IP:" prop="ip">
                <Select v-model="backendForm.ip" style="width: 300px; margin-right: 10px" @on-open-change="handleHasBeenPublished">
                  <Option v-for="ip in publishIpList" :value="ip[0]" :key="ip[0]" :disabled="ip[1]">{{ ip[0] }}
                    <span style="float:right;color:#ccc" v-show="ip[1]">LOCK</span>
                    <span style="float:right;color:#ccc" v-show="!ip[1]">UNLOCK</span>
                  </Option>
                </Select>
                <Tooltip content="被锁定的IP，是发布周期内已发布的IP;" placement="left-start">
                  <Button type="default" size="small" icon="ios-unlock" :loading="unlockBtnLoading" @click="handleUnlockPublishIp">解锁</Button>
                </Tooltip>
              </FormItem>
              <FormItem label="分支:" prop="branch" v-show="backendAction !== 'Rollback'">
                <Select v-model="backendForm.branch" filterable style="width: 300px" placement="top">
                  <Option v-for="branch in branchList" :value="branch" :key="branch">{{ branch }}</Option>
                </Select>
              </FormItem>
              <FormItem label="历史版本:" prop="publish_version" v-show="backendAction === 'Rollback'">
                <Select v-model="backendForm.publish_version" style="width: 300px; margin-right: 10px" @on-open-change="handleAlreadyPublishVer">
                  <Option :value="version" v-for="(branch, version) in alreadyPublishVerList" :key="version">{{ version }}
                    <span style="float:right;color:#ccc">分支: {{ branch }}</span>
                  </Option>
                </Select>
                <Tooltip content="只显示2个发布周期完整的版本" placement="left-start">
                  <Icon type="ios-alert-outline" size="20"/>
                </Tooltip>
              </FormItem>
              <FormItem label="代码覆盖率:" prop="is_jacoco">
                <Checkbox v-model="backendForm.is_jacoco" @click="() => { backendForm.is_sync = !backendForm.is_jacoco }"> 是</Checkbox>
              </FormItem>
              <FormItem label="同步执行:" prop="is_sync">
                <Checkbox v-model="backendForm.is_sync" @on-change="() => {
                  backendForm.sync_env = ''
                  backendForm.sync_ip = ''
                }"> 是</Checkbox>
              </FormItem>
              <FormItem label="同步环境:" prop="sync_env" v-show="backendForm.is_sync">
                <Select v-model="backendForm.sync_env" filterable style="width: 300px" @on-change="handleSyncEnvChange" placement="top">
                  <Option v-for="env in publishEnvList" :value="env" :key="env">{{ env }}</Option>
                </Select>
              </FormItem>
              <FormItem label="同步环境IP:" prop="sync_ip" v-show="backendForm.is_sync">
                <Select v-model="backendForm.sync_ip"  style="width: 300px" placement="top">
                  <Option v-for="ip in syncPublishIpList" :value="ip[0]" :key="ip[0]">{{ ip[0] }}
                  </Option>
                </Select>
              </FormItem>
            </Form>
          </TabPane>
          <TabPane label="Frontend (前端)" name=frontend>
            <Alert type="warning" show-icon v-show="frontendReleaseWarn">现在您选择的环境为<b style="color: red">线上环境(Release)</b>, 请确认发布环境。</Alert>
            <Form :model="frontendForm" :label-width="110" ref="frontendForm" :rules="ruleFrontendForm">
              <FormItem label="动作:" prop="action" >
                <Select v-model="frontendForm.action" style="width: 300px" @on-change="() => { frontendAction = frontendForm.action }">
                  <Option v-for="action in actionList" :value="action[0]" :key="action[0]">{{ action[1] }}
                    <span style="float:right;color:#ccc">{{ action[0] }}</span>
                  </Option>
                </Select>
              </FormItem>
              <FormItem label="环境:" prop="env">
                <Select v-model="frontendForm.env" style="width: 300px" @on-change="handleEnvChange">
                  <Option v-for="env in publishEnvList" :value="env" :key="env">{{ env }}</Option>
                </Select>
              </FormItem>
              <FormItem label="应用名:" prop="app_name">
                <Select v-model.trim="frontendForm.app_name" filterable style="width: 300px"
                @on-change="handleAppNameChange" @on-open-change="handleOpenAppName">
                  <Option v-for="app in appNameBackendList" :value="app[0]" :key="app[0]" :disabled="app[1]">{{ app[0] }}
                    <!-- <span style="float:right;color:#ccc" v-show="app[1]">LOCK</span>
                    <span style="float:right;color:#ccc" v-show="!app[1]">UNLOCK</span> -->
                  </Option>
                </Select>
              </FormItem>
              <FormItem label="发布IP:" prop="ip">
                <Select v-model="frontendForm.ip"  style="width: 300px; margin-right: 10px" @on-open-change="handleHasBeenPublished">
                  <Option v-for="ip in publishIpList" :value="ip[0]" :key="ip[0]" :disabled="ip[1]">{{ ip[0] }}
                    <span style="float:right;color:#ccc" v-show="ip[1]">LOCK</span>
                    <span style="float:right;color:#ccc" v-show="!ip[1]">UNLOCK</span>
                  </Option>
                </Select>
                <Tooltip content="被锁定的IP，是发布周期内已发布的IP;" placement="left-start">
                  <Button type="default" size="small" icon="ios-unlock" :loading="unlockBtnLoading" @click="handleUnlockPublishIp">解锁</Button>
                </Tooltip>
              </FormItem>
              <FormItem label="分支:" prop="branch" v-show="frontendAction !== 'Rollback'">
                <Select v-model="frontendForm.branch" style="width: 300px" filterable  placement="top">
                  <Option v-for="branch in branchList" :value="branch" :key="branch">{{ branch }}</Option>
                </Select>
              </FormItem>
              <FormItem label="历史版本:" prop="publish_version" v-show="frontendAction === 'Rollback'">
                <Select v-model="frontendForm.publish_version" style="width: 300px; margin-right: 10px" @on-open-change="handleAlreadyPublishVer">
                  <Option :value="version" v-for="(branch, version) in alreadyPublishVerList" :key="version">{{ version }}
                    <span style="float:right;color:#ccc">分支: {{ branch }}</span>
                  </Option>
                </Select>
                <Tooltip content="只显示2个发布周期完整的版本" placement="left-start">
                  <Icon type="ios-alert-outline" size="20"/>
                </Tooltip>
              </FormItem>
              <!-- #版本号 前
              GitDiffBefore=${10}
              #版本号 后
              GitDiffAfter=${11} -->
              <!-- <FormItem label="对比版本前(PHP):" >
                <Checkbox v-model="frontendForm.git_diff_before" @click="() => { frontendForm.git_diff_before = !frontendForm.git_diff_before }"> 是</Checkbox>
              </FormItem>
              <FormItem label="对比版本后(PHP):">
                <Checkbox v-model="frontendForm.git_diff_after" @click="() => { frontendForm.git_diff_after = !frontendForm.git_diff_after }"> 是</Checkbox>
              </FormItem> -->
              <FormItem label="同步执行:" prop="is_sync">
                <Checkbox v-model="frontendForm.is_sync" @on-change="() => {
                  frontendForm.sync_env = ''
                  frontendForm.sync_ip = ''
                }"> 是</Checkbox>
              </FormItem>
              <FormItem label="同步环境:" prop="sync_env" v-show="frontendForm.is_sync" >
                <Select v-model="frontendForm.sync_env" style="width: 300px" @on-change="handleSyncEnvChange" placement="top">
                  <Option v-for="env in publishEnvList" :value="env" :key="env">{{ env }}</Option>
                </Select>
              </FormItem>
              <FormItem label="同步环境IP:" prop="sync_ip" v-show="frontendForm.is_sync">
               <Select v-model="frontendForm.sync_ip" style="width: 300px"  placement="top">
                <Option v-for="ip in syncPublishIpList" :value="ip[0]" :key="ip[0]">{{ ip[0] }}
                </Option>
              </Select>
              </FormItem>
            </Form>
          </TabPane>
        </Tabs>
      <!-- </Card> -->
      <div slot="footer">
        <Button type="default"   @click="handleReset(currentForm)">重置</Button>
        <Button type="primary" ghost :loading="CommitBtnLoading" @click="handleTask">发布</Button>
      </div>
    </Modal>
  </div>
</template>
<script>
import { getAppDetail, getEnvs, getHasBeenPublished, getAppNameBranch, createPublishTask, getAlreadyPublishVer, getAppNameEndpoint, unlockPublishIp } from '@/api/code_publish/publish'
import { sendNotice } from '@/libs/util.js'
export default {
  name: 'publish_task',
  computed: {
    createModal: {
      get () {
        return this.taskModal
      },
      set (val) {
        this.$emit('switchTaskModal', val)
      }
    }
  },
  watch: {
    backendAction (newVal, oldVal) {
      console.log(newVal)
      if (newVal === 'Rollback') {
        delete this.ruleBackendForm['branch']
        this.ruleBackendForm['publish_version'] = [{ required: true, message: '必须填写', trigger: 'change' }]
      } else if (newVal === 'Deploy') {
        delete this.ruleBackendForm['publish_version']
        this.ruleBackendForm['branch'] = [{ required: true, message: '必须填写', trigger: 'change' }]
      }
    },
    frontendAction (newVal, oldVal) {
      console.log(newVal)
      if (newVal === 'Rollback') {
        delete this.ruleFrontendForm['branch']
        this.ruleFrontendForm['publish_version'] = [{ required: true, message: '必须填写', trigger: 'change' }]
      } else if (newVal === 'Deploy') {
        delete this.ruleFrontendForm['publish_version']
        this.ruleFrontendForm['branch'] = [{ required: true, message: '必须填写', trigger: 'change' }]
      }
    }
  },
  props: [
    'taskModal'
  ],
  data () {
    return {
      frontendReleaseWarn: false,
      backendReleaseWarn: false,
      unlockBtnLoading: false,
      CommitBtnLoading: false,
      commitForm: {},
      backendForm: {
        action: '',
        app_name: '',
        env: '',
        ip: '',
        branch: '',
        is_sync: false,
        sync_env: '',
        sync_ip: '',
        is_jacoco: false,
        publish_version: ''
      },
      ruleBackendForm: {
        action: [
          { required: true, message: '必须填写', trigger: 'change' }
        ],
        app_name: [
          { required: true, message: '必须填写', trigger: 'change' }
        ],
        env: [
          { required: true, message: '必须填写', trigger: 'change' }
        ],
        ip: [
          { required: true, message: '必须填写', trigger: 'change' }
        ],
        branch: [
          { required: true, message: '必须填写', trigger: 'change' }
        ],
        publish_version: [
          { required: false, message: '必须填写', trigger: 'change' }
        ]
      },
      frontendForm: {
        action: '',
        app_name: '',
        env: '',
        ip: '',
        branch: '',
        is_sync: false,
        sync_env: '',
        sync_ip: '',
        publish_version: '',
        git_diff_before: false,
        git_diff_after: false
      },
      ruleFrontendForm: {
        action: [
          { required: true, message: '必须填写', trigger: 'change' }
        ],
        app_name: [
          { required: true, message: '必须填写', trigger: 'change' }
        ],
        env: [
          { required: true, message: '必须填写', trigger: 'change' }
        ],
        ip: [
          { required: true, message: '必须填写', trigger: 'change' }
        ],
        branch: [
          { required: true, message: '必须填写', trigger: 'change' }
        ]
      },
      actionList: [
        ['Deploy', '发布'],
        ['Rollback', '回滚']
      ],
      backendServerMode: ['docker', 'jar', 'tomcat', 'tc2docker'],
      frontendServerMode: ['php', 'pc', 'mobile'],
      appDetailList: [],
      publishEnvList: [],
      publishIpList: [],
      branchList: [],
      alreadyPublishVerList: [],
      currentForm: 'backendForm',
      syncPublishIpList: [],
      frontendAction: 'Deploy',
      backendAction: 'Deploy',
      backendAppNameList: [],
      appNameBackendList: [],
      appNameFrontendList: []
    }
  },
  methods: {
    handleOpenAppName () {
      let webTag
      let env
      if (this.currentForm === 'backendForm') {
        webTag = 'backend'
        env = this.backendForm.env
        getAppNameEndpoint(webTag, env).then(res => {
          this.appNameBackendList = res.data
        }).catch(err => {
          sendNotice('error', err)
        })
      } else {
        webTag = 'frontend'
        env = this.frontendForm.env
        getAppNameEndpoint(webTag, env).then(res => {
          this.appNameBackendList = res.data
        }).catch(err => {
          sendNotice('error', err)
        })
      }
    },
    handleUnlockPublishIp () {
      let appName
      let env
      let action
      if (this.currentForm === 'backendForm') {
        appName = this.backendForm.app_name
        env = this.backendForm.env
        action = this.backendAction
      } else {
        appName = this.frontendForm.app_name
        env = this.frontendForm.env
        action = this.frontendAction
      }
      let data = {
        app_name: appName,
        env: env,
        action: action
      }
      this.unlockBtnLoading = true
      unlockPublishIp(data).then(res => {
        this.handleHasBeenPublished()
        this.$Message.success('成功解锁')
        this.unlockBtnLoading = false
      }).catch(err => {
        sendNotice('error', '解锁失败')
        sendNotice('error', err)
        this.unlockBtnLoading = false
      })
    },
    handleBackendAppNameChange () {
      this.backendForm.env = ''
      this.backendForm.publish_version = ''
      this.backendForm.ip = ''
      this.backendForm.branch = ''
      getAppMainConfig('backend').then(res => {
        this.backendAppNameList = res.data
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    handleAlreadyPublishVer () {
      let appName
      let env
      if (this.currentForm === 'backendForm') {
        appName = this.backendForm.app_name
        env = this.backendForm.env
      } else {
        appName = this.frontendForm.app_name
        env = this.frontendForm.env
      }
      getAlreadyPublishVer(appName, env).then(res => {
        this.alreadyPublishVerList = res.data
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    handleHasBeenPublished () {
      let appName
      let env
      let action
      if (this.currentForm === 'backendForm') {
        appName = this.backendForm.app_name
        env = this.backendForm.env
        action = this.backendForm.action
      } else {
        appName = this.frontendForm.app_name
        env = this.frontendForm.env
        action = this.frontendForm.action
      }
      // 调整 publish ip list
      getHasBeenPublished(appName, env, action).then(res => {
        this.publishIpList = this.publishIpList.filter(item => {
          if (res.data.indexOf(item[0]) === -1) {
            if (item.length > 1) { item.pop() }
            return item.push(false)
          } else {
            if (item.length > 1) { item.pop() }
            return item.push(true)
          }
        })
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    handleEnvChange () {
      if (this.currentForm === 'backendForm') {
        this.backendForm.ip = ''
        this.backendForm.app_name = ''
        this.backendForm.publish_ip = ''
        this.backendForm.branch = ''
        this.publishIpList = []
        this.branchList = []
        this.backendReleaseWarn = this.backendForm.env === 'Release'
      } else {
        this.frontendForm.ip = ''
        this.frontendForm.app_name = ''
        this.frontendForm.publish_ip = ''
        this.frontendForm.branch = ''
        this.publishIpList = []
        this.branchList = []
        this.frontendReleaseWarn = this.frontendForm.env === 'Release'
      }
    },
    handleAppNameChange (env) {
      let appName
      let env_
      if (this.currentForm === 'backendForm') {
        appName = this.backendForm.app_name
        env_ = this.backendForm.env
        this.backendForm.ip = ''
      } else {
        appName = this.frontendForm.app_name
        env_ = this.frontendForm.env
        this.frontendForm.ip = ''
      }
      if (appName && env) {
        getAppDetail(appName, env_).then(res => {
          console.log(res.data)
          this.publishIpList = res.data
        }).catch(err => {
          sendNotice('error', err)
        })
        getAppNameBranch(appName, env_).then(res => {
          this.branchList = res.data
        }).catch(err => {
          this.branchList = []
          sendNotice('error', err)
        })
      }
    },
    handleSyncEnvChange (env) {
      this.backendForm.sync_ip = ''
      this.frontendForm.sync_ip = ''
      if (this.currentForm === 'backendForm') {
        if (this.backendForm.app_name) {
          getAppDetail(this.backendForm.app_name, env).then(res => {
            this.syncPublishIpList = res.data
          }).catch(err => {
            sendNotice('error', err)
          })
        }
      } else {
        if (this.frontendForm.app_name) {
          getAppDetail(this.frontendForm.app_name, env).then(res => {
            this.syncPublishIpList = res.data
          }).catch(err => {
            sendNotice('error', err)
          })
        }
      }
    },
    commitTask () {
      this.CommitBtnLoading = false
      this.switchTaskModal(false)
    },
    handleTask () {
      console.log(this.currentForm)
      if (this.currentForm === 'backendForm') {
        this.CommitBtnLoading = true
        this.handleBackendTask(this.currentForm)
      } else if (this.currentForm === 'frontendForm') {
        this.CommitBtnLoading = true
        this.handleFrontendTask(this.currentForm)
      }
    },
    handleBackendTask (name) {
      let jenkinsParams = {
        IsJacoco: this.backendForm.is_jacoco
      }
      let data = {
        action: this.backendForm['action'],
        app_name: this.backendForm['app_name'],
        env: this.backendForm['env'],
        publish_ip: this.backendForm['ip'],
        branch: this.backendForm['branch'],
        is_sync: this.backendForm['is_sync'] ? 1 : 0,
        sync_env: this.backendForm['sync_env'],
        sync_ip: this.backendForm['sync_ip'],
        jenkins_params: JSON.stringify(jenkinsParams),
        publish_version: this.backendForm['publish_version']
      }
      this.$refs[name].validate((valid) => {
        if (valid) {
          createPublishTask(data).then(res => {
            this.$Message.success('创建发布任务成功')
            this.commitTask()
            this.backendForm.ip = ''
            this.$emit('refreshTaskList')
          }).catch(err => {
            sendNotice('error', err)
            this.commitTask()
          })
        } else {
          this.$Message.error('缺少必填参数')
          this.CommitBtnLoading = false
        }
      })
    },
    handleFrontendTask (name) {
      let jenkinsParams = {}
      let data = {
        action: this.frontendForm['action'],
        app_name: this.frontendForm['app_name'],
        env: this.frontendForm['env'],
        publish_ip: this.frontendForm['ip'],
        branch: this.frontendForm['branch'],
        is_sync: this.frontendForm['is_sync'] ? 1 : 0,
        sync_env: this.frontendForm['sync_env'],
        sync_ip: this.frontendForm['sync_ip'],
        jenkins_params: JSON.stringify(jenkinsParams),
        publish_version: this.frontendForm['publish_version']
      }
      console.log(data)
      this.$refs[name].validate((valid) => {
        if (valid) {
          createPublishTask(data).then(res => {
            this.$Message.success('创建发布任务成功')
            this.frontendForm.ip = ''
            this.commitTask()
            this.$emit('refreshTaskList')
          }).catch(err => {
            sendNotice('error', err)
            this.commitTask()
          })
          setTimeout(() => { this.commitTask() }, 3000)
        } else {
          this.$Message.error('缺少必填参数')
          this.CommitBtnLoading = false
        }
      })
    },
    switchTaskModal (val) {
      this.$emit('switchTaskModal', val)
    },
    handleReset (name) {
      this.$refs[name].resetFields()
    },
    handleEndpointChange (tabName) {
      if (tabName === 'backend') {
        this.commitForm = this.backendForm
        this.currentForm = 'backendForm'
      } else {
        this.commitForm = this.frontendForm
        this.currentForm = 'frontendForm'
      }
    }
  },
  mounted () {
    getEnvs().then(res => {
      this.publishEnvList = []
      res.data.forEach(item => {
        if (item.env !== 'ALL') {
          this.publishEnvList.push(item.env)
        }
      })
    }).catch(err => {
      sendNotice('error', err)
    })
  }
}
</script>
