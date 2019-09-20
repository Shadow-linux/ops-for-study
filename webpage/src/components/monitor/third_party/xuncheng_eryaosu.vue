<template>
  <div>
    <Row style="margin-bottom: 10px">
      <Col span="3">
        <Poptip
          confirm
          title="确认删除 ？"
          placement="top-start"
          @on-ok="deleteItem">
          <Button type="default" size="small">删除</Button>
        </Poptip>
        <span style="margin-left: 5px; font-size: 12px"> 总数: {{ totalItem }}</span>
      </Col>
      <Col span="5" offset="16">
        <Input  v-model.trim="searchVal" :placeholder="searchColumn" search @on-keyup.enter="search"></Input>
      </Col>
    </Row>
    <Table :row-class-name="rowClassName" @on-selection-change="selectChange" :columns="tableColumns" :data="tableDatas"></Table>
    <Modal
        v-model="chartModal"
        :title="`${chartTitle} 余量`"
        width="800">
        <div style="margin-left: 30px">
          天数: &nbsp;&nbsp;
          <Select v-model="chartDays" style="width:150px" @on-change="chartDaysChange">
            <Option value="7">7 days</Option>
            <Option value="30">30 days</Option>
            <Option value="90">90 days</Option>
          </Select>
        </div>
        <div ref="monitorChart" style="height: 300px; width: 100%"></div>
    </Modal>
  </div>
</template>
<script>
// 在复制到新的监控项目时需要修改，在其上面标注了 @modify, 其余基本无需修改直接复制即可
// @modify
import { getXunchengEryaosuInfo, deleteXunchengEryaosuInfo, updateXunchengEryaosuInfoMonitor, getTPChartData } from '@/api/monitor/third_party'
import { sendNotice, lineChart } from '@/libs/util.js'
import { getDate } from '@/libs/tools.js'

export default {
  // @modify
  name: 'tp_xuncheng_eryaosu',
  props: [
    'selectItem'
  ],
  computed: {
    totalItem () {
      return this.originTableDatas.length
    }
  },
  data () {
    return {
      // @modify
      searchColumn: 'key',
      // @modify
      monitorItem: 'xuncheng_eryaosu',
      chartModal: false,
      chartTitle: 'none',
      chartId: 0,
      chartDays: 7,
      searchVal: '',
      selectValues: [],
      originTableDatas: [],
      tableDatas: [],
      // @modify
      tableColumns: [
        {
          type: 'selection',
          width: 50,
          align: 'center'
        },
        {
          'title': '描述',
          'key': 'name_desc'
        },
        {
          'title': '余量',
          'key': 'compare_num',
          'sortable': true,
          'sortType': 'asc'
        },
        {
          'title': 'Key',
          'key': 'key',
          'width': 250
        },
        {
          'title': 'Ops Id',
          'key': 'work_order',
          'width': 250
        },
        {
          'title': '更新时间',
          'key': 'updated',
          'align': 'center'
        },
        {
          'title': '图表',
          'width': 90,
          'align': 'center',
          render: (h, params) => {
            return h('Icon', {
              'props': {
                'type': 'ios-stats'
              },
              'style': {
                'color': '#409EFF',
                'font-size': '20px',
                'cursor': 'pointer'
              },
              'on': {
                click: () => {
                  this.chartModal = true
                  this.chartId = params.row.id
                  this.chartTitle = params.row[this.searchColumn]
                  this.chartDaysChange()
                }
              }
            })
          }
        },
        {
          'title': '监控',
          'align': 'center',
          'width': 100,
          render: (h, params) => {
            let id = params.row.id
            let isMonitor = params.row.is_monitor
            return h('i-switch', {
              props: {
                'value': isMonitor
              },
              on: {
                'on-change': (status) => {
                  let isMonitorNum = status ? 1 : 0
                  updateXunchengEryaosuInfoMonitor(id, isMonitorNum).then(res => {
                    this.$Message.success('操作成功')
                  }).catch(err => {
                    sendNotice('error', err)
                  })
                }
              }
            })
          }
        }
      ]
    }
  },
  methods: {
    // 删除item
    deleteItem () {
      this.selectValues.forEach(item => {
        deleteXunchengEryaosuInfo(item.id).then(res => {
          this.$Message.success('删除成功')
          this.tableDatas = this.originTableDatas.filter(oitem => {
            if (oitem.id !== item.id) {
              return item
            }
          })
        }).catch(err => {
          sendNotice('error', err)
        })
      })
    },
    // 选中的items
    selectChange (value) {
      this.selectValues = value
    },
    // 获取table datas
    getTableDatas () {
      getXunchengEryaosuInfo().then(res => {
        this.originTableDatas = res.data
        this.tableDatas = this.originTableDatas
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    // 查询
    search () {
      if (this.searchVal === '') {
        this.tableDatas = this.originTableDatas
        return
      }
      this.tableDatas = this.originTableDatas.filter(item => {
        if (item[this.searchColumn].indexOf(this.searchVal) !== -1) {
          return item
        }
      })
    },
    rowClassName (row, index) {
      let current_alarm = row.current_alarm
      console.log(current_alarm)
      if (current_alarm) {
        return 'demo-table-error-row'
      }
      return ''
    },
    // 图表数据
    chartDaysChange () {
      getTPChartData(this.chartId, this.monitorItem, parseInt(this.chartDays)).then(res => {
        let data = res.data
        let _sdatas = []
        let xdatas = data.map(item => {
          _sdatas.push(item.value)
          return getDate(item.timestamp, 'year')
        })
        let sdatas = {
          'type': 'line',
          'name': 'balance',
          'data': _sdatas
        }
        lineChart(this, xdatas, sdatas, 'monitorChart', 'balance')
      }).catch(err => {
        sendNotice('error', err)
      })
    }
  },
  mounted () {
    if (this.selectItem === this.monitorItem) {
      this.getTableDatas()
    }
  }
}
</script>
<style>
.ivu-table .demo-table-error-row td{
  background-color: #fde2e2;
  color: #565e71;
}
</style>
