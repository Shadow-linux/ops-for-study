<template>
  <div>
    <Row :gutter="10">
      <Col span="24">
        <Divider orientation="left"><span class="divider-text"> CPU / 内存 / 系统负载 </span></Divider>
      </Col>
      <Col span="8">
        <Card>
          <p slot="title">CPU 使用率</p>
          <Spin v-if="graphSpin.cpu" size="large" fix></Spin>
          <div  ref="cpuTotal" style="height: 300px; width: 100%"></div>
        </Card>
      </Col>
      <Col span="8">
        <Card>
          <Spin v-if="graphSpin.mem" size="large" fix></Spin>
          <p slot="title">Memory 使用率</p>
          <div ref="memUsed" style="height: 300px; width: 100%"></div>
        </Card>
      </Col>
      <Col span="8">
        <Card>
          <Spin v-if="graphSpin.loadAyg" size="large" fix></Spin>
          <p slot="title">系统平均负载</p>
          <div ref="loadAvg" style="height: 300px; width: 100%"></div>
        </Card>
      </Col>
      <Col span="24">
        <Divider orientation="left"><span class="divider-text"> 网络监控指标 </span></Divider>
      </Col>
      <Col span="12">
        <Card>
          <p slot="title">公网流入流出速率(Kbps)</p>
          <Spin v-if="graphSpin.network" size="large" fix></Spin>
          <div ref="publicNetwork" style="height: 300px; width: 100%"></div>
        </Card>
      </Col>
      <Col span="12">
        <Card>
          <p slot="title">私网流入流出速率(Kbps)</p>
          <Spin v-if="graphSpin.network" size="large" fix></Spin>
          <div ref="privateNetwork" style="height: 300px; width: 100%"></div>
        </Card>
      </Col>
      <Col span="24">
        <Divider orientation="left"><span class="divider-text"> 磁盘监控指标 </span></Divider>
        <Form inline>
          <FormItem >
            <Select v-model="selectDiskId" @on-change="selectDiskhandle" style="width:200px">
              <Option value="system">系统盘</Option>
              <Option v-for="item in diskIdObjList" :value="item.diskId" :key="item.diskId">{{ item.name }}</Option>
            </Select>
          </FormItem>
        </Form>
      </Col>
      <div v-show="diskGraphShow">
        <Col span="12">
          <Card>
            <p slot="title">磁盘使用率</p>
            <Spin v-if="graphSpin.diskUsed" size="large" fix></Spin>
            <div ref="diskUsed" style="height: 300px; width: 100%"></div>
          </Card>
        </Col>
        <Col span="12">
          <Card>
            <p slot="title">读写字节数(KBps)</p>
            <Spin v-if="graphSpin.diskRW" size="large" fix></Spin>
            <div ref="diskRW" style="height: 300px; width: 100%"></div>
          </Card>
        </Col>
      </div>
    </Row>
  </div>
</template>
<script>

import { getGraphdata } from '@/api/cmdb/aliyun/monitor'
import { ChartLine } from '_c/charts'
import { getDate } from '@/libs/tools.js'
import echarts from 'echarts'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'cmdb_aliyun_monitor_ecs_system',
  components: {
    ChartLine
  },
  data () {
    return {
      diskGraphShow: false,
      graphSpin: {
        'cpu': false,
        'mem': false,
        'loadAyg': false,
        'network': false,
        'diskUsed': false,
        'diskRW': false
      },
      cpuSpin: false,
      selectDiskId: '',
      cpuTotalGraphObj: {}
    }
  },
  props: [
    'pdataForm',
    'pdiskIdObj',
    'graphSignal'
  ],
  computed: {
    // 磁盘列表
    diskIdObjList () {
      var retList = []
      for (let idx in this.pdiskIdObj) {
        retList.push({
          'diskId': this.pdiskIdObj[idx],
          'name': idx
        })
      }
      return retList
    }
  },
  watch: {
    graphSignal () {
      var keyName = this.pdataForm.key_name
      var action = 'ecs_graph'
      if (this.graphSignal) {
        // cpu 使用率
        this.graphCpuTotal(keyName, action)
        // Memory 使用量
        this.graphMemUsed(keyName, action)
        // load Avg
        this.graphLoadAyg(keyName, action)
        // 公网
        this.graphPublicNetwork(keyName, action)
        // 私网
        this.graphPrivateNetwork(keyName, action)
      }
      this.$emit('closeGraphSignal')
      this.diskGraphShow = false
    }
  },
  methods: {
    singleLineChart (xdatas, sdatas, ref, tags) {
      let dom = this.$refs[ref]
      let option = {
        title: {
          x: 'left'
        },
        dataZoom: [
          {
            type: 'slider',
            show: false,
            start: 0,
            end: 100
          },
          {
            type: 'inside',
            start: 1,
            end: 10
          },
          {
            type: 'slider',
            show: false,
            filterMode: 'empty',
            width: 12,
            handleSize: 8,
            showDataShadow: false,
            left: '100%'
          }
        ],
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: tags
        },
        xAxis: {
          type: 'category',
          data: xdatas
        },
        yAxis: {
          type: 'value'
        },
        series: sdatas
        // series: [{
        //   name: sname,
        //   data: sdatas,
        //   type: 'line'
        // }]
      }
      let myChart = echarts.init(dom)
      myChart.setOption(option)
    },
    // cpu 图表
    graphCpuTotal (keyName, action) {
      this.graphSpin.cpu = true
      let kwargs = {
        'metric': 'cpu_total',
        'region_id': this.pdataForm.region_id,
        'days': this.pdataForm.days,
        'dimensions': JSON.stringify([{ 'instanceId': this.pdataForm.instance_id }])
      }
      getGraphdata(keyName, action, JSON.stringify(kwargs)).then(res => {
        let xdatas = []
        let _sdatas = []
        let ref = 'cpuTotal'
        let tags = ['cpu_total']
        let sname = 'cpu_total'
        res.data.forEach(item => {
          let _timestampStr = item.timestamp.toString()
          let timestamp = parseInt(_timestampStr.substring(0, _timestampStr.length - 3))
          let time = getDate(timestamp, 'year')
          xdatas.push(time)
          _sdatas.push(item.Average)
        })
        let sdatas = {
          'type': 'line',
          'name': sname,
          'data': _sdatas
        }
        this.singleLineChart(xdatas, sdatas, ref, tags)
        this.graphSpin.cpu = false
      }).catch(err => {
        sendNotice('error', err)
        this.graphSpin.cpu = false
      })
    },
    // 内存图表
    graphMemUsed (keyName, action) {
      // metric 是由aliyun参数决定
      this.graphSpin.mem = true
      let kwargs = {
        'metric': 'memory_usedutilization',
        'region_id': this.pdataForm.region_id,
        'days': this.pdataForm.days,
        'dimensions': JSON.stringify([{ 'instanceId': this.pdataForm.instance_id }])
      }
      getGraphdata(keyName, action, JSON.stringify(kwargs)).then(res => {
        let xdatas = []
        let _sdatas = []
        let ref = 'memUsed'
        let tags = ['mem_used']
        let sname = 'mem_used'
        res.data.forEach(item => {
          let _timestampStr = item.timestamp.toString()
          let timestamp = parseInt(_timestampStr.substring(0, _timestampStr.length - 3))
          let time = getDate(timestamp, 'year')
          xdatas.push(time)
          _sdatas.push(item.Average)
        })
        let sdatas = {
          'type': 'line',
          'name': sname,
          'data': _sdatas
        }
        this.singleLineChart(xdatas, sdatas, ref, tags)
        this.graphSpin.mem = false
      }).catch(err => {
        sendNotice('eroor', err)
        this.graphSpin.mem = false
      })
    },
    // load avg
    graphLoadAyg (keyName, action) {
      // metric 是由aliyun参数决定
      this.graphSpin.loadAyg = true
      let kwargs = {
        'metric': 'load_1m',
        'region_id': this.pdataForm.region_id,
        'days': this.pdataForm.days,
        'dimensions': JSON.stringify([{ 'instanceId': this.pdataForm.instance_id }])
      }
      getGraphdata(keyName, action, JSON.stringify(kwargs)).then(res => {
        let xdatas = []
        let _sdatas = []
        let ref = 'loadAvg'
        let tags = ['load_1m']
        let sname = 'load_1m'
        res.data.forEach(item => {
          let _timestampStr = item.timestamp.toString()
          let timestamp = parseInt(_timestampStr.substring(0, _timestampStr.length - 3))
          let time = getDate(timestamp, 'year')
          xdatas.push(time)
          _sdatas.push(item.Average)
        })
        let sdatas = {
          'type': 'line',
          'name': sname,
          'data': _sdatas
        }
        this.singleLineChart(xdatas, sdatas, ref, tags)
        this.graphSpin.loadAyg = false
      }).catch(err => {
        sendNotice('error', err)
        this.graphSpin.loadAyg = false
      })
    },
    // 公网
    graphPublicNetwork (keyName, action) {
      this.graphSpin.network = true
      let ref = 'publicNetwork'
      let mOut = 'InternetOutRate'
      let mIn = 'InternetInRate'
      this.graphBaseNetwork(keyName, action, ref, mOut, mIn)
    },
    // 私网
    graphPrivateNetwork (keyName, action) {
      this.graphSpin.network = true
      let ref = 'privateNetwork'
      let mOut = 'IntranetOutRate'
      let mIn = 'IntranetInRate'
      this.graphBaseNetwork(keyName, action, ref, mOut, mIn)
    },
    graphBaseNetwork (keyName, action, ref, mOut, mIn) {
      // metric 是由aliyun参数决定
      var xdatas = []
      var tags = ['out', 'in']
      var sdatas = [
        {
          name: 'out',
          data: [],
          type: 'line'
        },
        {
          name: 'in',
          data: [],
          type: 'line'
        }
      ]
      var outkwargs = {
        'metric': mOut,
        'region_id': this.pdataForm.region_id,
        'days': this.pdataForm.days,
        'dimensions': JSON.stringify([{ 'instanceId': this.pdataForm.instance_id }])
      }
      getGraphdata(keyName, action, JSON.stringify(outkwargs)).then(res => {
        let _sdatas = []
        res.data.forEach(item => {
          _sdatas.push((item.Average / 1024.0).toFixed(2))
        })
        sdatas[0]['data'] = _sdatas
        var inkwargs = {
          'metric': mIn,
          'region_id': this.pdataForm.region_id,
          'days': this.pdataForm.days,
          'dimensions': JSON.stringify([{ 'instanceId': this.pdataForm.instance_id }])
        }
        getGraphdata(keyName, action, JSON.stringify(inkwargs)).then(res => {
          let _sdatas = []
          res.data.forEach(item => {
            let _timestampStr = item.timestamp.toString()
            let timestamp = parseInt(_timestampStr.substring(0, _timestampStr.length - 3))
            let time = getDate(timestamp, 'year')
            xdatas.push(time)
            _sdatas.push((item.Average / 1024.0).toFixed(2))
          })
          sdatas[1]['data'] = _sdatas
          this.singleLineChart(xdatas, sdatas, ref, tags)
          this.graphSpin.network = false
        })
      }).catch(err => {
        sendNotice('error', err)
        this.graphSpin.network = false
      })
    },
    // 选择查看的磁盘数据
    selectDiskhandle (diskId) {
      this.diskGraphShow = true
      var keyName = this.pdataForm.key_name
      var action = 'ecs_graph'
      var readMetric
      var writeMetric
      // 查看系统盘和挂载盘的API参数不一样
      if (diskId === 'system') {
        readMetric = 'DiskReadBPS'
        writeMetric = 'DiskWriteBPS'
      } else {
        readMetric = 'disk_readbytes'
        writeMetric = 'disk_writebytes'
        // 系统盘没有使用率
        this.graphDiskUsed(keyName, action, diskId)
      }
      this.graphDiskRW(keyName, action, diskId, readMetric, writeMetric)
    },
    // 挂载磁盘使用率
    graphDiskUsed (keyName, action, diskId) {
      this.graphSpin.diskUsed = true
      let kwargs = {
        'metric': 'diskusage_utilization',
        'region_id': this.pdataForm.region_id,
        'days': this.pdataForm.days,
        'dimensions': JSON.stringify([{ 'instanceId': this.pdataForm.instance_id }, { 'device': diskId }])
      }
      getGraphdata(keyName, action, JSON.stringify(kwargs)).then(res => {
        let xdatas = []
        let _sdatas = []
        let ref = 'diskUsed'
        let tags = ['disk_used']
        let sname = 'disk_used'
        res.data.forEach(item => {
          let _timestampStr = item.timestamp.toString()
          let timestamp = parseInt(_timestampStr.substring(0, _timestampStr.length - 3))
          let time = getDate(timestamp, 'year')
          xdatas.push(time)
          _sdatas.push(item.Average)
        })
        let sdatas = {
          'type': 'line',
          'name': sname,
          'data': _sdatas
        }
        this.singleLineChart(xdatas, sdatas, ref, tags)
        this.graphSpin.diskUsed = false
      }).catch(err => {
        sendNotice('error', err)
        this.graphSpin.diskUsed = false
      })
    },
    // 挂载磁盘读写
    graphDiskRW (keyName, action, diskId, readMetric, writeMetric) {
      this.graphSpin.diskRW = true
      var ref = 'diskRW'
      var xdatas = []
      var tags = ['read', 'write']
      var sdatas = [
        {
          name: 'read',
          data: [],
          type: 'line'
        },
        {
          name: 'write',
          data: [],
          type: 'line'
        }
      ]
      let readkwargs = {
        'metric': readMetric,
        'region_id': this.pdataForm.region_id,
        'days': this.pdataForm.days,
        'dimensions': JSON.stringify([{ 'instanceId': this.pdataForm.instance_id }, { 'device': diskId }])
      }
      getGraphdata(keyName, action, JSON.stringify(readkwargs)).then(res => {
        let _sdatas = []
        res.data.forEach(item => {
          _sdatas.push((item.Average / 1024.0).toFixed(2))
        })
        sdatas[0]['data'] = _sdatas
        let writekwargs = {
          'metric': writeMetric,
          'region_id': this.pdataForm.region_id,
          'days': this.pdataForm.days,
          'dimensions': JSON.stringify([{ 'instanceId': this.pdataForm.instance_id }, { 'device': diskId }])
        }
        getGraphdata(keyName, action, JSON.stringify(writekwargs)).then(res => {
          let _sdatas = []
          res.data.forEach(item => {
            let _timestampStr = item.timestamp.toString()
            let timestamp = parseInt(_timestampStr.substring(0, _timestampStr.length - 3))
            let time = getDate(timestamp, 'year')
            xdatas.push(time)
            _sdatas.push((item.Average / 1024.0).toFixed(2))
          })
          sdatas[1]['data'] = _sdatas
          console.log(sdatas)
          this.singleLineChart(xdatas, sdatas, ref, tags)
          this.graphSpin.diskRW = false
        })
      }).catch(err => {
        sendNotice('error', err)
        this.graphSpin.diskRW = false
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
