<template>
  <div>
    <Alert show-icon> docker容器指标监控可视化（App 需要设置server为docker, 及其绑定docker的Host需把tag的key设置为docker）</Alert>
    <Card>
      <p slot="title">查询</p>
      <Form ref="queryForm" :model="dataForm" :rules="ruleDataForm" inline>
        <FormItem label="" prop="app">
          <Select v-model="dataForm.app" style="width:200px" filterable placeholder="App名" @on-change="getEpList">
            <Option v-for="item in appList" :value="item.app_name" :key="item.id">{{ item.app_name }}</Option>
          </Select>
        </FormItem>
        <FormItem label="" prop="ep">
          <Select v-model="dataForm.ep" style="width:300px" multiple filterable placeholder="主机名">
            <Option v-for="item in epList" :value="item" :key="item.id">{{ item }}</Option>
          </Select>
        </FormItem>
        <FormItem label="">
          <Select v-model="dataForm.hours" style="width:200px" filterable placeholder="时间">
            <Option :value="1">1 小时</Option>
            <Option :value="24">1 天</Option>
            <Option :value="72">3 天</Option>
            <Option :value="168">7 天</Option>
          </Select>
        </FormItem>
        <FormItem label="">
          <Button type="primary" @click="queryGraph" ghost>查看</Button>
        </FormItem>
      </Form>
    </Card>
    <Card style="margin-top: 10px">
      <p slot="title">监控图表</p>
      <Spin v-if="graphSpin" size="large" fix></Spin>
      <Divider orientation="left"><span class="divider-text"> CPU / 系统负载  </span></Divider>
      <Row :gutter="10">
        <Col span="12" >
          <Card>
            <p slot="title">CPU 使用率(%)</p>
            <div  ref="cpuUsedPercent" style="height: 300px; width: 100%"></div>
          </Card>
        </Col>
        <Col span="12">
          <Card>
            <p slot="title">系统平均负载</p>
            <div  ref="loadAvg" style="height: 300px; width: 100%"></div>
          </Card>
        </Col>
      </Row>
      <Divider orientation="left"><span class="divider-text"> 内存指标 </span></Divider>
      <Row :gutter="10">
        <Col span="12">
          <Card>
            <p slot="title">Memory 使用率(%)</p>
            <div  ref="memoryUsedPercent" style="height: 300px; width: 100%"></div>
          </Card>
        </Col>
        <Col span="12" >
          <Card>
            <p slot="title">Memory 使用 (MB)</p>
            <div  ref="memoryUsed" style="height: 300px; width: 100%"></div>
          </Card>
        </Col>
      </Row>
      <Divider orientation="left"><span class="divider-text"> 网络指标 </span></Divider>
      <Row :gutter="10">
        <Col span="12" >
          <Card>
            <p slot="title">Network [IN] (MB)</p>
            <div  ref="networkIn" style="height: 300px; width: 100%"></div>
          </Card>
        </Col>
        <Col span="12">
          <Card>
            <p slot="title">Network [OUT] (MB)</p>
            <div  ref="networkOut" style="height: 300px; width: 100%"></div>
          </Card>
        </Col>
      </Row>
    </Card>
  </div>
</template>
<script>
import { getAppList, getDockerAppGraph } from '@/api/monitor/docker.js'
import { sendNotice, lineChart } from '@/libs/util.js'

export default {
  name: 'monitor_docker',
  data () {
    return {
      originAppList: [],
      appList: [],
      epList: [],
      dataForm: {
        'app': '',
        'ep': [],
        'hours': 1
      },
      graphSpin: false,
      ruleDataForm: {
        app: [
          { required: true, message: 'The app cannot be empty', trigger: 'change' }
        ],
        ep: [
          { required: true, type: 'array', message: 'The ep cannot be empty', trigger: 'change' }
        ]
      }
    }
  },
  methods: {
    getRelAppList () {
      this.appList = this.originAppList.filter(item => {
        // app 需要带有server 为docker 的应用
        if (item.service === 'docker' && item.is_active) {
          for (let env in item.host_list) {
            let hostInfoList = item.host_list[env]
            for (let idx in hostInfoList) {
              let tags = hostInfoList[idx]['tags']
              for (let tidx in tags) {
                // app 绑定的host 也需要带有 docker 标记，才返回到展示列表
                if (tags[tidx].key === 'docker') {
                  return item
                }
              }
            }
          }
        }
      })
    },
    getEpList (choseVal) {
      this.epList = []
      this.dataForm.ep = []
      this.originAppList.forEach(item => {
        if (item.app_name === choseVal) {
          for (let env in item.host_list) {
            let hostInfoList = item.host_list[env]
            for (let idx in hostInfoList) {
              let hostInfo = hostInfoList[idx]
              console.log(hostInfo)
              let tags = hostInfo['tags']
              for (let tidx in tags) {
                // app 绑定的host 也需要带有 docker 标记，才返回到展示列表
                if (tags[tidx].key === 'docker') {
                  console.log(hostInfo['hostname'])
                  this.epList.push(hostInfo['hostname'])
                }
              }
            }
          }
        }
      })
    },
    baseGraph (counter, ep, ref) {
      getDockerAppGraph(counter, JSON.stringify(ep), parseInt(this.dataForm.hours)).then(res => {
        let xdatas = res.data.time
        let sdatas = []
        let tags = []
        for (let idx in res.data.data) {
          let item = res.data.data[idx]
          tags.push(item['ep'])
          sdatas.push({
            name: item['ep'],
            data: item['values'],
            type: 'line'
          })
        }
        lineChart(this, xdatas, sdatas, ref, tags)
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    // 数值转换为MB
    mbGraph (counter, ep, ref) {
      getDockerAppGraph(counter, JSON.stringify(ep), parseInt(this.dataForm.hours)).then(res => {
        let xdatas = res.data.time
        let sdatas = []
        let tags = []
        for (let idx in res.data.data) {
          let item = res.data.data[idx]
          tags.push(item['ep'])
          let values = item['values'].map(dd => {
            return dd / 1024 / 1024
          })
          sdatas.push({
            name: item['ep'],
            data: values,
            type: 'line'
          })
        }
        lineChart(this, xdatas, sdatas, ref, tags)
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    loadAvgGraph () {
      let ep = this.dataForm.ep
      let counter = `docker.load.1min/app=${this.dataForm.app}`
      this.baseGraph(counter, ep, 'loadAvg')
    },
    cpuGraph () {
      let ep = this.dataForm.ep
      let counter = `docker.cpu.used.percent/app=${this.dataForm.app}`
      this.baseGraph(counter, ep, 'cpuUsedPercent')
    },
    memoryUsedPercentGraph () {
      let ep = this.dataForm.ep
      let counter = `docker.mem.used.percent/app=${this.dataForm.app}`
      this.baseGraph(counter, ep, 'memoryUsedPercent')
    },
    memoryUsed () {
      let ep = this.dataForm.ep
      let counter = `docker.mem.used/app=${this.dataForm.app}`
      this.mbGraph(counter, ep, 'memoryUsed')
    },
    networkIn () {
      let ep = this.dataForm.ep
      let counter = `docker.net.if.in.bytes/app=${this.dataForm.app}`
      this.mbGraph(counter, ep, 'networkIn')
    },
    networkOut () {
      let ep = this.dataForm.ep
      let counter = `docker.net.if.out.bytes/app=${this.dataForm.app}`
      this.mbGraph(counter, ep, 'networkOut')
    },
    queryGraph () {
      this.$refs['queryForm'].validate((valid) => {
        if (valid) {
          this.graphSpin = true
          this.cpuGraph()
          this.loadAvgGraph()
          this.memoryUsedPercentGraph()
          this.memoryUsed()
          this.networkIn()
          this.networkOut()
          setTimeout(() => { this.graphSpin = false }, 1000)
        } else {
          this.$Message.error('查询失败')
        }
      })
    }
  },
  mounted () {
    getAppList().then(res => {
      this.originAppList = res.data
      this.getRelAppList()
      console.log(this.appList)
    }).catch(err => {
      sendNotice('error', err)
    })
  }
}
</script>
<style scoped>
.divider-text {
  color: #909399;
  font-size: 14px;
}
</style>
