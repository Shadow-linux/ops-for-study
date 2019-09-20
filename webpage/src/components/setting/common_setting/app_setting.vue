<template>
  <div>
    <Divider orientation="left">&nbsp;<span class="divider-text">服务选项设置</span>&nbsp;</Divider>
    <Alert show-icon type="warning">已被选择的属性被删除，关联的App不会改变其已设置的属性，需重新修改；(docker 选项用于docker监控)</Alert>
    <p style="color: #2d8cf0; line-height: 15px; margin-top: 5px; font-size: 12px">
      * 如 docker, k8s, tomcat, java, nginx, php, mysql, redis, kafka, python
    </p>
    <Tag
      type="border"
      color="cyan"
      v-for="item in serviceList"
      :key="item"
      :name="item"
      closable
      @on-close="serviceClose"
    >{{ item }}</Tag>
    <div style="margin-top: 10px">
      <Input v-model.trim="serviceName" placeholder="服务名" style="width: 200px; margin-right: 10px;"></Input>
      <Button icon="ios-add" type="dashed" size="small" @click="serviceAdd">服务选项添加</Button>
    </div>
    <Divider orientation="left">&nbsp;<span class="divider-text">环境监控Urlooker Agent设置</span>&nbsp;</Divider>
    <Alert show-icon type="warning">为每个环境设置，其对应的agent; <br>
      * <b>default</b> 为线上的agent, 部署在 service-test01-172-30-2-1.pre-release.ayg; <br>
      * <b>internal.ayg.gz</b> 为线下机房的agent，部署在 basic-ops-192-168-1-158.internal.ayg<br>
      * 进程名：<b>urlooker-agent</b>
      </Alert>
    <div style="margin-bottom: 10px">
      <Tag color="cyan" type="border" v-for="(agent, env) in envMonitorAgentDict" :key="env">
        {{ env }}: {{ agent }}
      </Tag>
    </div>
    <Form :model="appMonitorAgentForm" inline>
      <FormItem>
        <Select filter v-model="appMonitorAgentForm.env" style="width: 200px" placeholder="Associate Env">
          <Option v-for="item in envList" :value="item" :key="item">
            {{ item }}
          </Option>
        </Select>
      </FormItem>
      <FormItem>
        <Select filter v-model="appMonitorAgentForm.agent" style="width: 200px" placeholder="Monitor Agent">
          <Option v-for="item in agentList" :value="item" :key="item">
            {{ item }}
          </Option>
        </Select>
      </FormItem>
      <FormItem>
        <Button type="primary" ghost @click="handleAddEnvMonitorAgent">添加</Button>
      </FormItem>
    </Form>
    <Divider orientation="left">&nbsp;<span style="color: #c5c8ce">Other</span>&nbsp;</Divider>
  </div>
</template>
<script>

import { getAppSetting, updateAppSetting, getCmdbSetting } from '@/api/setting/common_setting'

export default {
  name: 'app_setting',
  data () {
    return {
      envMonitorAgentDict: {},
      envList: [],
      agentList: ['default', 'internal.ayg.gz'],
      orginData: {},
      serviceList: [],
      serviceName: '',
      appMonitorAgentForm: {
        env: '',
        agent: ''
      }
    }
  },
  methods: {
    handleAddEnvMonitorAgent () {
      this.envMonitorAgentDict[this.appMonitorAgentForm.env] = this.appMonitorAgentForm.agent
      this.handleService()
      this.appMonitorAgentForm = {
        env: '',
        agent: ''
      }
    },
    handleService () {
      this.orginData['service'] = this.serviceList
      this.orginData['env_monitor_agent'] = this.envMonitorAgentDict
      var data = {
        'app_setting': JSON.stringify(this.orginData)
      }
      updateAppSetting(data).then(res => {
        this.$Message.success('操作成功')
      })
    },
    serviceAdd () {
      this.serviceList.push(this.serviceName)
      this.handleService()
      this.serviceName = ''
    },
    serviceClose (event, name) {
      const index = this.serviceList.indexOf(name)
      this.serviceList.splice(index, 1)
      this.handleService()
    }
  },
  mounted () {
    getAppSetting().then(res => {
      this.orginData = res.data[0]['app_setting']
      this.serviceList = res.data[0]['app_setting']['service']
      this.envMonitorAgentDict = res.data[0]['app_setting']['env_monitor_agent']
    })
    getCmdbSetting().then(res => {
      this.envList = res.data[0]['cmdb_setting']['base']['env']
      this.envList = this.envList.filter(item => {
        if (item !== 'external' && item !== 'undefined') {
          return item
        }
      })
    }).catch(err => {
      sendNotice('error', err)
    })
  }
}
</script>
<style scoped>
.divider-text {
  color: #515a6e;
  font-size: 14px;
}
</style>
