<template>
  <div>
    <Card>
      <p slot="title">App 管理</p>
      <div style="margin-bottom: 10px">
        <Button type="primary"  ghost @click="addApp">添加应用</Button>
        <Button style="float: right" @click="() => { reloadTable() }">刷新</Button>
      </div>
      <Row style="height: 50px">
        <Col span="8" style="margin-top: 10px">
          <Poptip
            confirm
            title="确认删除吗 ?"
            placement="right-start"
            @on-ok="deleteOk">
            <Button size="small">删除</Button>
          </Poptip>
          <Button size="small" style="margin-left: 10px" @click="handleBatchControlHost">批量操作关联主机</Button>
          <Button size="small" style="margin-left: 10px" @click="handleBatchControlEnv">批量操作更改监控环境</Button>
        </Col>
        <Col span="6" offset="10">
          <Checkbox v-model="appUsed">使用中</Checkbox>
          <Input search v-model.trim="searchValue" style="width: 78%" @on-keyup.enter="enterSearch" placeholder="搜索App名字"/>
        </Col>
      </Row>
      <span style="font-size: 12px; color: #808695">总数: {{ pageTotal }}</span>
      <!-- <Page :total="pageTotal"  :page-size="pageSize" @on-change="pageChange" size="small" show-total /> -->
      <Table :loading="tableLoading" max-height="1024" @on-selection-change="selectChange" :columns="tableColumns" :data="tableDatas"></Table>
      <br>
    </Card>
    <Modal
      v-model="editModal"
      :title="editModalTitle"
      @on-ok="editOk('dataForm')"
      :mask-closable="false"
      >
      <Alert type="warning" show-icon>✳️号为辅助检查项。</Alert>
      <Form ref="dataForm" :model="dataForm" :rules="ruleDataForm" :label-width=120>
        <FormItem label="应用名:" prop="app_name">
          <Input v-model.trim="dataForm.app_name" />
        </FormItem>
        <FormItem label="应用端口:" prop="port">
          <Input v-model.trim="dataForm.port" />
        </FormItem>
        <FormItem label="描述:" prop="description">
          <Input v-model.trim="dataForm.description" />
        </FormItem>
        <FormItem label="服务:" prop="service">
          <Select filterable v-model="dataForm.service" >
            <Option v-for="item in serviceList" :value="item" :key="item">{{ item }}</Option>
          </Select>
        </FormItem>
        <FormItem label="联系人:" prop="connector">
          <Select filterable multiple v-model="dataForm.connector" >
            <Option v-for="item in usernameList" :value="item.id" :key="item.id">{{ item.username }}</Option>
          </Select>
        </FormItem>
        <FormItem label="关联主机:" prop="hosts">
          <Select filterable multiple v-model="dataForm.hosts" >
            <Option v-for="item in hostsList" :value="`${item.id}:${item.owner}`" :key="`${item.id}:${item.owner}`">
              <Tag style="margin-right: 10px"><b>{{ item.owner }}</b></Tag> {{ item.hostname }}
            </Option>
          </Select>
        </FormItem>
        <FormItem label="使用中:">
          <RadioGroup v-model="dataForm.is_active">
            <Radio label="true">是</Radio>
            <Radio label="false">否</Radio>
          </RadioGroup>
        </FormItem>
        <FormItem label="发布:">
          <RadioGroup v-model="dataForm.is_publish">
            <Radio label="true">是</Radio>
            <Radio label="false">否</Radio>
          </RadioGroup>
        </FormItem>
        <FormItem label="平台启动:">
          <RadioGroup v-model="dataForm.is_launch">
            <Radio label="true">是</Radio>
            <Radio label="false">否</Radio>
          </RadioGroup>
        </FormItem>
        <FormItem label="监控 (App Alive):">
          <RadioGroup v-model="dataForm.is_monitor">
            <Radio label="true">是</Radio>
            <Radio label="false">否</Radio>
          </RadioGroup>
          <span style="color: red">* 需要填写内外部检测信息</span>
        </FormItem>
        <FormItem label="内部API检测:">
          <RadioGroup v-model="dataForm.is_internal_check_api">
            <Radio label="true">是</Radio>
            <Radio label="false">否</Radio>
          </RadioGroup>
        </FormItem>
        <FormItem label="内部检测API Uri:" v-show="dataForm.is_internal_check_api === 'true'" prop="internal_check_api">
          <Input v-model.trim="dataForm.internal_check_api" placeholder="/info"/>
        </FormItem>
        <FormItem label="内部需检测环境:" v-show="dataForm.is_internal_check_api === 'true'" prop="internal_check_api_env">
          <Select filter multiple v-model="dataForm.internal_check_api_env" >
            <Option v-for="item in envList" :value="item" :key="item">
              {{ item }}
            </Option>
          </Select>
        </FormItem>
        <FormItem label="Urlooker Agent" v-show="dataForm.is_internal_check_api === 'true'" prop="chose_agent">
          <Input v-model.trim="dataForm.chose_agent" disabled />
          <p style="color: #2d8cf0; line-height: 15px; margin-top: 5px">* 为不同环境选择不同urlooker agent; 现有 default, internal.agy.gz
            json格式如: {"release": "default", "test92": "internal.ayg.gz"}
          </p>
        </FormItem>
        <FormItem label="外部API检测:">
          <RadioGroup v-model="dataForm.is_external_check_api">
            <Radio label="true">是</Radio>
            <Radio label="false">否</Radio>
          </RadioGroup>
        </FormItem>
        <FormItem label="外部检测API:" v-show="dataForm.is_external_check_api === 'true'" prop="external_check_api">
          <Input v-model.trim="dataForm.external_check_api" placeholder="http://ops-url.aiyuangong.com/deliver/info"/>
          <p style="color: #2d8cf0; line-height: 15px; margin-top: 5px">* 外部检测API 不用设置urlooker agent; 默认直接使用default agent，
            确保default能通外网</p>
        </FormItem>
      </Form>
    </Modal>
    <Modal
      v-model="batchControlHostModal"
      title="批量关联主机"
      @on-ok="handlebatchCtrlHostOk"
      >
      <Alert show-icon type="warning">批量增加或删除关联主机，若新增环境或减少环境则需要批量修改APP所属的环境监控</Alert>
      <Form :model="batchCtrlHostForm" :label-width="80">
        <FormItem label="批量添加: ">
          <Checkbox v-model="batchCtrlHostForm.is_add"></Checkbox>
        </FormItem>
        <FormItem label="Hosts: " v-show="batchCtrlHostForm.is_add">
          <Select v-model="batchCtrlHostForm.add_hosts" multiple filterable>
            <Option v-for="item in hostsList" :value="`${item.id}:${item.owner}`" :key="`${item.id}:${item.owner}`">
              <Tag style="margin-right: 10px"><b>{{ item.owner }}</b></Tag> {{ item.hostname }}
            </Option>
          </Select>
        </FormItem>
        <FormItem label="批量删除: ">
          <Checkbox v-model="batchCtrlHostForm.is_delete"></Checkbox>
        </FormItem>
        <FormItem label="Hosts: " v-show="batchCtrlHostForm.is_delete">
          <Select v-model="batchCtrlHostForm.delete_hosts" multiple filterable>
            <Option v-for="item in hostsList" :value="`${item.id}:${item.owner}`" :key="`${item.id}:${item.owner}`">
              <Tag style="margin-right: 10px"><b>{{ item.owner }}</b></Tag> {{ item.hostname }}
            </Option>
          </Select>
        </FormItem>
        <FormItem label="已选择应用:">
          <p v-for="item in selectList" :key="item.id">{{ item.app_name }}</p>
        </FormItem>
      </Form>
    </Modal>
    <Modal
      v-model="batchCtrlEnvModal"
      title="批量操作修改监控APP所属环境"
      @on-ok="batchCtrlEnvModalOk"
      >
      <Alert show-icon type="warning">选择需要被监控的APP所属环境, 该环境会替换原有的监控环境</Alert>
      <Form :model="batchCtrlEnvForm" :label-width="100">
        <FormItem label="监控环境列表: ">
          <Select filter multiple v-model="batchCtrlEnvForm.envList" >
            <Option v-for="item in envList" :value="item" :key="item">
              {{ item }}
            </Option>
          </Select>
        </FormItem>
        <FormItem label="已选择应用:">
          <p v-for="item in selectList" :key="item.id">{{ item.app_name }}</p>
        </FormItem>
      </Form>
    </Modal>
  </div>
</template>
<script>

import {
  getAppDetail,
  createAppDetail,
  createUrlookerAppAlive,
  deleteUrlookerAppAlive,
  deleteAppDetail,
  getAllHosts,
  getAllUsers,
  getAppHostRel,
  updateAppDetail,
  getCmdbSetting,
  getServiceList,
  getAppSetting
} from '@/api/apps/app_managerment'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'apps_app_management',
  watch: {
    'dataForm.is_external_check_api' (newVal, oldVal) {
      if (newVal === 'false') {
        this.dataForm.external_check_api = ''
      }
    },
    'dataForm.is_internal_check_api' (newVal, oldVal) {
      if (newVal === 'false') {
        this.dataForm.internal_check_api = ''
        this.dataForm.internal_check_api_env = []
      }
    },
    appUsed: function (newVal, oldVal) {
      this.tableLoading = true
      if (newVal === false) {
        this.tableDatas = this.orginTableDatas
      } else {
        this.tableDatas = this.tableDatas.filter(item => {
          if (item.is_active) {
            return item
          }
        })
      }
      this.pageTotal = this.tableDatas.length
      this.tableLoading = false
    }
  },
  data () {
    const checkIcon = function (h, check) {
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
    const validateChoseAgent = (rule, value, callback) => {
      try {
        let valueArr = JSON.parse(value)
        if (typeof valueArr !== 'object') {
          callback(new Error('请输入 JSON 格式, 如 {"release": "default", "test92": "internal.ayg.gz", "preRelease": "default"}'))
        }
        callback()
      } catch (err) {
        callback(new Error('请输入 JSON 格式, 如 {"release": "default", "test92": "internal.ayg.gz"}'))
      }
    }
    return {
      envMonitorAgent: {},
      batchCtrlEnvForm: {
        envList: []
      },
      batchCtrlEnvModal: false,
      appUsed: false,
      isCheckArr: ['is_active', 'is_launch', 'is_publish', 'is_monitor', 'is_external_check_api', 'is_internal_check_api'],
      batchCtrlHostForm: {
        is_add: false,
        add_hosts: [],
        is_delete: false,
        delete_hosts: []
      },
      batchControlHostModal: false,
      tableLoading: false,
      serviceList: [],
      usernameList: [],
      hostsList: [],
      urlookerAgentList: ['default', 'internal.ayg.gz'],
      envList: [],
      editModalTitle: '',
      editModalAction: '',
      pageTotal: 0,
      pageSize: 20,
      ruleDataForm: {
        chose_agent: [
          { required: true, validator: validateChoseAgent, trigger: 'blur', type: 'string' }
        ],
        app_name: [
          { required: true, message: '必须填写', trigger: 'blur' }
        ],
        port: [
          { required: true, message: '必须填写', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '必须填写', trigger: 'blur' }
        ],
        service: [
          { required: true, message: '必须填写', trigger: 'blur' }
        ],
        connector: [
          { required: true, message: '必须填写', trigger: 'change', type: 'array' }
        ],
        hosts: [
          { required: true, message: '必须填写', trigger: 'change', type: 'array' }
        ]
      },
      originDataForm: {
        app_name: '',
        port: '',
        description: '',
        connector: [],
        is_active: 'false',
        is_publish: 'false',
        is_monitor: 'false',
        is_launch: 'false',
        is_internal_check_api: 'false',
        is_external_check_api: 'false',
        internal_check_api: '',
        internal_check_api_env: [],
        chose_agent: '',
        external_check_api: '',
        hosts: [],
        service: ''
      },
      dataForm: {},
      editModal: false,
      searchValue: '',
      orginTableDatas: [],
      tableDatas: [],
      selectList: [],
      searchList: ['app_name'],
      tableColumns: [
        {
          type: 'selection',
          width: 50
        },
        {
          'title': '应用名',
          'key': 'app_name',
          'sortable': true,
          'width': 150,
          render: (h, params) => {
            return h('a', {
              on: {
                click: () => {
                  let id = params.row.id
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
          'title': '端口',
          'key': 'port',
          'width': 80
        },
        {
          'title': '关联主机',
          render: (h, params) => {
            let hostList = params.row.host_list
            let renderList = []
            for (let env in hostList) {
              let hostDetailList = hostList[env]
              for (let idx in hostDetailList) {
                let hostObj = hostDetailList[idx]
                let id = hostObj.id
                let hostname = hostObj.hostname
                let privateIp = hostObj.private_ip
                let publicIp = hostObj.public_ip
                let cmdb = hostObj.cmdb
                renderList.push(
                  h('p', {}, [
                    h('a', {
                      on: {
                        click: () => {
                          const route = {
                            name: 'cmdb_host_info',
                            params: {
                              id
                            },
                            query: {
                              hostname,
                              cmdb
                            }
                          }
                          this.$router.push(route)
                        }
                      }
                    }, `【${cmdb} - ${env}】 ${hostObj.hostname}`),
                    h('p', {}, `（私）  ${privateIp}`),
                    h('p', {}, `（公）  ${publicIp}`)
                  ])
                )
              }
            }
            return h('div', {}, renderList)
          }
        },
        {
          'title': '服务',
          'key': 'service',
          'width': 80,
          'align': 'center',
          'sortable': true
        },
        {
          'title': '使用中',
          'key': 'is_active',
          'align': 'center',
          'width': 90,
          'sortable': true,
          render: (h, params) => {
            let check = params.row.is_active
            return checkIcon(h, check)
          }
        },
        {
          'title': '发布',
          'key': 'is_publish',
          'align': 'center',
          'width': 80,
          'sortable': true,
          render: (h, params) => {
            let check = params.row.is_publish
            return checkIcon(h, check)
          }
        },
        {
          'title': '监控',
          'key': 'is_monitor',
          'align': 'center',
          'width': 80,
          'sortable': true,
          render: (h, params) => {
            let check = params.row.is_monitor
            return checkIcon(h, check)
          }
        },
        {
          'title': '平台启动',
          'key': 'is_launch',
          'align': 'center',
          'width': 95,
          'sortable': true,
          render: (h, params) => {
            let check = params.row.is_launch
            return checkIcon(h, check)
          }
        },
        // {
        //   'title': '内部检测',
        //   'key': 'is_internal_check_api',
        //   'align': 'center',
        //   'width': 85,
        //   'sortable': true,
        //   render: (h, params) => {
        //     let check = params.row.is_internal_check_api
        //     return checkIcon(h, check)
        //   }
        // },
        // {
        //   'title': '外部检测',
        //   'key': 'is_external_check_api',
        //   'align': 'center',
        //   'width': 85,
        //   'sortable': true,
        //   render: (h, params) => {
        //     let check = params.row.is_external_check_api
        //     return checkIcon(h, check)
        //   }
        // },
        {
          'title': '操作',
          'width': 60,
          'align': 'center',
          render: (h, params) => {
            return h('div', {}, [
              h('a', {}, [
                h('Icon', {
                  props: {
                    'type': 'md-open'
                  },
                  on: {
                    click: () => {
                      let data = params.row
                      // 获取host，避免异步数据显示不了，所以直接同步
                      getAppHostRel(data.id).then(res => {
                        let hosts = res.data.map(item => {
                          return `${item.id}:${item.owner}`
                        })
                        let connector = data.connector_detail.map(item => {
                          return item.id
                        })
                        this.dataForm['id'] = data.id
                        this.dataForm.app_name = data.app_name
                        this.dataForm.port = data.port
                        this.dataForm.description = data.description
                        this.dataForm.connector = connector
                        this.dataForm.is_active = data.is_active.toString()
                        this.dataForm.is_publish = data.is_publish.toString()
                        this.dataForm.is_monitor = data.is_monitor.toString()
                        this.dataForm.is_launch = data.is_launch.toString()
                        this.dataForm.is_internal_check_api = data.is_internal_check_api.toString()
                        this.dataForm.is_external_check_api = data.is_external_check_api.toString()
                        this.dataForm.internal_check_api = data.internal_check_api
                        this.dataForm.internal_check_api_env = JSON.parse(data.internal_check_api_env)
                        this.dataForm.chose_agent = JSON.stringify(this.envMonitorAgent)
                        this.dataForm.external_check_api = data.external_check_api
                        this.dataForm.hosts = hosts
                        this.dataForm.service = data.service
                      })
                      this.editApp()
                    }
                  },
                  style: {
                    'font-size': '20px'
                  }
                })
              ])
            ])
          }
        }
      ]
    }
  },
  methods: {
    pageChange (page) {
      this.spliceTableDatas(page, this.orginTableDatas)
    },
    spliceTableDatas (page, originDatas) {
      this.tableDatas = originDatas.slice(page * this.pageSize - this.pageSize, page * this.pageSize)
    },
    batchCtrlEnvModalOk () {
      for (let idx in this.selectList) {
        let item = this.selectList[idx]
        item.internal_check_api_env = JSON.stringify(this.batchCtrlEnvForm.envList)
        item.chose_agent = JSON.stringify(this.envMonitorAgent)
        // 转换 check arr
        for (let idx in this.isCheckArr) {
          item[this.isCheckArr[idx]] = item[this.isCheckArr[idx]] === true ? 1 : 0
        }
        getAppHostRel(item.id).then(res => {
          let hosts = res.data.map(dd => {
            return `${dd.id}:${dd.owner}`
          })
          let connector = item.connector_detail.map(cd => {
            return cd.id
          })
          item.hosts = hosts
          item.connector = connector
          console.log(item)
          updateAppDetail(item.id, item).then(res => {
            this.$Message.success('更新app成功')
            let appId = res.data.id
            // 发送删除监控请求
            deleteUrlookerAppAlive(appId).then(res => {
              // 发送创建监控请求
              console.log(appId)
              createUrlookerAppAlive({ 'app_id': appId }).then(res => {
                this.$Message.success('操作Urlooker监控')
              })
            })
          }).catch(err => {
            sendNotice('error', err)
          })
        }).catch(err => {
          sendNotice('error', err)
        })
      }
    },
    handleBatchControlEnv () {
      if (this.selectList.length !== 0) {
        this.batchCtrlEnvModal = true
        this.batchCtrlEnvForm.envList = []
      } else {
        this.$Message.error('请选择需要操作的应用.')
      }
    },
    handlebatchCtrlHostOk () {
      for (let idx in this.selectList) {
        let item = this.selectList[idx]
        for (let idx in this.isCheckArr) {
          item[this.isCheckArr[idx]] = item[this.isCheckArr[idx]] === true ? 1 : 0
        }
        getAppHostRel(item.id).then(res => {
          let hosts = res.data.map(dd => {
            return `${dd.id}:${dd.owner}`
          })
          let connector = item.connector_detail.map(cd => {
            return cd.id
          })
          item.connector = connector
          if (this.batchCtrlHostForm.is_add) {
            this.batchCtrlHostForm.add_hosts.forEach(h => {
              if (hosts.indexOf(h) === -1) {
                hosts.push(h)
              }
            })
          }
          if (this.batchCtrlHostForm.is_delete) {
            let delList = []
            this.batchCtrlHostForm.delete_hosts.forEach(h => {
              if (hosts.indexOf(h) > -1) {
                delList.push(h)
              }
            })
            delList.forEach(idx => {
              hosts.pop(idx)
            })
          }
          item.hosts = hosts
          updateAppDetail(item.id, item).then(res => {
            this.$Message.success('更新app成功')
            let appId = res.data.id
            // 发送删除监控请求
            deleteUrlookerAppAlive(appId).then(res => {
              // 发送创建监控请求
              console.log(appId)
              createUrlookerAppAlive({ 'app_id': appId }).then(res => {
                this.$Message.success('操作Urlooker监控')
              })
            })
          }).catch(err => {
            sendNotice('error', err)
          })
        })
      }
      this.selectList = []
    },
    handleBatchControlHost () {
      console.log(this.selectList)
      this.batchCtrlHostForm = {
        is_add: false,
        add_hosts: [],
        is_delete: false,
        delete_hosts: []
      }
      if (this.selectList.length !== 0) {
        this.batchControlHostModal = true
      } else {
        this.$Message.error('请选择需要操作的应用.')
      }
    },
    enterSearch () {
      this.tableDatas = []
      this.searchList.forEach(idx => {
        this.orginTableDatas.forEach(item => {
          if (item[idx].toString().indexOf(this.searchValue) > -1) {
            this.tableDatas.push(item)
          }
        })
      })
      // console.log(this.tableDatas)
      this.pageTotal = this.tableDatas.length
    },
    selectChange (value) {
      this.selectList = value
      console.log(value)
    },
    deleteOk () {
      if (this.selectList) {
        this.selectList.forEach(item => {
          deleteUrlookerAppAlive(item.id).then(res => {
            deleteAppDetail(item.id).then(res2 => {
              this.$Message.success('删除 app 成功')
              this.reloadTable()
            })
          }).catch(err => {
            sendNotice('error', err)
            this.reloadTable()
          })
        })
      }
    },
    editOk (name) {
      if (this.dataForm.is_internal_check_api === 'true') {
        if (this.dataForm.internal_check_api.trim() === '' || this.dataForm.internal_check_api_env.length === 0) {
          this.$Message.error('信息未填写完整')
          return
        }
      }
      if (this.dataForm.is_external_check_api === 'true') {
        if (this.dataForm.external_check_api.trim() === '') {
          this.$Message.error('信息未填写完整')
          return
        }
      }
      this.$refs[name].validate((valid) => {
        if (valid) {
          let action = this.editModalAction
          if (action === 'add') {
            this.addAppHandler()
          } else if (action === 'update') {
            this.updateAppHandler()
          }
        } else {
          this.$Message.error('信息未填完整.')
        }
      })
    },
    addApp () {
      this.dataForm = JSON.parse(JSON.stringify(this.originDataForm))
      this.dataForm.chose_agent = JSON.stringify(this.envMonitorAgent)
      this.editModalTitle = '添加 App'
      this.editModal = true
      this.editModalAction = 'add'
    },
    editApp () {
      this.editModalTitle = '编辑 App'
      this.editModal = true
      this.editModalAction = 'update'
    },
    dataHandler (dataForm) {
      // 需要转换下状态
      for (let idx in this.isCheckArr) {
        dataForm[this.isCheckArr[idx]] = dataForm[this.isCheckArr[idx]] === 'true' ? 1 : 0
      }
      dataForm.internal_check_api_env = JSON.stringify(dataForm.internal_check_api_env)
      return dataForm
    },
    addAppHandler () {
      this.dataForm = this.dataHandler(this.dataForm)
      createAppDetail(this.dataForm).then(res => {
        this.$Message.success('创建app成功')
        this.reloadTable()
        // 发送创建监控请求
        createUrlookerAppAlive({ 'app_id': res.data.id }).then(res => {
          this.$Message.success('操作Urlooker监控')
          this.reloadTable()
        })
      }).catch(err => {
        sendNotice('error', err)
        this.reloadTable()
      })
    },
    updateAppHandler () {
      this.dataForm = this.dataHandler(this.dataForm)
      console.log(this.dataForm)
      updateAppDetail(this.dataForm.id, this.dataForm).then(res => {
        this.$Message.success('更新app成功')
        var appId = res.data.id
        // 发送删除监控请求
        deleteUrlookerAppAlive(appId).then(res => {
          // 发送创建监控请求
          createUrlookerAppAlive({ 'app_id': appId }).then(res => {
            this.$Message.success('操作Urlooker监控')
            this.reloadTable()
          })
        })
      }).catch(err => {
        sendNotice('error', err)
        this.reloadTable()
      })
    },
    reloadTable () {
      this.tableLoading = true
      getAppDetail().then(res => {
        this.orginTableDatas = res.data.reverse()
        this.tableDatas = this.orginTableDatas
        // this.pageChange(1)
        this.tableLoading = false
        this.pageTotal = this.orginTableDatas.length
      }).catch(err => {
        sendNotice('error', err)
      })
    }
  },
  mounted () {
    this.dataForm = JSON.parse(JSON.stringify(this.originDataForm))
    this.reloadTable()
    getAllHosts().then(res => {
      this.hostsList = res.data
    }).catch(err => {
      sendNotice('error', err)
    })
    getAllUsers().then(res => {
      this.usernameList = res.data
    }).catch(err => {
      sendNotice('error', err)
    })
    getCmdbSetting().then(res => {
      this.envList = res.data[0]['cmdb_setting']['base']['env']
      this.envList = this.envList.filter(item => {
        if (item !== 'external' && item !== 'undefined') {
          return item
        }
      })
    }).catch(err => {
      sendNotice('error', err)
    })
    getAppSetting().then(res => {
      this.envMonitorAgent = res.data[0]['app_setting']['env_monitor_agent']
    }).catch(err => {
      sendNotice('error', err)
    })
    getServiceList().then(res => {
      this.serviceList = res.data[0]['app_setting']['service']
    }).catch(err => {
      sendNotice('error', err)
    })
  }
}
</script>
