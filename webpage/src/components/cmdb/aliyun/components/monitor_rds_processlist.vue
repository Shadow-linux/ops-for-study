<template>
  <div>
    <Row>
      <Col span="24">
        <br>
        <Card>
          <p slot="title">CPU / 内存 利用率(%)</p>
          <Spin v-if="graphSpin.cpu_mem" size="large" fix></Spin>
          <div  ref="cpuMemUsage" style="height: 150px; width: 100%"></div>
        </Card>
        <Divider orientation="left"><span class="divider-text">Process List</span></Divider>
        <Col span="10">
          <span style="color: #2d8cf0"><Icon type="ios-alert-outline" size="18"/>自动更新：频率10秒/次，周期3分钟，每点击一次查看增加周期</span>
        </Col>
        <Col span="4" offset="10">
          <Button type="default" style="margin-right: 15px" @click="stopRefresh">停止刷新</Button>
          <Button type="primary" ghost :loading="tableLoading" @click="refreshData" style="width: 92px">即刻刷新</Button>
        </Col>
        <br><br>
        <Col span="24">
          <Table :loading="tableLoading" :columns="tableColumns" :data="tableDatas"></Table>
        </Col>
      </Col>
    </Row>
  </div>
</template>
<script>
import { getRdsGraphData, getRdsProcessList } from '@/api/cmdb/aliyun/monitor'
import { sendNotice, stackChart } from '@/libs/util.js'
import { getDate } from '@/libs/tools.js'
export default {
  name: 'cmdb_aliyun_monitor_rds_processlist',
  data () {
    return {
      graphSpin: {
        cpu_mem: false
      },
      Timer: [],
      tableLoading: false,
      tableColumns: [
        {
          'title': 'THREAD ID',
          'key': 'id'
        },
        {
          'title': 'USER',
          'key': 'user'
        },
        {
          'title': 'HOST',
          'key': 'host',
          'width': 180
        },
        {
          'title': 'DATABASE',
          'key': 'db'
        },
        {
          'title': 'TIME(s)',
          'key': 'time'
        },
        {
          'title': 'COMMAND',
          'key': 'command'
        },
        {
          'title': 'STATE',
          'key': 'state'
        },
        {
          'title': 'INFO',
          'key': 'info',
          'ellipsis': true,
          'tooltip': true
        }
      ],
      tableDatas: []
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
        this.reloadTable()
        // time interval 如果连续按查看会堆叠次数
        // 现在设置每10秒执行 1次, 3分钟一个周期
        this.Timer.push(setInterval(() => {
          this.autoRefresh()
          console.log(this.Timer)
        }, 10000))
        setTimeout(() => {
          clearInterval(this.Timer[0])
          this.Timer = this.Timer.splice(1)
        }, 180000)
      }
      this.$emit('closeGraphSignal')
    }
  },
  methods: {
    stopRefresh () {
      this.Timer.forEach(item => {
        clearInterval(item)
      })
      this.Timer = []
      this.$Message.success('停止刷新')
    },
    refreshData () {
      this.reloadTable()
      let dd = new Date()
      let timestamp = parseInt(dd.getTime().toString().slice(0, 10))
      this.dataForm.end_time = getDate(timestamp, 'minute')
      this.cpuMemChart()
    },
    autoRefresh () {
      this.reloadTable()
    },
    reloadTable () {
      this.tableLoading = true
      getRdsProcessList(this.dataForm.id).then(res => {
        this.tableDatas = res.data
        this.tableLoading = false
      }).catch(err => {
        this.tableLoading = false
        sendNotice('error', err)
      })
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
