<template>
  <div>
    <Card>
      <p slot="title">查询</p>
      <Form ref="" :model="dataForm" inline>
        <FormItem label="">
          <Select filterable v-model="dataForm.access_key_id" placeholder="AccessKey" style="width:200px" @on-change="selectAccessKey">
            <Option v-for="item in accessKeyList" :value="item.id" :key="item.id">{{ item.key_name }}</Option>
          </Select>
        </FormItem>
        <FormItem label="">
          <Select filterable v-model="dataForm.id" :disabled="rdsSelectBool" placeholder="实例名称" style="width:200px">
            <Option v-for="item in rdsList" :value="item.id" :key="item.id">{{ item.instance_desc }}</Option>
          </Select>
        </FormItem>
        <FormItem>
          <DatePicker
          type="datetimerange"
          format="yyyy-MM-dd HH:mm"
          placeholder="选择日期时间"
          style="width: 250px"
          :value="timePicker"
          @on-change="setDateTime">
          </DatePicker>
        </FormItem>
        <FormItem>
          <Button type="primary" ghost @click="queryGraph">查看</Button>
        </FormItem>
      </Form>
    </Card>
    <Card style="margin-top: 10px;">
      <Tabs type="card" name="monitor-rds" >
        <TabPane label="实时进程" tab="monitor-rds">
          <MonitorRdsProcessList
          :dataForm="dataForm"
          :graphSignal="processListGraphSignal"
          @closeGraphSignal="processListCloseGraphSignal"
          ></MonitorRdsProcessList>
        </TabPane>
        <TabPane label="资源监控" tab="monitor-rds">
          <MonitorRdsResource
          :dataForm="dataForm"
          :graphSignal="resourcGraphSignal"
          @closeGraphSignal="resourceCloseGraphSignal"
          ></MonitorRdsResource>
        </TabPane>
        <TabPane label="引擎监控" tab="monitor-rds">
          <MonitorRdsEngine
          :dataForm="dataForm"
          :graphSignal="engineGraphSignal"
          @closeGraphSignal="engineCloseGraphSignal"
          ></MonitorRdsEngine>
        </TabPane>
    </Tabs>
    </Card>
  </div>
</template>
<script>
import { getAccessKeyInfo, getAccessKey2Rds } from '@/api/cmdb/aliyun/monitor'
import MonitorRdsResource from './components/monitor_rds_resource'
import MonitorRdsEngine from './components/monitor_rds_engine'
import MonitorRdsProcessList from './components/monitor_rds_processlist'
import { sendNotice } from '@/libs/util.js'
import { getDate } from '@/libs/tools.js'
export default {
  name: 'cmdb_aliyun_monitor_rds',
  components: {
    MonitorRdsResource,
    MonitorRdsEngine,
    MonitorRdsProcessList
  },
  data () {
    const dd = new Date()
    const timestamp = parseInt(dd.getTime().toString().slice(0, 10))
    const startTime = getDate(timestamp - 3600, 'minute')
    const endTime = getDate(timestamp, 'minute')
    return {
      timePicker: [startTime, endTime],
      accessKeyList: [],
      rdsList: [],
      rdsSelectBool: true,
      resourcGraphSignal: false,
      engineGraphSignal: false,
      processListGraphSignal: false,
      dataForm: {
        access_key_id: '',
        id: '',
        start_time: startTime,
        end_time: endTime
      }
    }
  },
  methods: {
    // 关闭graphSignal
    resourceCloseGraphSignal () {
      this.resourcGraphSignal = false
    },
    engineCloseGraphSignal () {
      this.engineGraphSignal = false
    },
    processListCloseGraphSignal () {
      this.processListGraphSignal = false
    },
    queryGraph () {
      this.resourcGraphSignal = true
      this.engineGraphSignal = true
      this.processListGraphSignal = true
      console.log(this.dataForm)
    },
    setDateTime (date) {
      this.dataForm['start_time'] = date[0]
      this.dataForm['end_time'] = date[1]
    },
    selectAccessKey (accessKey) {
      this.rdsSelectBool = true
      getAccessKey2Rds(this.dataForm.access_key_id).then(res => {
        this.rdsList = res.data.filter(item => {
          return {
            'id': item.id,
            'instance_desc': item.instance_desc
          }
        })
        this.rdsSelectBool = false
      }).catch(err => {
        sendNotice('error', err)
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
