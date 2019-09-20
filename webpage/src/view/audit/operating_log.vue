<template>
  <div>
    <Alert show-icon closable>全站所有对数据操作的记录均可在此查看，支持单一条件或多条件搜索（30天的操作记录）。</Alert>
    <Card>
      <p slot="title">全局操作记录</p>
      <a @click="reloadTableDatas"  slot="extra">
        <Icon type="md-refresh" style="font-size: 20px; float: right;" />
      </a>
      <Row>
        <Col span="24">
          <Select v-model="queryDataForm.user" style="width:150px; margin-right: 10px" placeholder="用户">
            <Option v-for="item in userList" :value="item.username" :key="item.id">{{ item.username }}</Option>
          </Select>
          <Select v-model="queryDataForm.method" style="width:150px; margin-right: 10px" placeholder="HTTP METHOD">
            <Option v-for="item in methodList" :value="item" :key="item">{{ item }}</Option>
          </Select>
          <DatePicker type="daterange"
           placement="bottom-start"
           placeholder="日期"
           style="width: 200px; margin-right: 10px"
           @on-change="dateChange"></DatePicker>
          <Input v-model="queryDataForm.data" placeholder="模糊搜索‘提交数据’内容" style="width: 200px; margin-right: 20px" />
          <Button type="primary" @click="queryData" ghost>查询</Button>
        </Col>
      </Row>
      <br>
      <Row>
        <Col span="22">
          <Page :total="pageTotal"
          show-sizer show-total
          :page-size="pageSize"
          :page-size-opts="pageSizeOpts"
          @on-change="pageChange"
          @on-page-size-change="pageSizeChange"/>
        </Col>
        <Col span="2">
          <Button type="default" v-show="superUser" @click="delete30DaysAgo">删除数据</Button>
        </Col>
      </Row>
      <br>
      <Table :loading="tableLoading" :columns="tableColumns" :data="tableDatas"></Table>
    </Card>
  </div>
</template>
<script>

import { getGlobalOperatingLog, getUserList, delete30DaysAgo } from '@/api/audit/operation_log'
import { sendNotice, isSuperUser } from '@/libs/util.js'

export default {
  name: 'audit_operatingLog',
  data () {
    return {
      queryDataForm: {
        user: '',
        method: '',
        select_date: '',
        data: ''
      },
      tableLoading: false,
      pageTotal: 0,
      pageSize: 50,
      pageSizeOpts: [50, 150, 200],
      orginTableDatas: [],
      userList: [],
      methodList: [ 'POST', 'PUT', 'PATCH', 'DELETE' ],
      tableColumns: [
        {
          title: '用户',
          key: 'user',
          width: 150
        },
        {
          title: '时间',
          key: 'time',
          width: 100,
          align: 'center'
        },
        {
          title: 'HTTP方法',
          key: 'method',
          width: 100,
          align: 'center',
          render: (h, params) => {
            // console.log(params.row)
            var method = params.row.method
            if (method === 'POST') {
              return h('Tag', {
                props: {
                  color: 'green'
                }
              }, 'POST')
            }
            if (method === 'PUT' || method === 'PATCH') {
              return h('Tag', {
                props: {
                  color: 'blue'
                }
              }, 'PUT')
            }
            if (method === 'DELETE') {
              return h('Tag', {
                props: {
                  color: 'red'
                }
              }, 'DELETE')
            }
          }
        },
        {
          title: '描述',
          key: 'description',
          width: 200
        },
        {
          title: 'URI',
          key: 'uri',
          width: 200
        },
        {
          title: '提交数据',
          key: 'data'
        },
        {
          title: '是否成功',
          key: 'is_succeed',
          width: 100,
          align: 'center',
          render: (h, params) => {
            var check = params.row.is_succeed
            if (check) {
              return h('Icon', {
                props: {
                  type: 'md-checkmark-circle-outline'
                },
                style: {
                  'color': '#67C23A',
                  'font-size': '20px'
                }
              })
            }
            return h('Icon', {
              props: {
                type: 'ios-close-circle-outline'
              },
              style: {
                'color': '#ed4014',
                'font-size': '20px'
              }
            })
          }
        }
      ],
      tableDatas: [],
      superUser: false
    }
  },
  methods: {
    pageSizeChange (pageSize) {
      this.pageSize = pageSize
      this.spliceTableDatas(1)
    },
    pageChange (page) {
      this.spliceTableDatas(page)
    },
    spliceTableDatas (page) {
      this.tableDatas = this.orginTableDatas.slice(page * this.pageSize - this.pageSize, page * this.pageSize)
    },
    queryData () {
      var queryForm = {}
      for (var key in this.queryDataForm) {
        if (this.queryDataForm[key]) {
          queryForm[key] = this.queryDataForm[key]
        }
      }
      console.log(queryForm)
      getGlobalOperatingLog(queryForm).then(res => {
        this.orginTableDatas = res.data.reverse()
        this.pageTotal = this.orginTableDatas.length
        this.spliceTableDatas(1)
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    dateChange (value) {
      if (value[0].length === 0) {
        this.queryDataForm.select_date = ''
        return
      }
      this.queryDataForm.select_date = value.join()
    },
    reloadTableDatas () {
      this.tableLoading = true
      getGlobalOperatingLog().then(res => {
        this.orginTableDatas = res.data.reverse()
        this.pageTotal = this.orginTableDatas.length
        this.spliceTableDatas(1)
        this.tableLoading = false
      }).catch(err => {
        sendNotice('error', err)
        this.tableLoading = false
      })
    },
    delete30DaysAgo () {
      delete30DaysAgo().then(res => {
        this.$Message.success('操作成功')
        this.reloadTableDatas()
      }).catch(err => {
        sendNotice('error', err)
      })
    }
  },
  mounted () {
    this.reloadTableDatas()
    getUserList().then(res => {
      this.userList = res.data
    }).catch(err => {
      sendNotice('error', err)
    })
    this.superUser = isSuperUser()
  }
}
</script>
<style  scoped>
</style>
