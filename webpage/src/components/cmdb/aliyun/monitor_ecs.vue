<template>
  <div>
    <Row>
      <Col span="24">
        <Card>
          <p slot="title">查询</p>
          <Form ref="dataForm" :model="dataForm"  inline>
            <FormItem label="">
              <Select filterable v-model="dataForm.access_key_id" placeholder="AccessKey" style="width:200px" @on-change="selectAccessKey">
                <Option v-for="item in accessKeyList" :value="item.id" :key="item.id">{{ item.key_name }}</Option>
              </Select>
            </FormItem>
            <FormItem label="">
              <Select filterable v-model="dataForm.instance_id" :disabled="hostnameSelectBool" placeholder="主机名" style="width:200px" @on-change="selectHostname">
                <Option v-for="item in hostnameList" :value="item.instance_id" :key="item.instance_id">{{ item.hostname }}</Option>
              </Select>
            </FormItem>
            <FormItem>
              <Select filterable v-model="dataForm.days" placeholder="日期" style="width:200px">
                <Option :value="anHour">1 小时</Option>
                <Option v-for="item in dayList" :value="item" :key="item">{{ item }} 天</Option>
              </Select>
            </FormItem>
            <FormItem>
              <Button type="primary" ghost @click="queryGraph">查看</Button>
            </FormItem>
          </Form>
        </Card>
        <Card style="margin-top: 10px">
          <!-- <p slot="title">图表</p> -->
          <Tabs name="monitor-ecs" type="card">
            <TabPane label="系统监控" style="font-size: 14px" tab="monitor-ecs">
              <AliyunMonitorEcsSystem
              :pdataForm="dataForm"
              :pdiskIdObj="diskIdObj"
              :graphSignal="graphSignal"
              @closeGraphSignal="closeGraphSignal"></AliyunMonitorEcsSystem>
            </TabPane>
            <TabPane label="进程监控" tab="monitor-ecs" >Comming soon...</TabPane>
          </Tabs>
        </Card>
      </Col>
    </Row>
  </div>
</template>
<script>
import AliyunMonitorEcsSystem from './components/monitor_ecs_system'
import { getAccessKeyInfo, getAccessKey2Ecs } from '@/api/cmdb/aliyun/monitor'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'cmdb_aliyun_monitor_ecs',
  components: {
    AliyunMonitorEcsSystem
  },
  data () {
    return {
      hostnameSelectBool: true,
      accessKeyList: [],
      hostnameList: [],
      diskIdObj: {},
      labList: [],
      anHour: 0,
      dayList: [1, 3, 7, 30],
      graphSignal: false,
      dataForm: {
        'region_id': '',
        'key_name': '',
        'access_key_id': '',
        'instance_id': '',
        'days': 0
      },
      ruleDataForm: []
    }
  },
  methods: {
    // 查看图表
    queryGraph () {
      for (let idx in this.accessKeyList) {
        if (this.dataForm.access_key_id === this.accessKeyList[idx]['id']) {
          this.dataForm.key_name = this.accessKeyList[idx]['key_name']
          this.dataForm.region_id = this.accessKeyList[idx]['region_id']
        }
      }
      this.graphSignal = true
      console.log(this.dataForm)
      console.log(this.diskIdObj)
    },
    // 关闭graphSignal
    closeGraphSignal () {
      this.graphSignal = false
    },
    selectAccessKey (accessKey) {
      this.hostnameSelectBool = true
      getAccessKey2Ecs(this.dataForm.access_key_id).then(res => {
        this.hostnameList = res.data.filter(item => {
          return {
            'instance_id': item.instance_id,
            'hostname': item.hostname,
            'disk_id': JSON.parse(item.disk_id)
          }
        })
        this.hostnameSelectBool = false
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    selectHostname () {
      this.hostnameList.forEach(item => {
        if (item.instance_id === this.dataForm.instance_id) {
          this.diskIdObj = JSON.parse(item.disk_id)
        }
      })
    }
  },
  mounted () {
    getAccessKeyInfo().then(res => {
      this.accessKeyList = res.data.map(item => {
        return {
          'id': item.id,
          'key_name': item.key_name,
          'region_id': item.region_id
        }
      })
    }).catch(err => {
      sendNotice('error', err)
    })
  }
}
</script>
<style scoped>
.ivu-tabs-tab {
  font-size: 13px;
}
</style>
