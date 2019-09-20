<template>
  <div>
    <Row :gutter="10">
      <Col span="14">
        <Card style="margin-bottom: 10px">
          <p slot="title">基本信息</p>
          <Form :label-width=90>
            <FormItem label="主机名:" style="margin-bottom: 5px">
              <span class="instance-content">{{ instanceData.hostname }}</span>
            </FormItem>
            <FormItem v-show="cmdb === 'native'" label="IDC:" style="margin-bottom: 5px">
              <span class="instance-content">{{ instanceData.idc }}</span>
            </FormItem>
            <FormItem v-show="cmdb === 'native'" label="描述:" style="margin-bottom: 5px">
              <span class="instance-content">{{ instanceData.description }}</span>
            </FormItem>
            <FormItem v-show="cmdb === 'aliyun'" label="可用区:" style="margin-bottom: 5px">
              <span class="instance-content">{{ instanceData.zone_id }}</span>
            </FormItem>
            <FormItem v-show="cmdb === 'aliyun'" label="名称:" style="margin-bottom: 5px">
              <span class="instance-content">{{ instanceData.instance_name }}</span>
            </FormItem>
            <FormItem v-show="cmdb === 'aliyun'" label="ID:" style="margin-bottom: 5px">
              <span class="instance-content">{{ instanceData.instance_id }}</span>
            </FormItem>
            <FormItem v-show="cmdb === 'aliyun'" label="实例规格:" style="margin-bottom: 5px">
              <span class="instance-content">{{ instanceData.instance_type }}</span>
            </FormItem>
            <FormItem v-show="cmdb === 'aliyun'" label="付费方式:" style="margin-bottom: 5px">
              <span class="instance-content">{{ instanceData.instance_charge_type }}</span>
            </FormItem>
            <FormItem v-show="cmdb === 'aliyun'" label="创建时间:" style="margin-bottom: 5px">
              <span class="instance-content">{{ instanceData.created }}</span>
            </FormItem>
            <FormItem v-show="cmdb === 'aliyun'" label="最后更新时间:" style="margin-bottom: 5px">
              <span class="instance-content">{{ instanceData.updated }}</span>
            </FormItem>
            <FormItem v-show="cmdb === 'aliyun'" label="过期时间:" style="margin-bottom: 5px">
              <span class="instance-content">{{ instanceData.expired_time }}</span>
            </FormItem>
            <FormItem label="SN:" style="margin-bottom: 5px">
              <span class="instance-content">{{ instanceData.serial_number }}</span>
            </FormItem>
          </Form>
        </Card>
        <Card >
          <p slot="title">配置信息</p>
          <Form :label-width=80>
            <FormItem label="环境:" style="margin-bottom: 5px">
              <span class="instance-content">{{ instanceData.environment }}</span>
            </FormItem>
            <FormItem label="CPU:" style="margin-bottom: 5px">
              <span class="instance-content">{{ instanceData.cpu }}</span>
            </FormItem>
            <FormItem label="内存:" style="margin-bottom: 5px">
              <span class="instance-content">{{ instanceData.memory }} MB</span>
            </FormItem>
            <FormItem label="磁盘:" style="margin-bottom: 5px">
              <span class="instance-content">{{ instanceData.disk }}</span>
            </FormItem>
            <FormItem label="操作系统:" style="margin-bottom: 5px">
              <span class="instance-content">{{ instanceData.os_name }}</span>
            </FormItem>
            <FormItem label="公网IP:" style="margin-bottom: 5px">
              <span class="instance-content">{{ instanceData.public_ip }}</span>
            </FormItem>
            <FormItem label="私网IP:" style="margin-bottom: 5px">
              <span class="instance-content">{{ instanceData.private_ip }}</span>
            </FormItem>
            <FormItem label="SSH IP:" style="margin-bottom: 5px">
              <span class="instance-content">{{ instanceData.ssh_ip }}</span>
            </FormItem>
            <FormItem label="SSH Port:" style="margin-bottom: 5px">
              <span class="instance-content">{{ instanceData.ssh_port }}</span>
            </FormItem>
          </Form>
        </Card>
      </Col>
      <Col span="10">
        <Card style="margin-bottom: 10px">
          <p slot="title">状态</p>
          <Row :gutter="10">
            <Col span="4">
              <p style="text-align: center">
                <Icon v-show="instanceData.status === 'Running'"
                style="font-size: 40px;color: #67C23A;"
                type="md-arrow-dropright-circle" />
                <Icon v-show="instanceData.status !== 'Running'"
                style="font-size: 40px;color: #F56C6C;"
                type="md-pause" />
                <br>
                <span v-show="instanceData.status === 'Running'" style="color: #67C23A;">运行中</span>
                <span v-show="instanceData.status !== 'Running'" style="color: #F56C6C;">停止</span>
              </p>
            </Col>
            <Col span="4">
              <p style="text-align: center">
                <Icon v-show="instanceData.is_active"
                style="font-size: 40px;color: #67C23A;"
                type="md-checkmark-circle-outline" />
                <Icon v-show="!instanceData.is_active"
                style="font-size: 40px;color: #F56C6C;"
                type="ios-remove-circle-outline" />
                <br>
                <span v-show="instanceData.is_active" style="color: #67C23A;">使用中</span>
                <span v-show="!instanceData.is_active" style="color: #F56C6C;">回收</span>
              </p>
            </Col>
            <Col span="4">
              <p style="text-align: center">
                <Icon v-show="instanceData.is_ansible"
                type="md-checkmark-circle-outline"
                style="font-size: 40px;color: #67C23A;" />
                <Icon v-show="!instanceData.is_ansible"
                style="font-size: 40px;color: #F56C6C;"
                type="ios-close-circle-outline" />
                <br>
                <span v-show="instanceData.is_ansible" style="color: #67C23A;">激活 Ansible</span>
                <span v-show="!instanceData.is_ansible" style="color: #F56C6C;">禁用 Ansible</span>
              </p>
            </Col>
          </Row>
        </Card>
        <Card style="margin-bottom: 10px">
          <p slot="title">操作</p>
          <Form :label-width=100>
            <FormItem label="Ansible 更新:">
              <Button type="primary" ghost  :loading="ansibleLoading"
              :disabled="!instanceData.is_ansible"
              @click="ansibleUpdate" style="float: right">执行</Button>
            </FormItem>
          </Form>
        </Card>
        <Card>
          <p slot="title">App</p>
          <Table :columns="tableColumns" :data="tableDatas"></Table>
        </Card>
      </Col>
    </Row>
  </div>
</template>
<script>

import { readEcsInfo, ansibleUpdateAliyunEcs, getAliyunEcsAppRel } from '@/api/cmdb/aliyun/resource'
import { readNativeHostInfo, ansibleUpdateNativeHost, getNativeHostAppRel } from '@/api/cmdb/native/resource'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'cmdb_host_info',
  watch: {
    id (newVal, oldVal) {
      // 因为watch 会带入下个组件，所以判断如果是undefined 就不去更新
      if (newVal === undefined || !this.$route.query.cmdb) { return }
      this.reloadInfo(this.cmdb)
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
    cmdb: {
      get: function () {
        return this.$route.query.cmdb
      },
      set: function (newVal) {
        return newVal
      }
    }
  },
  data () {
    const checkIcon = function (h, check) {
      if (check) {
        return h('Icon', {
          props: {
            type: 'md-checkmark-circle-outline'
          },
          style: {
            'color': '#67C23A',
            'font-size': '20px'
          }
        })
      }
      return h('Icon', {
        props: {
          type: 'ios-close-circle-outline'
        },
        style: {
          'color': '#ed4014',
          'font-size': '20px'
        }
      })
    }
    return {
      ansibleLoading: false,
      tableColumns: [
        {
          'title': 'Name',
          'key': 'app_name',
          render: (h, params) => {
            return h('a', {
              on: {
                click: () => {
                  let id = params.row.id
                  let appName = params.row.app_name
                  const route = {
                    name: 'apps_app_detail',
                    params: {
                      id
                    },
                    query: {
                      app_name: appName
                    }
                  }
                  this.$router.push(route)
                }
              }
            }, params.row.app_name)
          }
        },
        {
          'title': 'Used',
          'key': 'is_active',
          'align': 'center',
          render: (h, params) => {
            let check = params.row.is_active
            return checkIcon(h, check)
          }
        }
      ],
      tableDatas: [],
      instanceData: {}
    }
  },
  methods: {
    ansibleUpdate () {
      this.ansibleLoading = true
      var data = {
        'cmdb': this.cmdb,
        'single_host_id': this.id
      }
      try {
        // 其实2个api 是一样的, 只是为了区分权限
        switch (this.cmdb) {
          case 'aliyun':
            ansibleUpdateAliyunEcs(data).then(res => {
              this.$Message.success('操作成功')
              this.reloadInfo(this.cmdb)
              this.ansibleLoading = false
            }).catch(err => {
              sendNotice('error', err)
              this.ansibleLoading = false
            })
            break
          case 'native':
            ansibleUpdateNativeHost(data).then(res => {
              this.$Message.success('操作成功')
              this.reloadInfo(this.cmdb)
              this.ansibleLoading = false
            }).catch(err => {
              sendNotice('error', err)
              this.ansibleLoading = false
            })
            break
        }
      } catch (err) {
        sendNotice('error', err)
        this.ansibleLoading = false
      }
    },
    reloadInfo (cmdb) {
      const funcMap = {
        'aliyun': readEcsInfo,
        'native': readNativeHostInfo
      }
      const AppRelMap = {
        'aliyun': getAliyunEcsAppRel,
        'native': getNativeHostAppRel
      }
      funcMap[cmdb](this.id).then(res => {
        this.instanceData = res.data
        this.instanceData.private_ip = JSON.parse(this.instanceData.private_ip).join('; ')
        this.instanceData.public_ip = JSON.parse(this.instanceData.public_ip).join('; ')
        let disk = []
        let diskObj = JSON.parse(this.instanceData.disk)
        for (let idx in diskObj) {
          disk.push(`${idx}: ${diskObj[idx]} GiB`)
        }
        this.instanceData.disk = disk.join('; ')
      }).catch(err => {
        sendNotice('error', err)
      })
      AppRelMap[cmdb](this.id).then(res => {
        this.tableDatas = res.data
      }).catch(err => {
        sendNotice('error', err)
      })
    }
  },
  mounted () {
    this.cmdb = this.$route.query.cmdb
    this.id = this.$route.params.id
    this.reloadInfo(this.cmdb)
  }
}
/** @description aliyun ecs表数据
  // 'id': 1,
  // 'updated': '2019-04-22 18:21:30',
  // 'created': '2019-04-15 06:51:00',
  // 'expired_time': '2020-04-15 16:00:00',
  // 'hostname': 'pingan-mbfe-02.release.ayg',
  // 'serial_number': 'a6f6325c-e23f-4446-ac57-ce4af84581a5',
  // 'cpu': 2,
  // 'memory': 4096,
  // 'os_type': 'linux',
  // 'os_name': 'CentOS  7.2 64位',
  // 'disk': '{"/dev/xvda": 50}',
  // 'private_ip': '["172.30.5.19"]',
  // 'public_ip': '["120.78.220.71"]',
  // 'status': 'Running',
  // 'environment': 'undefined',
  // 'is_active': true,
  // 'ssh_port': 38333,
  // 'ac_key_id': 2,
  // 'zone_id': 'cn-shenzhen-c',
  // 'region_id': 'cn-shenzhen',
  // 'instance_type': 'ecs.sn1ne.large',
  // 'instance_name': '平安前置机02',
  // 'instance_id': 'i-wz93uu93v1vyu6qryv38',
  // 'instance_charge_type': 'PrePaid'
 */
</script>
<style>
.instance-content {
  font-size: 13px;
  font-weight: 500;
}
.demo-spin-icon-load{
  animation: ani-demo-spin 1s linear infinite;
}
</style>
