<template>
  <div>
    <Alert show-icon type="warning">已被设置的属性被删除后，关联的Host不会改变其已设置的属性，需重新修改</Alert>
    <span v-if="!showAlert">
      <a style=" font-size: 12px" @click="showAlert = true" >HELP</a>
      <Icon type="ios-help-circle-outline" style="color: #2D8cF0; margin-left: 3px"/>
    </span>
    <Alert v-if="showAlert" type="warning" closable @on-close="showAlert = false">
      <span slot="desc">
          <b>IDC设置: </b>设置后可在cmdb中的idc选择资源归属的机房；<br>
          <b>环境设置: </b>设置后可在cmdb中的环境选择资源归属的环境；
      </span>
    </Alert>
    <Divider orientation="left">
      <span class="divider-text">IDC 设置</span>
    </Divider>
    <div class="content-text">
      <Tag
        type="border"
        color="cyan"
        v-for="item in idcList"
        :key="item"
        :name="item"
        closable
        @on-close="idcClose"
      >{{ item }}</Tag>
      <div style="margin-top: 10px">
        <Input v-model.trim="idcName" placeholder="机房名" style="width: 200px; margin-right: 10px;"></Input>
        <Button icon="ios-add" type="dashed" size="small" @click="idcAdd">添加机房</Button>
      </div>
    </div>
    <Divider orientation="left">
      <span class="divider-text">环境设置</span>
    </Divider>
    <div class="content-text">
      <Tag
        type="border"
        color="cyan"
        v-for="item in envList"
        :key="item"
        :name="item"
        closable
        @on-close="envClose"
      >{{ item }}</Tag>
      <div style="margin-top: 10px">
        <Input v-model.trim="envName" placeholder="环境名" style="width: 200px; margin-right: 10px;"></Input>
        <Button icon="ios-add" type="dashed" size="small" @click="envAdd">添加环境</Button>
      </div>
    </div>
    <Divider orientation="left">
      <span class="divider-text">SSH PROXY</span>
    </Divider>
    <div class="content-text">
      <Select v-model="proxyIdc" multiple style="width:200px">
        <Option v-for="(item, idx) in idcObj" :value="idx" :key="idx">{{ idx }}</Option>
      </Select>
      <Button style="margin-left: 10px" type="default" :loading="sshProxyloading" size="small"  @click="renderSshProxy">
        <span v-if="!sshProxyloading">渲染ssh proxy</span>
        <span v-else>Loading...</span>
    </Button>
    </div>
    <Divider orientation="left">&nbsp;<span style="color: #c5c8ce">Other</span>&nbsp;</Divider>
  </div>
</template>
<script>

import {
  getCmdbSetting,
  updateCmdbSetting,
  getSshProxy,
  updateSshProxy
} from '@/api/setting/common_setting'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'cmdb_setting_common',
  data () {
    return {
      orginData: '',
      showAlert: false,
      idcName: '',
      envName: '',
      idcList: [],
      envList: [],
      idcObj: {
        'aliyun': 'AliyunEcs',
        'native': 'NativeHost'
      },
      proxyIdc: [],
      sshProxyloading: false
    }
  },
  methods: {
    renderSshProxy () {
      if (this.proxyIdc.length === 0) {
        this.$Message.error('ssh proxy 不允许为空.')
        return
      }
      this.sshProxyloading = true
      updateSshProxy(JSON.stringify(this.proxyIdc)).then(res => {
        this.$Message.success('操作成功')
        this.sshProxyloading = false
      }).catch(err => {
        sendNotice('error', err)
        this.sshProxyloading = false
      })
    },
    handleIdc () {
      this.orginData['base']['idc'] = this.idcList
      var data = {
        'cmdb_setting': JSON.stringify(this.orginData)
      }
      console.log(data)
      updateCmdbSetting(data).then(res => {
        this.$Message.success('操作成功')
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    handleEnv () {
      this.orginData['base']['env'] = this.envList
      var data = {
        'cmdb_setting': JSON.stringify(this.orginData)
      }
      updateCmdbSetting(data).then(res => {
        this.$Message.success('操作成功')
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    idcAdd () {
      this.idcList.push(this.idcName)
      this.handleIdc()
      this.idcName = ''
    },
    envAdd () {
      this.envList.push(this.envName)
      this.handleEnv()
      this.envName = ''
    },
    idcClose (event, name) {
      const index = this.idcList.indexOf(name)
      this.idcList.splice(index, 1)
      this.handleIdc()
    },
    envClose (event, name) {
      const index = this.envList.indexOf(name)
      this.envList.splice(index, 1)
      this.handleEnv()
    }
  },
  mounted () {
    getCmdbSetting().then(res => {
      this.orginData = res.data[0]['cmdb_setting']
      this.idcList = res.data[0]['cmdb_setting']['base']['idc']
      this.envList = res.data[0]['cmdb_setting']['base']['env']
    }).catch(err => {
      sendNotice('error', err)
    })
    getSshProxy().then(res => {
      this.idcObj = res.data
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
.content-text {
  padding-left: 30px;
}
</style>
