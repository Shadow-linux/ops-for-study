<template>
  <div>
    <Alert show-icon closable>数据源: <a href="http://kibana.aiyuangong.com" target="_blank">http://kibana.aiyuangong.com </a> , es index: plog-callchain*</Alert>
    <Card style="margin-bottom: 10px" v-show="showCreateTab">
      <Spin size="large" fix v-if="createTabSpin"></Spin>
      <p slot="title">添加策略</p>
      <Form ref="dataForm" :model="dataForm" :rules="ruleDataForm" inline>
        <Row>
          <Col span="24">
            <FormItem prop="alarm_name">
              <Input v-model.trim="dataForm.alarm_name" style="width: 200px" placeholder="监控名"></Input>
            </FormItem>
            <FormItem prop="where_condition">
              <Input
                v-model.trim="dataForm.where_condition"
                style="width: 500px"
                placeholder='API 匹配条件 {"http_host": "www.tokenworld.pro"}'>
              </Input>
            </FormItem>
            <FormItem >
              <InputNumber
                v-model="dataForm.latest_time"
                style="width: 100px"
                :formatter="value => `最近 ${value} 分钟`"
                placeholder="最近几分钟">
                </InputNumber>
            </FormItem>
            <Tooltip  max-width="400" placement="bottom"  >
              <Icon type="ios-alert-outline" style="font-size: 20px;color: #2d8cf0; cursor: pointer"/>
              <div slot="content">
                  <p>可匹配字段:</p>
                  <p>server,requestsize,sessionid,responsesize,cspanid,requestid</p>
                  <p>envtype,pspanid,responsecode,cost,logname,requestip,url,</p>
                  <p>success, loglevel, appid</p>
                  <p>以上字段均为string，匹配字段不存在请联系管理员</p>
              </div>
            </Tooltip>
          </Col>
        </Row>
        <Row>
          <Col span="24">
            <FormItem>
              <Select v-model="dataForm.alarm_strategy" style="width:200px" placeholder="策略">
                <Option v-for="item in strategyList" :value="item.strategy" :key="item.strategy">{{ item.comment }}</Option>
              </Select>
            </FormItem>
            <FormItem><b>IF</b></FormItem>
            <FormItem>
              <Select v-model="dataForm.op" style="width:70px" placeholder="比较符">
                <Option v-for="item in opList" :value="item" :key="item">{{ item }}</Option>
              </Select>
            </FormItem>
            <FormItem>
              <Input-number v-model="dataForm.cost"
                style="width: 100px"
                placeholder="告警值"
                :formatter="value => `${value} ms`"></Input-number>
            </FormItem>
            <FormItem v-show="dataForm.alarm_strategy === 'cost_percent'">
              <InputNumber v-model="dataForm.strategy_external.percent"
                :max="100"
                :min="1"
                style="width: 150px"
                placeholder="百分比(number)"
                :formatter="value => `占比  ${dataForm.op}  ${value}%`"
                >
                  <!-- <span slot="prepend">占比&nbsp;&nbsp;{{ dataForm.op }}</span>
                  <span slot="append">%</span> -->
              </InputNumber>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span="24">
            <FormItem prop="send_user_id">
              <Select v-model="dataForm.send_user_id" style="width:200px" placeholder="发送用户" multiple filterable>
                <Option v-for="item in sendUseIdList" :value="item.id" :key="item.id">{{ item.real_name }}</Option>
              </Select>
            </FormItem>
            <FormItem>
              <Checkbox v-model="dataForm.is_mail">邮件</Checkbox>
              <Checkbox v-model="dataForm.is_message" disabled>短信</Checkbox>
              <Checkbox v-model="dataForm.is_wechat" disabled>微信</Checkbox>
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Button type="default" style="margin-right: 10px" @click="() => { showCreateTab = false }">关闭</Button>
          <Button type="primary" ghost @click="saveStrategy"><Icons type="save" :size="10" color="#2d8cf0"/> 保存</Button>
        </Row>
      </Form>
    </Card>
    <Card>
      <p slot="title">策略表</p>
      <Poptip
        confirm
        title="确认删除 ？"
        placement="right-start"
        @on-ok="deleteItem"
        style="margin-bottom: 20px; margin-right: 10px">
        <Button type="default" size="small">删除</Button>
      </Poptip>
      <Button type="primary" size="small" ghost @click="createStrategy">创建策略</Button>
      <Input v-model.trim="searchVal" placeholder="匹配条件" @on-keyup.enter="search" search style="width: 200px; float: right"></Input>
      <Dropdown style="margin-right: 10px; float: right" trigger="click" @on-click="patchAlarmOnOff">
        <Button type="primary" ghost>
          批量开关
          <Icon type="ios-arrow-down"></Icon>
        </Button>
        <DropdownMenu slot="list">
            <DropdownItem name="on">开</DropdownItem>
            <DropdownItem name="off">关</DropdownItem>
        </DropdownMenu>
      </Dropdown>
      <Table :loading="tableLoading" @on-selection-change="selectChange" :columns="tableColumns" :data="tableDatas"></Table>
    </Card>
    <Modal
      v-model="alarmPersonModal"
      title="修改发送人"
      @on-ok="modifySendUser"
      >
      <Form>
        <FormItem label="发送人: ">
          <Select v-model="mSendUserIdList" style="width:300px" placeholder="发送用户" multiple filterable>
            <Option v-for="item in sendUseIdList" :value="item.id" :key="item.id">{{ item.real_name }}</Option>
          </Select>
        </FormItem>
      </Form>
    </Modal>
  </div>
</template>
<script>
import Icons from '_c/icons'
import { sendNotice } from '@/libs/util.js'
import {
  getUsersList,
  getAccessAlarmStrategy,
  createAccessAlarmStrategy,
  updateAccessAlarmStrategy,
  deleteAccessAlarmStrategy
} from '@/api/monitor/business/api_quality.js'

export default {
  name: 'monitor_business_apiQuality',
  components: {
    Icons
  },
  data () {
    const validateJson = (rule, value, callback) => {
      try {
        let valueArr = JSON.parse(value)
        if (typeof valueArr !== 'object') {
          callback(new Error('请输入 JSON 格式, 如 {"appid": "dlvopenapi", "url": "/dlvopenapi/apixxx"}'))
        }
        callback()
      } catch (err) {
        callback(new Error('请输入 JSON 格式, 如 {"appid": "dlvopenapi", "url": "/dlvopenapi/apixxx"}'))
      }
    }
    return {
      mSendUserId: [],
      mSendUserIdList: [],
      alarmPersonModal: false,
      selectValues: [],
      searchVal: '',
      createTabSpin: false,
      showCreateTab: false,
      tableColumns: [
        {
          type: 'selection',
          width: 50,
          align: 'left'
        },
        {
          'title': 'Ops Id',
          'key': 'work_order',
          'sortable': true,
          'sortType': 'desc',
          'width': 130
        },
        {
          'title': '监控名',
          'key': 'alarm_name'
        },
        {
          'title': '匹配条件',
          'key': 'where_condition'
        },
        {
          'title': '策略',
          'width': 180,
          render: (h, params) => {
            let alarm_strategy = JSON.parse(params.row.alarm_strategy)
            let strategy = alarm_strategy['strategy']
            let op = params.row.op
            let cost = params.row.cost
            switch (strategy) {
              case 'cost_percent':
                let percent = alarm_strategy['percent']
                return h('span', {}, [
                  h('p', {}, `[${strategy}]`),
                  h('p', {}, `if ${op} ${cost}; 占比 ${op} ${percent * 100}% `)
                ])
              default:
                return h('span', {}, [
                  h('p', {}, `[${strategy}]`),
                  h('p', {}, `if ${op} ${cost};`)
                ])
            }
          }
        },
        {
          'title': '最近',
          'key': 'latest_time',
          'width': 80,
          'align': 'center',
          render: (h, params) => {
            return h('span', {}, `${params.row.latest_time} 分钟`)
          }
        },
        {
          'title': '发送人',
          render: (h, params) => {
            let userIdArr = JSON.parse(params.row.send_user_id)
            let renderSendUser = []
            this.sendUseIdList.forEach(item => {
              if (userIdArr.indexOf(item.id) !== -1) {
                renderSendUser.push(
                  h('p', {}, item.real_name)
                )
              }
            })
            return h('div', {}, renderSendUser)
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
          'title': '操作 | 告警',
          'align': 'center',
          'width': 120,
          render: (h, params) => {
            return h('div', {}, [
              h('a', {
                'on': {
                  'click': () => {
                    this.alarmPersonModal = true
                    this.mSendUserId = params.row.id
                    this.mSendUserIdList = JSON.parse(params.row.send_user_id)
                  }
                },
                'style': {
                  'margin-right': '10px'
                }
              }, '发送人'),
              h('i-switch', {
                props: {
                  'value': params.row.is_alarm,
                  'size': 'small'
                },
                on: {
                  'on-change': (status) => {
                    let commitStatus = status ? 1 : 0
                    updateAccessAlarmStrategy(params.row.id, { 'is_alarm': commitStatus }).then(res => {
                      this.$Message.success('On/Off 告警')
                    }).catch(err => {
                      sendNotice('error', err)
                    })
                  }
                }
              })
            ])
          }
        }
      ],
      tableLoading: false,
      tableDatas: [],
      originTableDatas: [],
      sendUseIdList: [],
      opList: ['>', '>=', '==', '<=', '<'],
      strategyList: [
        {
          'strategy': 'average',
          'comment': '平均值 (average)'
        },
        {
          'strategy': 'max',
          'comment': '最大值 (max)'
        },
        {
          'strategy': 'cost_percent',
          'comment': '花费占比 (cost_percent)'
        }
      ],
      strategyExternal: {
        percent: 0
      },
      dataForm: {
        alarm_name: '',
        where_condition: '',
        alarm_strategy: 'average',
        latest_time: 1,
        is_mail: false,
        is_message: false,
        is_wechat: false,
        op: '>',
        cost: 1000,
        is_alarm: 1,
        send_user_id: [],
        strategy_external: {
          percent: 50
        }
      },
      initDataForm: {
        alarm_name: '',
        where_condition: '',
        alarm_strategy: 'average',
        latest_time: 1,
        is_mail: false,
        is_message: false,
        is_wechat: false,
        op: '>',
        cost: 1000,
        is_alarm: 1,
        send_user_id: [],
        strategy_external: {
          percent: 50
        }
      },
      ruleDataForm: {
        alarm_name: [
          { required: true, message: '不能为空', trigger: 'blur' }
        ],
        where_condition: [
          { required: true, validator: validateJson, trigger: 'blur' }
        ],
        send_user_id: [
          { required: true, type: 'array', message: '不能为空', trigger: 'change' }
        ]
      }
    }
  },
  methods: {
    search () {
      if (!this.searchVal) {
        this.tableDatas = this.originTableDatas
        return
      }
      this.tableDatas = this.originTableDatas.filter(item => {
        if (item.where_condition.indexOf(this.searchVal) !== -1) {
          return item
        }
      })
    },
    reloadTable () {
      this.tableLoading = true
      getAccessAlarmStrategy().then(res => {
        this.tableDatas = this.originTableDatas = res.data
        console.log(this.tableDatas)
        this.tableLoading = false
      }).catch(err => {
        sendNotice('error', err)
        this.tableLoading = false
      })
    },
    selectChange (value) {
      this.selectValues = value
    },
    deleteItem () {
      this.selectValues.forEach(item => {
        deleteAccessAlarmStrategy(item.id).then(res => {
          this.$Message.success('删除成功')
          this.reloadTable()
        }).catch(err => {
          sendNotice('error', err)
        })
      })
    },
    modifySendUser () {
      updateAccessAlarmStrategy(this.mSendUserId, { 'send_user_id': JSON.stringify(this.mSendUserIdList) }).then(res => {
        this.$Message.success('操作成功')
        this.reloadTable()
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    createStrategy () {
      this.showCreateTab = true
    },
    patchAlarmOnOff (value) {
      let commitStatus = value === 'on' ? 1 : 0
      this.originTableDatas.forEach(item => {
        updateAccessAlarmStrategy(item.id, { 'is_alarm': commitStatus }).then(res => {
          this.$Message.success('On/Off 告警')
        }).catch(err => {
          sendNotice('error', err)
        })
      })
      setTimeout(() => { this.reloadTable() }, 2000)
    },
    saveStrategy () {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          this.createTabSpin = true
          let alarmStrategy
          let strategy = this.dataForm.alarm_strategy
          switch (strategy) {
            case 'cost_percent':
              alarmStrategy = `{"strategy": "${strategy}", "percent": ${this.dataForm.strategy_external.percent / 100}}`
              break
            default:
              alarmStrategy = `{"strategy": "${strategy}"}`
              break
          }
          let commitForm = {
            alarm_name: this.dataForm.alarm_name,
            where_condition: this.dataForm.where_condition,
            alarm_strategy: alarmStrategy,
            latest_time: this.dataForm.latest_time,
            is_mail: this.dataForm.is_mail ? 1 : 0,
            is_message: this.dataForm.is_message ? 1 : 0,
            is_wechat: this.dataForm.is_wechat ? 1 : 0,
            op: '>',
            cost: this.dataForm.cost,
            is_alarm: 1,
            send_user_id: JSON.stringify(this.dataForm.send_user_id)
          }
          console.log(commitForm)
          createAccessAlarmStrategy(commitForm).then(res => {
            this.$Message.success('创建成功')
            this.reloadTable()
            this.showCreateTab = false
            this.createTabSpin = false
          }).catch(err => {
            sendNotice('error', err)
            this.createTabSpin = false
          })
        } else {
          this.$Message.error('信息不完整')
        }
      })
    }
  },
  mounted () {
    getUsersList().then(res => {
      this.sendUseIdList = res.data
    }).catch(err => {
      sendNotice('error', err)
    })
    this.reloadTable()
  }
}
</script>
