<template>
  <div>
    <Alert show-icon type="warning">这里的设置用于代码发布配置，各类固定选项的设置</Alert>
    <Divider orientation="left">&nbsp;<span class="divider-text">Git Auth 设置</span>&nbsp;</Divider>
    <Form inline >
      <FormItem label="Git Username:" :label-width="100">
        <Input v-model.trim="dataForm.git_info.username" placeholder="Git Username" style="width: 200px"></Input>
      </FormItem>
      <FormItem label="Git Password:" :label-width="100">
        <Input v-model.trim="dataForm.git_info.password" placeholder="Git Password" style="width: 200px;" ></Input>
      </FormItem>
      <FormItem>
        <Button type="primary" ghost size="small" @click="handleUpdateCodePublish">Save</Button>
      </FormItem>
    </Form>
    <Divider orientation="left">&nbsp;<span class="divider-text">Server Mode 设置</span>&nbsp;</Divider>
    <Tag v-for="item in serverModeList" :key="item" :name="item" closable @on-close="handleRemoveServerMode" color="cyan" type="border">{{ item }}</Tag>
    <br>
    <div style="margin-top: 10px">
      <Input v-model.trim="dataForm.server_mode" placeholder="" style="width: 200px; margin-right: 10px;"></Input>
      <Button icon="ios-add" type="dashed" size="small" @click="() => {
        serverModeList.push(dataForm.server_mode)
        handleUpdateCodePublish()
        }">添加 server mode</Button>
    </div>
    <Divider orientation="left">&nbsp;<span class="divider-text">Jenkins Project 设置</span>&nbsp;</Divider>
    <Tag v-for="item in JenkinsProject" :key="item" :name="item" closable @on-close="handleRemoveJenkinsProject" color="cyan" type="border">{{ item }}</Tag>
    <div style="margin-top: 10px">
      <Input v-model.trim="dataForm.jenkins_project" placeholder="" style="width: 200px; margin-right: 10px;"></Input>
      <Button icon="ios-add" type="dashed" size="small" @click="() => {
        JenkinsProject.push(dataForm.jenkins_project)
        handleUpdateCodePublish()
        }">添加 jenkins project</Button>
    </div>
    <Divider orientation="left">&nbsp;<span class="divider-text">发布记录删除x天前数据</span>&nbsp;</Divider>
    <Form inline >
    <FormItem label="删除x天前:" :label-width="100">
      <InputNumber v-model="dataForm.delete_expire_days" :min=1 :max=30 placeholder="min=1d，max30d" style="width: 200px"></InputNumber>
    </FormItem>
    <FormItem>
      <Button type="primary" ghost size="small" @click="handleUpdateCodePublish">Save</Button>
    </FormItem>
    </Form>
  </div>
</template>
<script>
import { getCodePublish, updateCodePublish } from '@/api/setting/common_setting'
import { sendNotice } from '@/libs/util.js'
export default {
  name: 'publish_setting',
  data () {
    return {
      dataForm: {
        server_mode: '',
        jenkins_project: '',
        git_info: {
          username: '',
          password: ''
        },
        delete_expire_days: 3
      },
      serverModeList: [],
      JenkinsProject: []
    }
  },
  methods: {
    refreshData () {
      getCodePublish().then(res => {
        this.serverModeList = res.data[0]['code_publish_setting']['server_mode']
        this.JenkinsProject = res.data[0]['code_publish_setting']['jenkins_project']
        this.dataForm.git_info.username = res.data[0]['code_publish_setting']['git_info']['username']
        this.dataForm.git_info.password = res.data[0]['code_publish_setting']['git_info']['password']
        this.dataForm.delete_expire_days = res.data[0]['code_publish_setting']['delete_expire_days']
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    handleRemoveServerMode (e, name) {
      this.serverModeList = this.serverModeList.filter(item => {
        if (item !== name) {
          return item
        }
      })
      this.handleUpdateCodePublish()
    },
    handleRemoveJenkinsProject (e, name) {
      this.JenkinsProject = this.JenkinsProject.filter(item => {
        if (item !== name) {
          return item
        }
      })
      this.handleUpdateCodePublish()
    },
    handleUpdateCodePublish () {
      let data = {
        server_mode: this.serverModeList,
        jenkins_project: this.JenkinsProject,
        git_info: {
          username: this.dataForm.git_info.username,
          password: this.dataForm.git_info.password
        },
        delete_expire_days: this.dataForm.delete_expire_days
      }
      updateCodePublish({ code_publish_setting: JSON.stringify(data) }).then(res => {
        this.$Message.success('操作成功')
        this.dataForm.server_mode = ''
        this.dataForm.jenkins_project = ''
      }).catch(err => {
        sendNotice('error', err)
      })
    }
  },
  mounted () {
    this.refreshData()
  }
}
</script>
