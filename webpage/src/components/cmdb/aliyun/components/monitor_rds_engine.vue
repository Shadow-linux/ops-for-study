<template>
  <div>
    <br>
    <Row :gutter="10">
      <Col span="2" offset="22">
        <Button type="primary" ghost @click="refreshData">即刻刷新</Button>
      </Col>
      <br><br>
      <Col span="12">
        <Card>
          <p slot="title">TPS(平均每秒事务数）/QPS(平均每秒SQL语句执行次数)</p>
          <Spin v-if="graphSpin.tps_qps" size="large" fix></Spin>
          <div  ref="tpsqps" style="height: 300px; width: 100%"></div>
        </Card>
      </Col>
      <Col span="12">
        <Card>
          <p slot="title">InnoDB缓存读命中率、使用率、脏块率(%)</p>
          <Spin v-if="graphSpin.innodbbuffer" size="large" fix></Spin>
          <div  ref="innodbbuffer" style="height: 300px; width: 100%"></div>
        </Card>
      </Col>
    </Row>
    <br>
    <Row :gutter="10">
      <Col span="12">
        <Card>
          <p slot="title">InnoDB读写量（单位为KB）</p>
          <Spin v-if="graphSpin.innodbdatarw" size="large" fix></Spin>
          <div  ref="innodbdatarw" style="height: 300px; width: 100%"></div>
        </Card>
      </Col>
      <Col span="12">
        <Card>
          <p slot="title">InnoDB缓存请求次数</p>
          <Spin v-if="graphSpin.innodblogrequests" size="large" fix></Spin>
          <div  ref="innodblogrequests" style="height: 300px; width: 100%"></div>
        </Card>
      </Col>
    </Row>
    <br>
    <Row :gutter="10">
      <Col span="12">
        <Card>
          <p slot="title">InnoDB日志读/写/fsync</p>
          <Spin v-if="graphSpin.innodblogwrites" size="large" fix></Spin>
          <div  ref="innodblogwrites" style="height: 300px; width: 100%"></div>
        </Card>
      </Col>
      <Col span="12">
        <Card>
          <p slot="title">MySQL执行语句时在硬盘上自动创建的临时表的数量</p>
          <Spin v-if="graphSpin.tempdisktablecreates" size="large" fix></Spin>
          <div  ref="tempdisktablecreates" style="height: 300px; width: 100%"></div>
        </Card>
      </Col>
    </Row>
    <br>
    <Row>
      <Col span="24">
        <Card>
          <p slot="title">MySQL_COMDML</p>
          <Spin v-if="graphSpin.comdml" size="large" fix></Spin>
          <div  ref="comdml" style="height: 300px; width: 100%"></div>
        </Card>
      </Col>
    </Row>
    <br>
    <Row>
      <Col span="24">
        <Card>
          <p slot="title">MySQL_RowDML</p>
          <Spin v-if="graphSpin.rowdml" size="large" fix></Spin>
          <div  ref="rowdml" style="height: 300px; width: 100%"></div>
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
  name: 'cmdb_aliyun_monitor_rds_engine',
  data () {
    return {
      graphSpin: {
        tps_qps: false,
        innodbbuffer: false,
        innodbdatarw: false,
        innodblogrequests: false,
        innodblogwrites: false,
        tempdisktablecreates: false,
        comdml: false,
        rowdml: false,
        myisamkeyreadwrites: false,
        myisamkeybufferratio: false
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
        this.tpsqpsChart()
        this.innodbbufferChart()
        this.innodbdatarwChart()
        this.innodblogrequestsChart()
        this.innodblogwritesChart()
        this.tempdisktablecreatesChart()
        this.comdmlChart()
        this.rowdmlChart()
      }
      this.$emit('closeGraphSignal')
    }
  },
  methods: {
    refreshData () {
      let dd = new Date()
      let timestamp = parseInt(dd.getTime().toString().slice(0, 10))
      this.dataForm.end_time = getDate(timestamp, 'minute')
      this.tpsqpsChart()
      this.innodbbufferChart()
      this.innodbdatarwChart()
      this.innodblogrequestsChart()
      this.innodblogwritesChart()
      this.tempdisktablecreatesChart()
      this.comdmlChart()
      this.rowdmlChart()
    },
    tpsqpsChart () {
      this.graphSpin.tps_qps = true
      getRdsGraphData(this.dataForm.id, 'MySQL_QPSTPS', this.dataForm.start_time, this.dataForm.end_time).then(res => {
        let xdata = []
        let qps = []
        let tps = []
        let ldata = ['QPS', 'TPS']
        res.data.forEach(item => {
          xdata.push(item.date)
          let ii = item.value.split('&')
          tps.push(ii[1])
          qps.push(ii[0])
        })
        let sdata = [
          {
            name: 'QPS',
            type: 'line',
            areaStyle: {},
            data: qps
          },
          {
            name: 'TPS',
            type: 'line',
            areaStyle: {},
            data: tps
          }
        ]
        stackChart(this, xdata, sdata, 'tpsqps', ldata)
        this.graphSpin.tps_qps = false
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    innodbbufferChart () {
      this.graphSpin.innodbbuffer = true
      getRdsGraphData(this.dataForm.id, 'MySQL_InnoDBBufferRatio', this.dataForm.start_time, this.dataForm.end_time).then(res => {
        let xdata = []
        let ibufreadhit = []
        let ibufuseratio = []
        let ibufdirtyratio = []
        let ldata = ['缓存读命中率', '缓存使用率', '缓存脏块率']
        res.data.forEach(item => {
          xdata.push(item.date)
          let ii = item.value.split('&')
          ibufreadhit.push(ii[0])
          ibufuseratio.push(ii[1])
          ibufdirtyratio.push(ii[2])
        })
        let sdata = [
          {
            name: '缓存读命中率',
            type: 'line',
            areaStyle: {},
            data: ibufreadhit
          },
          {
            name: '缓存使用率',
            type: 'line',
            areaStyle: {},
            data: ibufuseratio
          },
          {
            name: '缓存脏块率',
            type: 'line',
            areaStyle: {},
            data: ibufdirtyratio
          }
        ]
        stackChart(this, xdata, sdata, 'innodbbuffer', ldata)
        this.graphSpin.innodbbuffer = false
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    innodbdatarwChart () {
      this.graphSpin.innodbdatarw = true
      getRdsGraphData(this.dataForm.id, 'MySQL_InnoDBDataReadWriten', this.dataForm.start_time, this.dataForm.end_time).then(res => {
        let xdata = []
        let innodataread = []
        let innodatawritten = []
        let ldata = ['平均每秒钟读取', '平均每秒钟写入']
        res.data.forEach(item => {
          xdata.push(item.date)
          let ii = item.value.split('&')
          innodataread.push(ii[0])
          innodatawritten.push(ii[1])
        })
        let sdata = [
          {
            name: '平均每秒钟读取',
            type: 'line',
            areaStyle: {},
            data: innodataread
          },
          {
            name: '平均每秒钟写入',
            type: 'line',
            areaStyle: {},
            data: innodatawritten
          }
        ]
        stackChart(this, xdata, sdata, 'innodbdatarw', ldata)
        this.graphSpin.innodbdatarw = false
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    innodblogrequestsChart () {
      this.graphSpin.innodblogrequests = true
      getRdsGraphData(this.dataForm.id, 'MySQL_InnoDBLogRequests', this.dataForm.start_time, this.dataForm.end_time).then(res => {
        let xdata = []
        let ibufrequestr = []
        let ibufrequestw = []
        let ldata = ['平均每秒向InnoDB缓冲池的读次数', '平均每秒向InnoDB缓冲池的写次数']
        res.data.forEach(item => {
          xdata.push(item.date)
          let ii = item.value.split('&')
          ibufrequestr.push(ii[0])
          ibufrequestw.push(ii[1])
        })
        let sdata = [
          {
            name: '平均每秒向InnoDB缓冲池的读次数',
            type: 'line',
            areaStyle: {},
            data: ibufrequestr
          },
          {
            name: '平均每秒向InnoDB缓冲池的写次数',
            type: 'line',
            areaStyle: {},
            data: ibufrequestw
          }
        ]
        stackChart(this, xdata, sdata, 'innodblogrequests', ldata)
        this.graphSpin.innodblogrequests = false
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    innodblogwritesChart () {
      this.graphSpin.innodblogwrites = true
      getRdsGraphData(this.dataForm.id, 'MySQL_InnoDBLogWrites', this.dataForm.start_time, this.dataForm.end_time).then(res => {
        let xdata = []
        let Innodblogwriterequests = []
        let Innodblogwrites = []
        let Innodboslogfsyncs = []
        let ldata = ['平均每秒日志写请求数', '平均每秒向日志文件的物理写次数', '平均每秒向日志文件完成的fsync()写数量']
        res.data.forEach(item => {
          xdata.push(item.date)
          let ii = item.value.split('&')
          Innodblogwriterequests.push(ii[0])
          Innodblogwrites.push(ii[1])
          Innodboslogfsyncs.push(ii[2])
        })
        let sdata = [
          {
            name: '平均每秒日志写请求数',
            type: 'line',
            areaStyle: {},
            data: Innodblogwriterequests
          },
          {
            name: '平均每秒向日志文件的物理写次数',
            type: 'line',
            areaStyle: {},
            data: Innodblogwrites
          },
          {
            name: '平均每秒向日志文件完成的fsync()写数量',
            type: 'line',
            areaStyle: {},
            data: Innodboslogfsyncs
          }
        ]
        stackChart(this, xdata, sdata, 'innodblogwrites', ldata)
        this.graphSpin.innodblogwrites = false
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    // comdmlChart MySQL_COMDML
    comdmlChart () {
      this.graphSpin.comdml = true
      getRdsGraphData(this.dataForm.id, 'MySQL_COMDML', this.dataForm.start_time, this.dataForm.end_time).then(res => {
        let xdata = []
        let comdelete = []
        let cominsert = []
        let cominsertselect = []
        let comreplace = []
        let comreplaceselect = []
        let comselect = []
        let comupdate = []
        let ldata = [
          '平均每秒Delete语句执行次数',
          '平均每秒Insert语句执行次数',
          '平均每秒Insert_Select语句执行次数',
          '平均每秒Replace语句执行次数',
          '平均每秒Replace_Select语句执行次数',
          '平均每秒Select语句执行次数',
          '平均每秒Update语句执行次数'
        ]
        res.data.forEach(item => {
          xdata.push(item.date)
          let ii = item.value.split('&')
          comdelete.push(ii[0])
          cominsert.push(ii[1])
          cominsertselect.push(ii[2])
          comreplace.push(ii[3])
          comreplaceselect.push(ii[4])
          comselect.push(ii[5])
          comupdate.push(ii[6])
        })
        let sdata = [
          {
            name: '平均每秒Delete语句执行次数',
            type: 'line',
            areaStyle: {},
            data: comdelete
          },
          {
            name: '平均每秒Insert语句执行次数',
            type: 'line',
            areaStyle: {},
            data: cominsert
          },
          {
            name: '平均每秒Insert_Select语句执行次数',
            type: 'line',
            areaStyle: {},
            data: cominsertselect
          },
          {
            name: '平均每秒Replace语句执行次数',
            type: 'line',
            areaStyle: {},
            data: comreplace
          },
          {
            name: '平均每秒Replace_Select语句执行次数',
            type: 'line',
            areaStyle: {},
            data: comreplaceselect
          },
          {
            name: '平均每秒Select语句执行次数',
            type: 'line',
            areaStyle: {},
            data: comselect
          },
          {
            name: '平均每秒Update语句执行次数',
            type: 'line',
            areaStyle: {},
            data: comupdate
          }
        ]
        stackChart(this, xdata, sdata, 'comdml', ldata)
        this.graphSpin.comdml = false
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    tempdisktablecreatesChart () {
      this.graphSpin.tempdisktablecreates = true
      getRdsGraphData(this.dataForm.id, 'MySQL_TempDiskTableCreates', this.dataForm.start_time, this.dataForm.end_time).then(res => {
        let xdata = []
        let values = []
        let ldata = ['自动创建的临时表的数量']
        res.data.forEach(item => {
          xdata.push(item.date)
          values.push(item.value)
        })
        let sdata = [
          {
            name: '自动创建的临时表的数量',
            type: 'line',
            areaStyle: {},
            data: values
          }
        ]
        stackChart(this, xdata, sdata, 'tempdisktablecreates', ldata)
        this.graphSpin.tempdisktablecreates = false
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    rowdmlChart () {
      this.graphSpin.rowdml = true
      getRdsGraphData(this.dataForm.id, 'MySQL_RowDML', this.dataForm.start_time, this.dataForm.end_time).then(res => {
        let xdata = []
        let ldata = [
          '平均每秒从InnoDB表读取的行数',
          '平均每秒从InnoDB表更新的行数',
          '平均每秒从InnoDB表删除的行数',
          '平均每秒从InnoDB表插入的行数',
          '平均每秒向日志文件的物理写次数'
        ]
        let innorowreaded = []
        let innorowupdate = []
        let innorowdelete = []
        let innorowinsert = []
        let Innologwrites = []
        res.data.forEach(item => {
          xdata.push(item.date)
          let ii = item.value.split('&')
          innorowreaded.push(ii[0])
          innorowupdate.push(ii[1])
          innorowdelete.push(ii[2])
          innorowinsert.push(ii[3])
          Innologwrites.push(ii[4])
        })
        let sdata = [
          {
            name: '平均每秒从InnoDB表读取的行数',
            type: 'line',
            areaStyle: {},
            data: innorowreaded
          },
          {
            name: '平均每秒从InnoDB表更新的行数',
            type: 'line',
            areaStyle: {},
            data: innorowupdate
          },
          {
            name: '平均每秒从InnoDB表删除的行数',
            type: 'line',
            areaStyle: {},
            data: innorowdelete
          },
          {
            name: '平均每秒从InnoDB表插入的行数',
            type: 'line',
            areaStyle: {},
            data: innorowinsert
          },
          {
            name: '平均每秒向日志文件的物理写次数',
            type: 'line',
            areaStyle: {},
            data: Innologwrites
          }
        ]
        stackChart(this, xdata, sdata, 'rowdml', ldata)
        this.graphSpin.rowdml = false
      }).catch(err => {
        sendNotice('error', err)
      })
    }
  },
  mounted () {
    console.log(this.graphSignal)
  }
}
</script>
<style scoped>
.divider-text {
  color: #909399;
  font-size: 14px;
}
</style>
