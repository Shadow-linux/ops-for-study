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
  </div>
</template>
<script>
// 在复制到新的监控项目时需要修改，在其上面标注了 @modify, 其余基本无需修改直接复制即可
// @modify
import { getRdsInfo, deleteRdsInfo, updateRdsInfoMonitor } from '@/api/monitor/third_party'
import { sendNotice } from '@/libs/util.js'

export default {
  // @modify
  name: 'tp_rds',
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
      searchColumn: 'instance_id',
      // @modify
      monitorItem: 'rds',
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
          'key': 'instance_desc',
          'width': 250
          // 'tooltip': true
        },
        {
          'title': 'Instance Id',
          'key': 'instance_id'
        },
        {
          'title': '状态',
          'key': 'status',
          'sortable': true,
          'align': 'center',
          'width': 110,
          render: (h, params) => {
            let status = params.row.status
            let color = status === 'Running' ? '#67C23A' : '#F56C6C'
            return h('Tag', {
              'props': {
                'color': color
              }
            }, status)
          }
        },
        {
          'title': '过期时间',
          'key': 'expire_time',
          'sortable': true,
          'sortType': 'asc',
          'align': 'center'
        },
        {
          'title': '更新时间',
          'key': 'updated',
          'align': 'center'
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
                  updateRdsInfoMonitor(id, isMonitorNum).then(res => {
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
        deleteRdsInfo(item.id).then(res => {
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
      getRdsInfo().then(res => {
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
