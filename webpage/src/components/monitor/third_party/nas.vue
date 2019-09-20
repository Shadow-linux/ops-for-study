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
import { getNasInfo, deleteNasInfo, updateNasInfoMonitor } from '@/api/monitor/third_party'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'tp_nas',
  watch: {
    selectItem (nVal, oVal) {
      console.log(nVal)
    }
  },
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
      searchColumn: 'package_id',
      monitorItem: 'nas',
      searchVal: '',
      selectValues: [],
      originTableDatas: [],
      tableDatas: [],
      tableColumns: [
        {
          type: 'selection',
          width: 50,
          align: 'center'
        },
        {
          'title': '描述',
          'key': 'desc',
          'width': 200
          // 'tooltip': true
        },
        {
          'title': 'System Id',
          'key': 'system_id'
        },
        {
          'title': 'Package Id',
          'key': 'package_id',
          'sortable': true
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
                  updateNasInfoMonitor(id, isMonitorNum).then(res => {
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
    deleteItem () {
      this.selectValues.forEach(item => {
        deleteNasInfo(item.id).then(res => {
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
    selectChange (value) {
      this.selectValues = value
    },
    getTableDatas () {
      getNasInfo().then(res => {
        this.originTableDatas = res.data
        this.tableDatas = this.originTableDatas
      }).catch(err => {
        sendNotice('error', err)
      })
    },
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
      console.log(this.selectItem)
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
