<template>
  <div>
    <Row :gutter="10">
      <br>
      <Col span="2" offset="22">
        <Button type="primary" ghost @click="refreshData">即刻刷新</Button>
      </Col>
      <Col span="24">
        <Divider orientation="left"><span class="divider-text">CPU / 内存 / IOPS </span></Divider>
      </Col>
      <Col span="12">
        <Card>
          <p slot="title">CPU / 内存 利用率(%)</p>
          <Spin v-if="graphSpin.cpu_mem" size="large" fix></Spin>
          <div  ref="cpuMemUsage" style="height: 300px; width: 100%"></div>
        </Card>
      </Col>
      <Col span="12">
        <Card>
          <p slot="title">IOPS（单位:次/秒）</p>
          <Spin v-if="graphSpin.iops" size="large" fix></Spin>
          <div  ref="IOPS" style="height: 300px; width: 100%"></div>
        </Card>
      </Col>
    </Row>
    <Divider orientation="left"><span class="divider-text">连接数 / 网络流量 </span></Divider>
    <Row :gutter="10">
      <Col span="12">
        <Card>
          <p slot="title">当前总连接数</p>
          <Spin v-if="graphSpin.session" size="large" fix></Spin>
          <div  ref="session" style="height: 300px; width: 100%"></div>
        </Card>
      </Col>
      <Col span="12">
        <Card>
          <p slot="title">网络流量（单位KB)</p>
          <Spin v-if="graphSpin.network" size="large" fix></Spin>
          <div  ref="netowrkTraffic" style="height: 300px; width: 100%"></div>
        </Card>
      </Col>
    </Row>
  </div>
</template>
<script>
import { getRdsGraphData } from '@/api/cmdb/aliyun/monitor'
import { sendNotice, stackChart } from '@/libs/util.js'
import { getDate } from '@/libs/tools.js'
export default {
  name: 'cmdb_aliyun_monitor_rds_resource',
  data () {
    return {
      graphSpin: {
        cpu_mem: false,
        iops: false,
        session: false,
        network: false
      }
    }
  },
  props: [
    'dataForm',
    'graphSignal'
  ],
  watch: {
    graphSignal () {
      if (this.graphSignal) {
        this.cpuMemChart()
        this.iopsChart()
        this.sessionChart()
        this.networkChart()
      }
      this.$emit('closeGraphSignal')
    }
  },
  methods: {
    refreshData () {
      let dd = new Date()
      let timestamp = parseInt(dd.getTime().toString().slice(0, 10))
      this.dataForm.end_time = getDate(timestamp, 'minute')
      this.cpuMemChart()
      this.iopsChart()
      this.sessionChart()
      this.networkChart()
    },
    cpuMemChart () {
      this.graphSpin.cpu_mem = true
      getRdsGraphData(this.dataForm.id, 'MySQL_MemCpuUsage', this.dataForm.start_time, this.dataForm.end_time).then(res => {
        let xdata = []
        let sdata = []
        let cpu = []
        let mem = []
        let ldata = ['cpu', 'mem']
        res.data.forEach(item => {
          xdata.push(item.date)
          let ii = item.value.split('&')
          mem.push(ii[1])
          cpu.push(ii[0])
        })
        sdata.push({
          name: 'cpu',
          type: 'line',
          areaStyle: {},
          data: cpu
        })
        sdata.push({
          name: 'mem',
          type: 'line',
          areaStyle: {},
          data: mem
        })
        stackChart(this, xdata, sdata, 'cpuMemUsage', ldata)
        this.graphSpin.cpu_mem = false
      }).catch(err => {
        this.graphSpin.cpu_mem = false
        sendNotice('error', err)
      })
    },
    iopsChart () {
      this.graphSpin.iops = true
      getRdsGraphData(this.dataForm.id, 'MySQL_IOPS', this.dataForm.start_time, this.dataForm.end_time).then(res => {
        let xdata = []
        let sdata = []
        let ldata = ['IOPS']
        let iops = []
        res.data.forEach(item => {
          xdata.push(item.date)
          iops.push(item.value)
        })
        sdata.push({
          name: 'IOPS',
          type: 'line',
          areaStyle: {},
          data: iops
        })
        stackChart(this, xdata, sdata, 'IOPS', ldata)
        this.graphSpin.iops = false
      }).catch(err => {
        this.graphSpin.iops = false
        sendNotice('error', err)
      })
    },
    sessionChart () {
      this.graphSpin.session = true
      getRdsGraphData(this.dataForm.id, 'MySQL_Sessions', this.dataForm.start_time, this.dataForm.end_time).then(res => {
        let xdata = []
        let sdata = []
        let ldata = ['active_session', 'total_session']
        let totalSession = []
        let activeSession = []
        res.data.forEach(item => {
          xdata.push(item.date)
          let ii = item.value.split('&')
          totalSession.push(ii[1])
          activeSession.push(ii[0])
        })
        sdata.push({
          name: 'active_session',
          type: 'line',
          areaStyle: {},
          data: activeSession
        })
        sdata.push({
          name: 'total_session',
          type: 'line',
          areaStyle: {},
          data: totalSession
        })
        stackChart(this, xdata, sdata, 'session', ldata)
        this.graphSpin.session = false
      }).catch(err => {
        sendNotice('error', err)
        this.graphSpin.session = false
      })
    },
    networkChart () {
      this.graphSpin.network = true
      getRdsGraphData(this.dataForm.id, 'MySQL_NetworkTraffic', this.dataForm.start_time, this.dataForm.end_time).then(res => {
        let xdata = []
        let ldata = ['received', 'sent']
        let recvk = []
        let sentk = []
        res.data.forEach(item => {
          xdata.push(item.date)
          let ii = item.value.split('&')
          sentk.push(ii[1])
          recvk.push(ii[0])
        })
        let sdata = [
          {
            name: 'received',
            type: 'line',
            areaStyle: {},
            data: recvk
          },
          {
            name: 'sent',
            type: 'line',
            areaStyle: {},
            data: sentk
          }
        ]
        stackChart(this, xdata, sdata, 'netowrkTraffic', ldata)
        this.graphSpin.network = false
      }).catch(err => {
        sendNotice('error', err)
        this.graphSpin.network = false
      })
    }
  },
  mounted () {
  }
}
</script>
<style scoped>
.divider-text {
  color: #909399;
  font-size: 14px;
}
</style>
