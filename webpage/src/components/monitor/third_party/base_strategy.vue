<template>
  <div>
    <Row>
      <Col span="4">
        <Input v-model="searchVal" placeholder="查询策略名称" @on-keyup.enter="search" search style=""></Input>
      </Col>
      <Col span="2" offset="18">
        <Button type="primary" ghost @click="createModal" style="float: right">创建策略</Button>
      </Col>
    </Row>
    <br>
    <div style="margin-bottom: 10px">
      <Poptip
        confirm
        title="确认删除 ？"
        placement="right-start"
        @on-ok="deleteItem">
        <Button type="default" size="small">删除</Button>
      </Poptip>
      <span style="margin-left: 5px; font-size: 12px"> 总数: {{ totalItem }}</span>
      <Button type="default" size="small" @click="getTableDatas()" style="float: right"><Icon type="md-refresh" style="font-size: 20px"/></Button>
    </div>
    <Table :columns="tableColumns" @on-selection-change="selectChange" :loading="tableLoading" :data="tableDatas"></Table>
    <Modal
      v-model="strategyModal"
      :title="`${modalTitle}策略`"
      :mask-closable="false"
      @on-ok="modalOk"
      >
      <Form :model="dataForm" :rules="ruleDataForm" :label-width="110" >
        <FormItem label="监控项目:" prop="monitor_item">
          <Select v-model="dataForm.monitor_item" style="width: 100%" filterable>
            <Option v-for="item in strategyItemList" :value="item" :key="item">{{ item }} {{ monitorItemList[item] }}</Option>
          </Select>
        </FormItem>
        <FormItem label="策略:">
          <Select v-model="dataForm.op" style="width:60px; margin-right: 3%">
            <Option v-for="item in opList" :value="item" :key="item">{{ item }}</Option>
          </Select>
          <InputNumber v-model="dataForm.alert_number" ></InputNumber>
        </FormItem>
        <FormItem label="告警内容 (Note):" prop="note">
          <Input v-model.trim="dataForm.note" ></Input>
        </FormItem>
        <FormItem label="是否告警:">
          <Checkbox v-model="dataForm.is_alarm">是</Checkbox>
        </FormItem>
        <FormItem label="发送人:" v-show="dataForm.is_alarm">
          <Select v-model="dataForm.send_user_id" style="width: 100%" multiple>
            <Option v-for="item in openUserList" :value="item.id" :key="item.id">{{ item.real_name }}</Option>
          </Select>
        </FormItem>
        <FormItem label="发送方式:" v-show="dataForm.is_alarm">
          <Checkbox v-model="dataForm.is_mail">邮件</Checkbox>
          <Checkbox v-model="dataForm.is_message" disabled>短信</Checkbox>
          <Checkbox v-model="dataForm.is_wechat" disabled>微信</Checkbox>
        </FormItem>
      </Form>
    </Modal>
  </div>
</template>
<script>
import { monitorItemList } from '_c/monitor/third_party/vars.js'
import {
  getTPStrategy,
  getOpenUserList,
  getTPBaseItem,
  createTPStrategy,
  updateTPStrategy,
  deleteTPStrategy
} from '@/api/monitor/third_party.js'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'tp_base_strategy',
  data () {
    return {
      'modalAction': '',
      'searchVal': '',
      'openUserList': [],
      'modalTitle': '添加',
      'strategyModal': false,
      'tableLoading': false,
      'opList': ['>', '>=', '==', '<=', '<'],
      // @modify
      'dataForm': {
        'monitor_item': '',
        'op': '<=',
        'alert_number': 0,
        'note': '',
        'send_user_id': [],
        'is_alarm': true,
        'is_mail': false,
        'is_message': false,
        'is_wechat': false
      },
      // @modify
      'initForm': {
        'monitor_item': '',
        'hours_ago': 1,
        'op': '>=',
        'alert_number': 0,
        'note': '',
        'send_user_id': [],
        'is_alarm': true,
        'is_mail': false,
        'is_message': false,
        'is_wechat': false
      },
      ruleDataForm: {
        monitor_item: [
          { required: true, message: 'The item cannot be empty', trigger: 'change' }
        ],
        note: [
          { required: true, message: 'The item cannot be empty', trigger: 'blur' }
        ]
      },
      'tableColumns': [
        {
          type: 'selection',
          width: 50,
          align: 'center'
        },
        {
          'title': '监控项',
          'key': 'monitor_item',
          'width': 150,
          'sortable': true,
          'sortType': 'asc',
          render: (h, params) => {
            return h('span', {}, `${params.row.monitor_item}`)
          }
        },
        {
          'title': '策略',
          'width': 110,
          render: (h, params) => {
            return h('span', {}, `${params.row.op} ${params.row.alert_number}`)
          }
        },
        {
          'title': 'Note',
          'key': 'note'
        },
        {
          'title': 'Ops Id',
          'key': 'work_order'
        },
        {
          'title': '告警',
          'align': 'center',
          'width': 80,
          render: (h, params) => {
            let status = params.row.is_alarm
            let color = '#909399'
            let _type = 'ios-remove-circle-outline'
            switch (status) {
              case true:
                color = '#67C23A'
                _type = 'md-checkmark-circle-outline'
                break
              case false:
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
          'title': '发送人',
          'width': 150,
          render: (h, params) => {
            let userIds = JSON.parse(params.row.send_user_id)
            let renderUsers = []
            this.openUserList.forEach(item => {
              if (userIds.indexOf(item['id']) > -1) {
                renderUsers.push(
                  h('p', {}, item['real_name'])
                )
              }
            })
            return h('div', {}, renderUsers)
          }
        },
        {
          'title': '发送方式',
          'width': 120,
          render: (h, params) => {
            let sendWay = [params.row.is_mail, params.row.is_message, params.row.is_wechat]
            let sendContent
            if (sendWay[0]) {
              sendContent = ' 邮箱 '
            }
            if (sendWay[1]) {
              sendContent = sendContent + ' 短信 '
            }
            if (sendWay[2]) {
              sendContent = sendContent + ' 微信 '
            }
            return h('span', {}, sendContent)
          }
        },
        {
          'title': '操作',
          'align': 'right',
          'width': 70,
          render: (h, params) => {
            // <Icon type="ios-create" />
            return h('Icon', {
              'props': {
                'type': 'md-open'
              },
              'style': {
                'font-size': '20px',
                'cursor': 'pointer',
                'color': '#2d8cf0'
              },
              'on': {
                click: () => {
                  this.strategyModal = true
                  this.modalTitle = '编辑'
                  this.modalAction = 'update'
                  this.dataForm = params.row
                  this.dataForm.send_user_id = JSON.parse(params.row.send_user_id)
                }
              }
            })
          }
        }
      ],
      'tableDatas': [],
      'originTableDatas': [],
      'totalItem': 0,
      'monitorItemList': monitorItemList,
      'strategyItemList': [],
      'selectValues': []
    }
  },
  methods: {
    getTableDatas () {
      this.tableLoading = true
      getTPStrategy().then(res => {
        this.tableLoading = false
        this.originTableDatas = res.data.reverse()
        this.tableDatas = this.originTableDatas
        this.totalItem = this.originTableDatas.length
      }).catch(err => {
        this.tableLoading = false
        sendNotice('error', err)
      })
    },
    createModal () {
      this.initDataForm()
      this.modalTitle = '创建'
      this.strategyModal = true
      this.modalAction = 'create'
    },
    initDataForm () {
      this.dataForm = this.initForm
    },
    deleteItem () {
      this.selectValues.forEach(item => {
        deleteTPStrategy(item.id).then(res => {
          this.$Message.success('删除成功')
          this.getTableDatas()
        }).catch(err => {
          sendNotice('error', err)
        })
      })
    },
    search () {
      if (this.searchVal === '') {
        this.tableDatas = this.originTableDatas
        return
      }
      this.tableDatas = this.originTableDatas.filter(item => {
        if (item['monitor_item'].indexOf(this.searchVal) !== -1) {
          return item
        }
      })
    },
    handleCommitVal () {
      let commitForm = {
        'monitor_item': this.dataForm.monitor_item,
        'note': this.dataForm.note,
        'op': this.dataForm.op,
        'hours_ago': this.dataForm.hours_ago,
        'alert_number': this.dataForm.alert_number,
        'is_alarm': this.dataForm.is_alarm ? 1 : 0,
        'is_mail': this.dataForm.is_mail ? 1 : 0,
        'is_wechat': this.dataForm.is_wechat ? 1 : 0,
        'is_message': this.dataForm.is_message ? 1 : 0,
        'send_user_id': JSON.stringify(this.dataForm.send_user_id)
      }
      return commitForm
    },
    createAction () {
      let commitForm = this.handleCommitVal()
      createTPStrategy(commitForm).then(res => {
        this.$Message.success('创建成功')
        this.getTableDatas()
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    updateAction () {
      let commitForm = this.handleCommitVal()
      updateTPStrategy(this.dataForm.id, commitForm).then(res => {
        this.$Message.success('更新成功')
        this.getTableDatas()
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    selectChange (items) {
      this.selectValues = items
    },
    modalOk () {
      switch (this.modalAction) {
        case 'create':
          this.createAction()
          break
        case 'update':
          this.updateAction()
          break
        default:
          this.$Message.error('nothing to do...')
      }
    }
  },
  mounted () {
    this.getTableDatas()
    getOpenUserList().then(res => {
      this.openUserList = res.data
    }).catch(err => {
      sendNotice('error', err)
    })
    getTPBaseItem().then(res => {
      this.strategyItemList = res.data
    }).catch(err => {
      sendNotice('error', err)
    })
  }
}
</script>
