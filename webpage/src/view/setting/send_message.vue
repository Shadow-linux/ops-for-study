<template>
  <Row>
    <Alert show-icon closable>根据不同的推送消息方式对用户发送消息、公告等行为。</Alert>
    <Card>
      <p slot="title">消息推送</p>
      <Form ref="messageForm" :model="messageForm" :rules="ruleMessageForm" inline>
        <FormItem prop="title">
          <Input v-model.trim="messageForm.title" placeholder="标题" style="width: 400px"></Input>
        </FormItem>
        <FormItem prop="user_id_list">
          <Select v-model="messageForm.user_id_list" multiple style="width: 250px;" :max-tag-count="3" placeholder="接收用户">
            <Option value="0">全部</Option>
            <Option  v-for="item in userIdList" :value="item.value" :key="item.value">{{ item.label }}</Option>
          </Select>
        </FormItem>
        <FormItem prop="send_type_list">
          <Select v-model="messageForm.send_type_list" multiple style="width: 250px;" :max-tag-count="3" placeholder="发送方式">
            <Option  v-for="item in sendTypeList" :value="item.value" :key="item.value">{{ item.label }}</Option>
          </Select>
        </FormItem>
        <FormItem style="float: right">
          <Button type="primary" @click="sendMessage('messageForm')" ghost>发送</Button>
        </FormItem>
        <br>
        <Editor ref="editor" :value="messageForm.content" @on-change="handleChange"/>
      </Form>
      <br>
      <h3 style="color: #515a6e;margin-bottom: 5px; font-size: 14px">推送记录:
        <Poptip  placement="right" trigger="hover">
          <a style="font-size: 12px; margin-left: 10px">帮助</a>
          <div slot="content">
            发送结果: <br>
            <Icon type="md-information-circle" style="color: #1890ff"/> 等待 <br>
            <Icon type="md-checkmark-circle" style="color: #19be6b"/> 成功 <br>
            <Icon type="md-close-circle" style="color: #ed4014"/> 失败 <br>
          </div>
        </Poptip>
      </h3>
      <br>
      <Row>
        <Col span="19">
          <Page :total="pageTotal"
          show-sizer show-total
          :page-size="pageSize"
          :page-size-opts="pageSizePpts"
          @on-change="pageChange"
          @on-page-size-change="pageSizeChange"
          style="margin-bottom: 10px"
          />
        </Col>
        <Col span="1" offset="4">
          <Button type="primary" size="small" ghost @click="refreshTable">刷新</Button>
        </Col>
      </Row>
      <Table :loading="tableLoading" :columns="tableColums" :data="tableDatas"></Table>
    </Card>
    </Row>
</template>
<script>

import { Editor } from '_c/setting/send_message'
import { getPushMessage, getMessageUserList, createPushMessage } from '@/api/setting/send_message'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'setting_sendMessage',
  components: {
    Editor
  },
  data () {
    return {
      pageTotal: 0,
      pageSize: 10,
      pageSizePpts: [10, 100, 200],
      messageStatus: {},
      tableLoading: false,
      tableDatas: [],
      messageUsers: [],
      ruleMessageForm: {
        title: [
          { required: true, message: '不能为空', trigger: 'blur' }
        ],
        user_id_list: [
          { required: true, message: '不能为空', trigger: 'change', type: 'array' }
        ],
        send_type_list: [
          { required: true, message: '不能为空', trigger: 'change', type: 'array' }
        ]
      },
      tableColums: [
        {
          title: '时间',
          key: 'created'
        },
        {
          title: '标题',
          key: 'title'
        },
        {
          title: '内容',
          key: 'content',
          ellipsis: true,
          tooltip: true,
          width: 200
        },
        {
          title: '发送方式',
          key: 'send_type',
          render: (h, parmas) => {
            var sendList = JSON.parse(parmas.row.send_type_list)
            var renderList = []
            for (var idx in sendList) {
              var workOrder = parmas.row.work_order
              var text = sendList[idx]
              var _color
              var _status
              if (this.messageStatus[workOrder][text] === 0) {
                _status = 'md-alert'
                _color = '#1890ff'
              } else if (this.messageStatus[workOrder][text] === 1) {
                _status = 'md-checkmark-circle'
                _color = '#19be6b'
              } else if (this.messageStatus[workOrder][text] === 2) {
                _status = 'md-close-circle'
                _color = '#ed4014'
              }
              renderList.push(h('p', {}, [
                h('Icon', {
                  props: {
                    type: _status
                  },
                  style: {
                    color: _color,
                    'font-size': '15px'
                  }
                }),
                h('Tag', {
                  props: {
                    color: 'default'
                  },
                  style: {
                    'margin-left': '10px'
                  }
                }, text)
              ]))
            }
            return h('p', {}, renderList)
          }
        },
        {
          title: '接收用户',
          key: 'user',
          ellipsis: true,
          render: (h, parmas) => {
            var renderList = []
            for (var idx in this.messageUsers[parmas.row.work_order]) {
              renderList.push(h('p', {
                style: {
                  color: '#1890ff'
                }
              }, this.messageUsers[parmas.row.work_order][idx]))
            }
            return h('span', {}, renderList)
          }
        }
      ],
      userIdList: [],
      sendTypeList: [
        {
          value: 'inner',
          label: '站内消息'
        },
        {
          value: 'mail',
          label: '邮件消息'
        }
      ],
      messageForm: {
        user_id_list: [],
        send_type_list: [],
        title: '',
        content: ''
      }
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
    sendMessage (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          this.messageForm.send_type_list = JSON.stringify(this.messageForm.send_type_list)
          this.messageForm.user_id_list = JSON.stringify(this.messageForm.user_id_list)
          if (this.messageForm.user_id_list.indexOf('0') > -1) {
            var userIdList = this.userIdList.map(item => {
              return item.value
            })
            this.messageForm.user_id_list = JSON.stringify(userIdList)
          }
          createPushMessage(this.messageForm).then(res => {
            this.$Message.success('消息已经推送了。')
            this.orginTableDatas = []
            this.reloadTable()
          }).catch(err => {
            sendNotice('error', err)
          })
        } else {
          this.$Message.error('推送失败，请检查填写是否正确。')
        }
      })
    },
    handleChange (value) {
      this.messageForm.content = value
    },
    refreshTable () {
      this.$Message.success('刷新表格数据')
      this.reloadTable()
    },
    reloadTable () {
      this.tableLoading = true
      getPushMessage().then(res => {
        this.orginTableDatas = res.data.data.reverse()
        this.pageTotal = this.orginTableDatas.length
        this.spliceTableDatas(1)
        this.messageStatus = res.data.send_types
        this.messageUsers = res.data['usernames']
        this.tableLoading = false
      }).catch(err => {
        sendNotice('error', err)
        this.tableLoading = false
      })
    }
  },
  mounted () {
    this.reloadTable()
    getMessageUserList().then(res => {
      res.data.forEach(item => {
        this.userIdList.push({
          label: item.real_names,
          value: item.id.toString()
        })
      })
    }).catch(err => {
      sendNotice('error', err)
    })
  }
}
</script>
<style scoped>
</style>
