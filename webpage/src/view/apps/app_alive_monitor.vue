<template>
  <div>
    <Alert show-icon>需要监控存活的 APP, 在APP管理中选择"监控（是）"，并且填写对应的监控地址。</Alert>
    <Row :gutter="-10">
      <Col span="5">
        <Menu  :active-name="envActive" @on-select="selectEnv" class="container" width="210">
          <MenuGroup title="环境选择">
              <MenuItem :name="env" v-for="env in envList" :key="env">
                <Icon type="ios-bookmark" />
                {{ env }}
              </MenuItem>
          </MenuGroup>
        </Menu>
      </Col>
      <Col span="19">
        <Card class="container" >
          <p slot="title" style="height: 18px">
            {{ envActive }}
            <span style="margin-left: 20px">
              <span style="color: #67C23A; margin-right: 5px">{{ tacticsData.success }}</span>
              <span style="color: #F56C6C; margin-right: 5px">{{ tacticsData.failed }}</span>
              <span style="color: #909399; margin-right: 5px">{{ tacticsData.unreachable }}</span>
            </span>
            <a style="float: right; font-size: 12px" @click="refreshPage">刷新</a>
          </p>
          <span style="font-size: 12px; margin-right: 5px">告警(统一开关): </span>
          <Button type="default" size="small" style="margin-right: 10px" @click="alarmSwitch(1)">开</Button>
          <Button type="default" size="small" @click="alarmSwitch(0)">关</Button>
          <br><br>
          <Table @on-sort-change="tableSort" :loading="tableLoading" :columns="tableColunm" :data="tableData"></Table>
        </Card>
      </Col>
    </Row>
    <Modal
      v-model="monitorModal"
      title="APP Alive 监控图"
      width="760"
      >
      <Alert type="warning" show-icon>0: 正常, 1: 异常, 2: 不可达</Alert>
      <div ref="appAliveChart" style="height: 300px; width: 100%"></div>
    </Modal>
  </div>
</template>
<script>

import {
  getCmdbSetting,
  getAppDetailList,
  getAppAliveData,
  updateAppAliveAlarm,
  getAppAliveGraph,
  tacticsAppAlive } from '@/api/apps/app_alive_monitor'
import { sendNotice } from '@/libs/util.js'
import { getDate } from '@/libs/tools.js'
import echarts from 'echarts'

export default {
  name: 'app_aliveMonitor',
  watch: {
    envActive (newVal, oldVal) {
      this.genCheckAliveList()
    }
  },
  data () {
    return {
      tableLoading: false,
      monitorModal: false,
      tacticsData: {
        'success': 0,
        'failed': 0,
        'unreachable': 0
      },
      originTableData: [],
      envActive: '',
      envList: [],
      tableColunm: [
        {
          'title': 'App 名称',
          'key': 'app_name',
          'width': 150,
          'sortable': true,
          render: (h, params) => {
            return h('a', {
              on: {
                click: () => {
                  let id = params.row.app_id
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
          'title': '状态',
          'key': 'alive_data',
          'width': 100,
          'sortable': 'custom',
          'sortType': 'desc',
          render: (h, params) => {
            let status = params.row.alive_data.value
            let color = '#909399'
            let _type = 'ios-remove-circle-outline'
            switch (status) {
              case 0:
                color = '#67C23A'
                _type = 'md-checkmark-circle-outline'
                break
              case 1:
                color = '#F56C6C'
                _type = 'ios-close-circle-outline'
                break
            }
            return h('Icon', {
              'props': {
                type: _type
              },
              'style': {
                color: color,
                'font-size': '20px'
              }
            })
          }
        },
        {
          'title': 'API',
          'key': 'check_api',
          'width': 250
        },
        {
          'title': '更新时间',
          'key': 'update_time',
          'align': 'center',
          render: (h, params) => {
            let timestamp = params.row.alive_data.timestamp
            let time = getDate(timestamp, 'year')
            return h('p', {}, time)
          },
          width: 150
        },
        {
          'title': '监控',
          'key': 'monitor',
          'width': 100,
          'align': 'center',
          render: (h, params) => {
            return h('a', {}, [
              h('Icon', {
                'props': {
                  'type': 'ios-stats'
                },
                'style': {
                  'font-size': '20px'
                },
                on: {
                  click: () => {
                    this.monitorModal = true
                    let appid = params.row.app_id
                    let env = params.row.env
                    let checkapi = params.row.check_api
                    getAppAliveGraph(appid, env, checkapi).then(res => {
                      let data = res.data[0]
                      let _sdatas = []
                      let xdatas = data.values.map(item => {
                        _sdatas.push(item.value)
                        return getDate(item.timestamp, 'year')
                      })
                      let sdatas = {
                        'type': 'line',
                        'name': 'app_alive',
                        'data': _sdatas
                      }
                      this.singleLineChart(xdatas, sdatas, 'appAliveChart', 'app_alive')
                    }).catch(err => {
                      sendNotice('error', err)
                    })
                  }
                }
              })
            ])
          }
        },
        {
          'title': '告警',
          'key': 'is_alarm',
          'align': 'center',
          render: (h, params) => {
            let isAlarm
            if (params.row.is_alarm === 1) {
              isAlarm = true
            } else {
              isAlarm = false
            }
            return h('i-switch', {
              props: {
                'value': isAlarm
              },
              on: {
                'on-change': (status) => {
                  let data = {
                    app_id: params.row.app_id,
                    env: params.row.env,
                    is_alarm: status ? 1 : 0,
                    check_api: params.row.check_api
                  }
                  updateAppAliveAlarm(data).then(res => {
                    this.$Message.success('操作成功')
                  }).catch(err => {
                    sendNotice('error', err)
                  })
                }
              }
            })
          }
        }
      ],
      'tableData': [],
      'checkAliveList': []
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
    selectEnv (name) {
      this.envActive = name
    },
    getAppList () {
      getAppDetailList().then(res => {
        this.originTableData = res.data.filter(item => {
          if (item.is_monitor) {
            return item
          }
        })
        this.envActive = this.envList[0]
        // this.genCheckAliveList()
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    refreshPage () {
      getAppDetailList().then(res => {
        this.originTableData = res.data.filter(item => {
          if (item.is_monitor) {
            return item
          }
        })
        this.genCheckAliveList()
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    genCheckAliveList () {
      this.tableLoading = true
      // 清空
      this.checkAliveList = []
      // 数据格式 [{ "app_id": 1000, "env": "undefined", "check_api": "http://10.81.126.19:8009/info" }]
      for (let idx in this.originTableData) {
        let item = this.originTableData[idx]
        if (this.envActive === 'external' && item.external_check_api) {
          this.checkAliveList.push({
            'app_name': item.app_name,
            'app_id': item.id,
            'env': this.envActive,
            'is_alarm': item.is_alarm,
            'check_api': item.external_check_api
          })
        } else {
          let envCheckApiList = item.host_list[this.envActive]
          // console.log(envCheckApiList)
          for (let idx2 in envCheckApiList) {
            let data = envCheckApiList[idx2]
            // 没有该环境的检查地址则跳过
            if (!data.internal_check_api) {
              continue
            }
            this.checkAliveList.push({
              'app_name': item.app_name,
              'app_id': item.id,
              'env': this.envActive,
              'is_alarm': item.is_alarm,
              'check_api': data.internal_check_api
            })
          }
        }
        // console.log(this.checkAliveList)
      }
      // 最终展示数据
      let data = JSON.stringify(this.checkAliveList)
      /**  [{ "app_id": 1000,
       *  "env": "undefined",
       *  "check_api": "http://10.81.126.19:8009/info",
       *  "is_alarm": 1,
       *  "app_name": "app"
       *  }] */
      getAppAliveData(data).then(res => {
        this.tableData = res.data
        // console.log(this.tableData)
        this.tableSort({ 'key': 'alive_data', 'order': 'desc' })
        this.tableLoading = false
      }).catch(err => {
        sendNotice('error', err)
        this.tableLoading = false
      })
      // 统计信息
      tacticsAppAlive(data).then(res => {
        this.tacticsData = res.data
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    alarmSwitch (isAlarm) {
      for (let idx in this.tableData) {
        let item = this.tableData[idx]
        let data = {
          app_id: item.app_id,
          env: item.env,
          is_alarm: isAlarm,
          check_api: item.check_api
        }
        updateAppAliveAlarm(data).then(res => {
          this.$Message.success('操作成功')
        }).catch(err => {
          sendNotice('error', err)
        })
      }
      this.refreshPage()
    },
    tableSort (obj) {
      if (obj.key === 'alive_data') {
        let s2List = []
        let s1List = []
        let s0LIst = []
        this.tableData.forEach(item => {
          switch (item.alive_data.value) {
            case 0:
              s0LIst.push(item)
              break
            case 1:
              s1List.push(item)
              break
            default:
              s2List.push(item)
              break
          }
        })
        if (obj.order === 'desc') {
          this.tableData = s2List.concat(s1List, s0LIst)
        } else {
          this.tableData = s0LIst.concat(s1List, s2List)
        }
      }
    }
  },
  created () {
    // 获取evn list
    getCmdbSetting().then(res => {
      this.envList = res.data[0]['cmdb_setting']['base']['env']
      this.envList = this.envList.filter(item => {
        if (item !== 'undefined') {
          return item
        }
      })
    }).catch(err => {
      sendNotice('error', err)
    })
    this.getAppList()
  },
  mounted () {
  }
}
</script>
<style>
.container {
  height: calc(100vh - 110px);
  padding-top: 0;
  overflow: auto;
}
</style>
