<template>
  <div>
    <Row :gutter="10">
      <Col span="12">
        <Card>
          <p slot="title">基本信息</p>
          <Form :label-width=100>
            <FormItem label="应用名: " class="instace-struct">
              <span class="instance-content">{{ appName }}</span>
            </FormItem>
            <FormItem label="端口: " class="instace-struct">
              <span class="instance-content">{{ appData.port }}</span>
            </FormItem>
            <FormItem label="服务: " class="instace-struct">
              <span class="instance-content">{{ appData.service }}</span>
            </FormItem>
            <FormItem label="描述: " class="instace-struct">
              <span class="instance-content">{{ appData.description }}</span>
            </FormItem>
            <FormItem label="最近修改时间: " class="instace-struct">
              <span class="instance-content">{{ appData.updated }}</span>
            </FormItem>
            <FormItem label="联系人: " class="instace-struct">
              <Tag :key="userObj.id" v-for="userObj in appData.connector_detail">{{ userObj.username }}</Tag>
            </FormItem >
            <FormItem label="使用中: " class="instace-struct">
              <Icon type="md-checkmark-circle-outline" v-show="appData.is_active" class="success"/>
              <Icon type="ios-close-circle-outline" v-show="!appData.is_active" class="failed"/>
            </FormItem >
            <FormItem label="发布: " class="instace-struct">
              <Icon type="md-checkmark-circle-outline" v-show="appData.is_publish" class="success"/>
              <Icon type="ios-close-circle-outline" v-show="!appData.is_publish" class="failed"/>
            </FormItem >
            <FormItem label="监控: " class="instace-struct">
              <Icon type="md-checkmark-circle-outline" v-show="appData.is_monitor" class="success"/>
              <Icon type="ios-close-circle-outline" v-show="!appData.is_monitor" class="failed"/>
            </FormItem >
            <FormItem label="平台启动: " class="instace-struct">
              <Icon type="md-checkmark-circle-outline" v-show="appData.is_launch" class="success"/>
              <Icon type="ios-close-circle-outline" v-show="!appData.is_launch" class="failed"/>
            </FormItem >
            <FormItem label="内部检测: " class="instace-struct">
              <Icon type="md-checkmark-circle-outline" v-show="appData.is_internal_check_api" class="success"/>
              <Icon type="ios-close-circle-outline" v-show="!appData.is_internal_check_api" class="failed"/>
            </FormItem >
            <FormItem label="内部检测地址: " class="instace-struct" v-show="appData.is_internal_check_api">
              <p  :key="idx" v-for="(hostArr, env, idx) in appData.host_list">
                <span style="font-weight: 500;">{{ env }}:</span>
                <ol style="margin-left: 30px">
                  <li v-for="host in hostArr" :key="host.id">
                    {{ host.internal_check_api }}
                  </li>
                </ol>
              </p>
            </FormItem >
            <FormItem label="外部检测: " class="instace-struct">
              <Icon type="md-checkmark-circle-outline" v-show="appData.is_external_check_api" class="success"/>
              <Icon type="ios-close-circle-outline" v-show="!appData.is_external_check_api" class="failed"/>
            </FormItem >
            <FormItem label="外部检测地址: " class="instace-struct" v-show="appData.is_external_check_api">
              <span class="instance-content">{{ appData.external_check_api }}</span>
            </FormItem >
          </Form>
        </Card>
      </Col>
      <Col span="12">
        <Card>
          <p slot="title">关联主机</p>
          <Table :columns="tableColunms" :data="tableDatas"></Table>
        </Card>
      </Col>
    </Row>
  </div>
</template>
<script>

import {
  getSingleAppDetail
} from '@/api/apps/app_managerment'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'apps_app_detail',
  data () {
    return {
      unwatch: '',
      appData: {
      },
      tableColunms: [
        {
          'title': '环境',
          'width': 130,
          'key': 'env'
        },
        {
          'title': '主机',
          render: (h, params) => {
            let renderArr = []
            for (let idx in params.row.hostArr) {
              let obj = params.row.hostArr[idx]
              let hostname = obj.hostname
              let privateIp = `（私）  ${obj.private_ip}`
              let publicIp = `（公）  ${obj.public_ip}`
              let id = obj.id
              let cmdb = obj.cmdb
              renderArr.push(
                h('p', {}, [
                  h('a', {
                    on: {
                      click: () => {
                        const route = {
                          name: 'cmdb_host_info',
                          params: {
                            id
                          },
                          query: {
                            hostname,
                            cmdb
                          }
                        }
                        this.$router.push(route)
                      }
                    }
                  }, hostname),
                  h('p', {}, privateIp),
                  h('p', {}, publicIp)
                ])
              )
            }
            return h('div', {}, renderArr)
          }
        }
      ],
      tableDatas: []
    }
  },
  watch: {
    id (newVal, oldVal) {
      // 因为watch 会带入下个组件，所以判断如果是undefined 就不去更新
      if (newVal === undefined || !this.$route.query.app_name) { return }
      this.reloadInfo()
      setTimeout(() => {
        this.$Spin.hide()
      }, 800)
      this.$Spin.show({
        render: (h) => {
          return h('div', [
            h('Icon', {
              'class': 'demo-spin-icon-load',
              props: {
                type: 'ios-loading',
                size: 18
              }
            }),
            h('div', 'Loading')
          ])
        }
      })
    }
  },
  computed: {
    id: {
      get: function () {
        return this.$route.params.id
      },
      set: function (newVal) {
        return newVal
      }
    },
    appName: {
      get: function () {
        return this.$route.query.app_name
      },
      set: function (newVal) {
        return newVal
      }
    }
  },
  methods: {
    reloadInfo () {
      getSingleAppDetail(this.id).then(res => {
        this.appData = res.data
        let hostList = this.appData.host_list
        this.tableDatas = []
        for (let env in hostList) {
          // 首位插入, 规定数据格式
          this.tableDatas.splice(0, 0, { env: env, 'hostArr': [] })
          let hostArr = hostList[env]
          for (let idx in hostArr) {
            // 插入hostname 数据
            this.tableDatas[0]['hostArr'].push(hostArr[idx])
          }
        }
      }).catch(err => {
        sendNotice('error', err)
      })
    }
  },
  mounted () {
    this.reloadInfo()
  }
}
</script>
<style>
.success {
  color: #67C23A;
  font-size: 20px;
}
.failed {
  color: #ed4014;
  font-size: 20px;
}
.instace-struct {
  margin-bottom: 5px
}
.instance-content {
  font-size: 13px;
  font-weight: 500;
}
.demo-spin-icon-load{
  animation: ani-demo-spin 1s linear infinite;
}
</style>
