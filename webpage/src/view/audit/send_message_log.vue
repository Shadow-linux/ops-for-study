<template>
  <div>
    <Alert show-icon closable>发送消息日志，保留30天。</Alert>
    <Card>
      <p slot="title">
        消息日志
        <a><Icon type="md-refresh" style="font-size: 20px; float: right;" /></a>
      </p>
      <Tabs v-model="currentTab">
        <TabPane label="邮件" name="mail">
          <Row>
            <Col span="5">
              <Input v-model.trim="searchEmailVal" placeholder="Ops Id" @on-keyup.enter="searchEmail" search style="width: 300px"></Input>
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
              @on-page-size-change="pageSizeChange"
              style=""/>
            </Col>
            <Col span="2">
              <Button type="default" v-show="superUser" @click="delete30DaysAgo">删除数据</Button>
            </Col>
          </Row>
          <br>
          <Table :loading="tableLoading" v-show="currentTab === 'mail'" :columns="mailTableColunms" :data="mailTableDatas"></Table>
        </TabPane>
        <TabPane label="短信" name="sms" disabled>
          <Page :total="pageTotal"
          show-sizer show-total
          :page-size="pageSize"
          :page-size-opts="pageSizeOpts"
          @on-change="pageChange"
          @on-page-size-change="pageSizeChange"/>
          <br>
          <Table :loading="tableLoading" v-show="currentTab === 'sms'" :columns="smsTableColumns" :data="smsTableDatas"></Table>
        </TabPane>
        <TabPane  label="微信" name="wechat" disabled>
          <Page :total="pageTotal"
          show-sizer show-total
          :page-size="pageSize"
          :page-size-opts="pageSizeOpts"
          @on-change="pageChange"
          @on-page-size-change="pageSizeChange"/>
          <br>
          <Table :loading="tableLoading" v-show="currentTab === 'wechat'" :columns="wechatTableColumns" :data="wechatTableDatas"></Table>
        </TabPane>
      </Tabs>
    </Card>
  </div>
</template>
<script>
// 后续添加日志时请添加一个watch currentTab 的变化来加载日志
import { messageMailLog, delete30DaysAgo } from '@/api/audit/mail_log.js'
import { sendNotice, isSuperUser } from '@/libs/util.js'

export default {
  name: 'audit_sendMessageLog',
  data () {
    return {
      searchEmailVal: '',
      currentTab: 'mail',
      smsTableColumns: [],
      wechatTableColumns: [],
      mailTableColunms: [
        {
          'title': 'Ops Id',
          'key': 'work_order'
        },
        {
          'title': '标题',
          'key': 'title'
        },
        {
          'title': '内容',
          'key': 'content',
          'tooltip': true,
          'width': 400
        },
        {
          'title': '时间',
          'key': 'created',
          'sortable': true,
          'align': 'center',
          'width': 100
        },
        {
          'title': '接收者',
          'key': 'receiver'
        },
        {
          'title': '状态',
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
      mailTableDatas: [],
      smsTableDatas: [],
      wechatTableDatas: [],
      tableLoading: false,
      pageTotal: 0,
      pageSize: 50,
      pageSizeOpts: [50, 150, 200],
      mailOrginTableDatas: [],
      smsOrginTableDatas: [],
      wechatOrginTableDatas: [],
      // 第一次通过token 分析出，该掌握不为superuser
      superUser: false
    }
  },
  methods: {
    searchEmail () {
      this.tableLoading = true
      if (!this.searchEmailVal) {
        this.mailTableDatas = this.mailOrginTableDatas
        this.tableLoading = false
        return
      }
      this.mailTableDatas = this.mailOrginTableDatas.filter(item => {
        if (item.work_order.indexOf(this.searchEmailVal) !== -1) {
          this.tableLoading = false
          return item
        }
      })
    },
    reloadTables () {
      this.tableLoading = true
      switch (this.currentTab) {
        case 'mail':
          messageMailLog().then(res => {
            this.mailTableDatas = this.mailOrginTableDatas = res.data.reverse()
            console.log(this.mailTableDatas)
            this.pageTotal = this.mailOrginTableDatas.length
            this.tableLoading = false
          }).catch(err => {
            sendNotice('error', err)
            this.tableLoading = false
          })
          break
        default:
          break
      }
    },
    pageSizeChange (pageSize) {
      this.pageSize = pageSize
      this.spliceTableDatas(1)
    },
    pageChange (page) {
      this.spliceTableDatas(page)
    },
    spliceTableDatas (page) {
      switch (this.currentTab) {
        case 'mail':
          this.mailTableDatas = this.mailOrginTableDatas.slice(page * this.pageSize - this.pageSize, page * this.pageSize)
          break
        case 'sms':
          this.smsTableDatas = this.smsOrginTableDatas.slice(page * this.pageSize - this.pageSize, page * this.pageSize)
          break
        case 'wechat':
          this.wechatTableDatas = this.wechatOrginTableDatas.slice(page * this.pageSize - this.pageSize, page * this.pageSize)
          break
      }
    },
    delete30DaysAgo () {
      delete30DaysAgo().then(res => {
        this.$Message.success('操作成功')
        this.reloadTables()
      }).catch(err => {
        sendNotice('error', err)
      })
    }
  },
  mounted () {
    this.reloadTables()
    this.superUser = isSuperUser()
  }
}
</script>
