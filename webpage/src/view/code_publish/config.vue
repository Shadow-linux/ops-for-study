<template>
  <div>
    <Row>
      <Alert type="info" show-icon>发布配置，用于代码发布。</Alert>
      <Col span="24">
        <Card>
          <p slot="title">
            <span style="font-size: 14px; color: #909399">发布配置</span>
            <a style="float: right; font-weight: normal; font-size: 12px" @click="refreshChoseData">刷新</a>
          </p>
          <Tabs value="ALL" type="card"  size="small" :animated="false" @on-click="choseTab">
            <TabPane v-for="tab in tabs" :key="tab.id" :name="tab.env" :label="tab.env">
              <div style="margin-top: 20px">
                <Row :gutter="10">
                  <Col span="10">
                    <Poptip
                      confirm
                      title="确认删除吗 ?"
                      @on-ok="deleteData"
                      placement="right-start"
                      style="margin-right: 10px">
                      <Button size="small">删除</Button>
                    </Poptip>
                    <Tooltip placement="bottom-start" content="复制配置后，请记住修改环境对应的IP">
                      <Button type="error" ghost size="small" style="margin-right: 10px"
                      v-if="currentTab !== 'ALL'" @click="handleCopyFormShow"
                      >批量复制配置</Button>
                    </Tooltip>
                    <Button type="primary" ghost size="small" style="margin-right: 10px" @click="handleCreateModal">创建发布配置</Button>
                  </Col>
                  <Col span="10" offset="4">
                    <Dropdown trigger="click" @on-click="handleServerMode" >
                      <Button type="primary" size="small" ghost>
                        Server Mode
                        <Icon type="ios-arrow-down"></Icon>
                      </Button>
                      <DropdownMenu slot="list">
                        <DropdownItem v-for="sm in configFormSelect.server_mode" :name="sm" :key="sm">{{ sm }}</DropdownItem>
                      </DropdownMenu>
                    </Dropdown>
                    <Button type="default"  size="small" style="margin-left: 10px;margin-right: 10px" @click="() => { changeIpModal = true; getOldIps() }">批量更换发布IP</Button>
                    <Input v-model="searchApp" placeholder="应用名" style="width: 54%" @on-enter="searchValue" search></Input>
                  </Col>
                </Row:>
              </div>
              <Table :columns="tableColumn" :loading="tableLoading" @on-selection-change="(items) => {
                tableSelectedIds = items.map(item => {
                  return item.id
                })}" :data="tableData" style="margin-top: 10px"></Table>
            </TabPane>
            <Dropdown slot="extra" placement="bottom-end" @on-click="hadnleDropDown">
              <a style="font-size: 13px">
                更多操作
                <Icon type="ios-arrow-down"></Icon>
              </a>
              <DropdownMenu slot="list">
                <DropdownItem name="add_env">增加 Env Tab</DropdownItem>
                <DropdownItem name="update_env">更新 Env Tab</DropdownItem>
                <DropdownItem name="delete_env">删除 Env Tab</DropdownItem>
              </DropdownMenu>
            </Dropdown>
          </Tabs>
        </Card>
      </Col>
    </Row>
    <Modal
      v-model="createModal"
      :title="createModalTitle"
      :mask-closable="false"
      :styles="{top: '20px'}"
      :mask="true"
      >
      <Alert show-icon> <b style="color: red; font-size: 20px;">*</b> 号为必填项</Alert>
      <Form ref="configForm" :model="configForm" :label-width="120" :rules="ruleConfigForm" >
        <Divider style="color: #909399; font-size: 13px">基础配置</Divider>
        <FormItem label="应用名:" prop="app_name">
          <Select v-model="configForm.app_name" filterable @on-change="handleAppNameChange">
            <Option v-for="app in appList" :value="app" :key="app">{{ app }}</Option>
          </Select>
        </FormItem>
        <FormItem label="(前/后) 端:" prop="web_tag">
          <Select v-model="configForm.web_tag" filterable @on-change="(value) => {
            currentWebTag = value
          }">
            <Option v-for="item in configFormSelect.web_tag" :value="item" :key="item">{{ item }}</Option>
          </Select>
        </FormItem>
        <FormItem label="环境:" prop="env">
          <Select v-model="configForm.env" filterable @on-change="handleEnvChange">
            <Option v-for="tab in dynamicTabs" :value="tab.env" :key="tab.env">{{ tab.env }}</Option>
          </Select>
        </FormItem>
        <FormItem label="发布IP:" prop="publish_ip" >
          <Select v-model="configForm.publish_ip" multiple >
            <Option v-for="item in configFormSelect.appEnvIp" :value="item[0]" :key="item[0]">
              {{ item[0] }}
              <span style="float:right;color:#909399">{{ item[1] }}</span>
            </Option>
          </Select>
        </FormItem>
        <FormItem label="Server Mode:" prop="server_mode">
          <Select v-model="configForm.server_mode">
            <Option v-for="item in configFormSelect.server_mode" :value="item" :key="item">{{ item }}
              <span style="float:right;color:#909399">(发布设置中定义)</span>
            </Option>
          </Select>
        </FormItem>
        <FormItem label="Jenkins Project:" prop="jenkins_project">
          <Select v-model="configForm.jenkins_project">
            <Option v-for="item in configFormSelect.jenkins_project" :value="item" :key="item">{{ item }}
              <span style="float:right;color:#909399">(发布设置中定义)</span>
            </Option>
          </Select>
        </FormItem>
        <FormItem label="Git Url:" prop="git_url">
          <Input v-model.trim="configForm.git_url" placeholder="">{{ configForm.git_url }}</Input>
        </FormItem>
        <FormItem label="发布步骤:" prop="steps_id">
          <Select v-model="configForm.steps_id">
            <Option v-for="opts in configFormSelect.steps" :value="opts.id" :key="opts.id">{{ opts.name }}
              <span style="float:right;color:#909399">模版</span>
            </Option>
          </Select>
        </FormItem>
        <div v-show="currentWebTag === 'frontend'">
          <Divider style="color: #909399; font-size: 13px">参数配置 (前端)</Divider>
          <h1 style="text-align: center;color: #909399 ">None</h1>
        </div>
        <div v-show="currentWebTag === 'backend'">
          <Divider style="color: #909399; font-size: 13px">参数配置 (后端)</Divider>
            <FormItem label="Package Name:" prop="pkg_name">
              <Input v-model.trim="configForm.pkg_name" placeholder="">{{ configForm.pkg_name }}</Input>
            </FormItem>
            <FormItem label="APP Port:" prop="port">
              <InputNumber v-model="configForm.port" style="width: 100%" :min="0" :max="65535" placeholder="">{{ configForm.port }}</InputNumber>
            </FormItem>
            <FormItem label="Mvn Options:" prop="mvn_opts_id">
              <Select v-model="configForm.mvn_opts_id">
                <Option v-for="opts in configFormSelect.mvn_opts" :value="opts.id" :key="opts.id">{{ opts.name }}
                  <span style="float:right;color:#909399">模版</span>
                </Option>
              </Select>
            </FormItem>
            <FormItem label="Gradle Options:" prop="gradle_opts_id">
              <Select v-model="configForm.gradle_opts_id">
                <Option v-for="opts in configFormSelect.gradle_opts" :value="opts.id" :key="opts.id">{{ opts.name }}
                  <span style="float:right;color:#909399">模版</span>
                </Option>
              </Select>
            </FormItem>
            <FormItem label="Java Options:" prop="java_opts_id">
              <Select v-model="configForm.java_opts_id">
                <Option v-for="opts in configFormSelect.java_opts" :value="opts.id" :key="opts.id">{{ opts.name }}
                  <span style="float:right;color:#909399">模版</span>
                </Option>
              </Select>
            </FormItem>
            <FormItem label="Jar Options:" prop="jar_opts_id">
              <Select v-model="configForm.jar_opts_id">
                <Option v-for="opts in configFormSelect.jar_opts" :value="opts.id" :key="opts.id">{{ opts.name }}
                  <span style="float:right;color:#909399">模版</span>
                </Option>
              </Select>
            </FormItem>
            <FormItem label="Docker Options:" prop="docker_opts_id">
              <Select v-model="configForm.docker_opts_id">
                <Option v-for="opts in configFormSelect.docker_opts" :value="opts.id" :key="opts.id">{{ opts.name }}
                  <span style="float:right;color:#909399">模版</span>
                </Option>
              </Select>
            </FormItem>
            <FormItem label="Dockerfile:" prop="dockerfile_id">
              <Select v-model="configForm.dockerfile_id">
                <Option v-for="opts in configFormSelect.dockerfile" :value="opts.id" :key="opts.id">{{ opts.name }}
                  <span style="float:right;color:#909399">模版</span>
                </Option>
              </Select>
            </FormItem>
        </div>
      </Form>
      <div slot="footer">
        <Button type="default" @click="handleReset('configForm')">重置</Button>
        <Button type="primary" ghost :loading="commitLoading" @click="handlePublishConfig('configForm')">提交</Button>
      </div>
    </Modal>
    <Modal
      v-model="envModal"
      :title="envModalTitle"
      @on-ok="handleEnv('envForm')"
      :mask="true"
      >
      <Alert type="warning" show-icon>环境名与应用名，不是强关系，即删除后也不会将整个已配置列表删除掉，只是不显示而已。</Alert>
      <Form ref="envForm" :model="envForm" :label-width="100" :rules="ruleEnvForm" inline>
        <FormItem v-if="envCurrentMode === 'update'" label="环境名(旧)" prop="id">
          <Select v-model="envForm.id" style="width:300px">
              <Option v-for="tab in dynamicTabs" :value="tab.id" :key="tab.env">{{ tab.env }}</Option>
          </Select>
        </FormItem>
        <FormItem label="环境名" prop="env">
          <Input v-model.trim="envForm.env" autofocus placeholder="env" style="width: 300px"></Input>
        </FormItem>
      </Form>
    </Modal>
    <Modal
      v-model="copyModal"
      :title="copyModalTitle"
      :closable="false"
      :mask-closable="false"
      @on-ok="handleCopyForm('copyForm')"
      >
      <Alert type="warning" show-icon>若被复制的配置已存在于被选中的环境中，则会出现错误异常 (部分复制成功，部分失败的情况).</Alert>
      <Form ref="copyForm" :model="copyForm" :label-width="120" :rules="ruleCopyForm" inline>
        <FormItem label="复制配置到(环境):" prop="envs">
          <Select v-model="copyForm.envs" multiple style="width:300px">
            <Option v-for="tab in dynamicTabs" :value="tab.env" :key="tab.env">{{ tab.env }}</Option>
          </Select>
        </FormItem>
      </Form>
    </Modal>
    <Modal
      v-model="batchCopyModal"
      title="批量复制配置"
      :closable="false"
      :mask-closable="false"
      @on-ok="handleBatchCopyForm('batchCopyForm')"
      >
      <Alert type="warning" show-icon>若被复制的配置已存在于被选中的环境中，则会出现错误异常 (部分复制成功，部分失败的情况).</Alert>
      <Form ref="batchCopyForm" :model="batchCopyForm" :label-width="120" :rules="ruleBatchCopyForm" inline>
        <FormItem label="复制配置到(环境):" prop="env">
          <Select v-model="batchCopyForm.env" style="width:300px">
            <Option v-for="tab in dynamicTabs" :value="tab.env" :key="tab.env">{{ tab.env }}</Option>
          </Select>
        </FormItem>
        <FormItem label="已选择的应用:">
          <p v-for="app in batchCopyAppShowList" :key="app">{{ app }}</p>
        </FormItem>
      </Form>
    </Modal>
    <Modal
      v-model="checkModal"
      :title="checkModalTitle"
      @on-ok="handleCheckModal"
      :width="800"
      >
      <Form :model="detailForm" :label-width="120">
        <Divider style="color: #909399; font-size: 13px">基础配置</Divider>
        <FormItem label="应用名:">
            <b>{{ detailForm.app_name }}</b>
        </FormItem>
        <FormItem label="环境:">
            <b>{{ detailForm.env }}</b>
        </FormItem>
        <FormItem label="(前/后) 端:">
            <b>{{ detailForm.web_tag }}</b>
        </FormItem>
        <FormItem label="发布IP:">
          <br>
          <ol>
            <li v-for="(ip, id) in detailForm.publish_ip" :key="id"><b>{{ ip }}</b></li>
          </ol>
        </FormItem>
        <FormItem label="Server Mode:">
            <b>{{ detailForm.server_mode }}</b>
        </FormItem>
        <FormItem label="Jenkins Project:">
            <b>{{ detailForm.jenkins_project }}</b>
        </FormItem>
        <FormItem label="Git Url:">
            <b>{{ detailForm.git_url }}</b>
        </FormItem>
        <FormItem label="部署步骤:">
          <b style="color: #909399;">模版：{{ detailForm.steps.name }}</b>
          <br>
          <b v-if="detailForm.steps.deploy_steps">{{ detailForm.steps.deploy_steps.join('  -->  ') }}</b>
        </FormItem>
        <FormItem label="回滚步骤:">
          <b style="color: #909399;">模版：{{ detailForm.steps.name }}</b>
          <br>
          <b v-if="detailForm.steps.rollback_steps">{{ detailForm.steps.rollback_steps.join('  -->  ') }}</b>
        </FormItem>
        <FormItem label="最后修改时间:">
            <b>{{ detailForm.updated }}</b>
        </FormItem>
        <div v-if="currentWebTag === 'frontend'">
          <Divider style="color: #909399; font-size: 13px">参数配置 (前端)</Divider>
          <h4 style="color: #909399;text-align:center">None</h4>
        </div>
        <div v-if="currentWebTag === 'backend'">
          <Divider style="color: #909399; font-size: 13px">参数配置 (后端)</Divider>
          <FormItem label="Package Name:">
              <b>{{ detailForm.pkg_name }}</b>
          </FormItem>
          <FormItem label="App Port:">
              <b>{{ detailForm.port }}</b>
          </FormItem>
          <FormItem label="Mvn Options:">
            <b style="color: #909399;">模版：{{ detailForm.mvn_opts.name }}</b>
            <br>
            <b>{{ detailForm.mvn_opts.mvn_opts }}</b>
          </FormItem>
          <FormItem label="Gradle Options:">
            <b style="color: #909399;">模版：{{ detailForm.gradle_opts.name }}</b>
            <br>
            <b>{{ detailForm.gradle_opts.gradle_opts }}</b>
          </FormItem>
          <FormItem label="Java Options:">
            <b style="color: #909399;">模版：{{ detailForm.java_opts.name }}</b>
            <br>
            <b>{{ detailForm.java_opts.java_opts }}</b>
          </FormItem>
          <FormItem label="Jar Options:">
            <b style="color: #909399;">模版：{{ detailForm.jar_opts.name }}</b>
            <br>
            <b>{{ detailForm.jar_opts.jar_opts }}</b>
          </FormItem>
          <FormItem label="Dockerfile:">
            <b style="color: #909399;">模版：{{ detailForm.dockerfile.name }}</b>
            <br>
            <Input type="textarea" style="width: 100%" readonly :rows="6" :value="detailForm.dockerfile.dockerfile"></Input>
          </FormItem>
          <FormItem label="Docker Options:">
            <b style="color: #909399;">模版：{{ detailForm.docker_opts.name }}</b>
            <br>
            <b>{{ detailForm.docker_opts.docker_opts }}</b>
          </FormItem>
        </div>
      </Form>
    </Modal>
    <Modal
      v-model="changeIpModal"
      title="批量更换IP"
      @on-ok="handleChangeIpModal('changeIpForm')"
      :mask="false"
      >
      <Alert show-icon type="warning">若新的IP不存在于被修改的环境的机器中，则会出现异常显示等问题 (通常修改回有的IP即可)</Alert>
      <Form ref="changeIpForm" :model="changeIpForm" :label-width="100" :rules="ruleChangeIpForm" inline>
        <FormItem label="环境:" prop="envs">
          <Select v-model="changeIpForm.envs" multiple style="width: 300px">
            <Option v-for="tab in dynamicTabs" :value="tab.env" :key="tab.id">{{ tab.env }}</Option>
          </Select>
        </FormItem>
        <FormItem label="旧IP:" prop="old_ip">
          <Select v-model="changeIpForm.old_ip" filterable style="width: 300px">
            <Option v-for="ip in oldIps" :value="ip" :key="ip">{{ ip }}</Option>
          </Select>
        </FormItem>
        <FormItem label="新IP:" prop="new_ip">
          <Input v-model.trim="changeIpForm.new_ip" placeholder="new ip" style="width: 300px"></Input>
        </FormItem>
      </Form>
    </Modal>
  </div>
</template>
<script>
import {
  getEnvs, createEnv, updateEnv, deleteEnv, getMainConfs,
  replaceIp, copyConfig, deleteMainConf, getAppDetail, createWebMainConf, updateWebMainConf,
  getMvnOpts, getJavaOpts, getJarOpts, getDockerOpts, getDockefile, getSteps, getCodePublish,
  batchCopyConfig, getGradleOpts
} from '@/api/code_publish/config'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'code_publish_conf',
  computed: {
    dynamicTabs: function () {
      return this.tabs.filter(tab => {
        if (tab.env !== 'ALL') {
          return tab
        }
      })
    }
  },
  data () {
    return {
      commitLoading: false,
      batchCopyAppShowList: [],
      batchCopyModal: false,
      batchCopyForm: {
        env: '',
        app_ids: []
      },
      currentSelectAppName: '',
      currentSelectEnv: '',
      appList: [],
      appDetail: {},
      currentTab: 'ALL',
      tableSelectedIds: [],
      oldIps: [],
      changeIpModal: false,
      searchApp: '',
      tableLoading: false,
      currentCreateModal: 'create',
      createModal: false,
      createModalTitle: '',
      currentWebTag: 'frontend',
      configFormSelect: {
        web_tag: ['frontend', 'backend'],
        jenkins_project: [],
        server_mode: [],
        appEnvIp: [],
        mvn_opts: [],
        java_opts: [],
        jar_opts: [],
        docker_opts: [],
        dockerfile: [],
        steps: [],
        gradle_opts: []
      },
      configForm: {
        app_name: '',
        env: '',
        web_tag: '',
        publish_ip: [],
        pkg_name: '',
        port: 0,
        server_mode: '',
        git_url: '',
        jenkins_project: '',
        mvn_opts_id: 0,
        java_opts_id: 0,
        jar_opts_id: 0,
        docker_opts_id: 0,
        steps_id: 0,
        dockerfile_id: 0,
        gradle_opts_id: 0
      },
      ruleBatchCopyForm: {
        env: [
          {
            required: true, message: '必须填写', trigger: 'change'
          }
        ]
      },
      ruleConfigForm: {
        app_name: [
          {
            required: true, message: '必须填写', trigger: 'blur'
          }
        ],
        web_tag: [
          {
            required: true, message: '必须填写', trigger: 'change'
          }
        ],
        env: [
          {
            required: true, message: '必须填写', trigger: 'change'
          }
        ],
        publish_ip: [
          {
            required: true, message: '必须填写', trigger: 'change', type: 'array'
          }
        ],
        server_mode: [
          {
            required: true, message: '必须填写', trigger: 'change'
          }
        ],
        jenkins_project: [
          {
            required: true, message: '必须填写', trigger: 'change'
          }
        ],
        git_url: [
          {
            required: true, message: '必须填写', trigger: 'blur'
          }
        ],
        steps_id: [
          {
            required: true, message: '必须填写'
          }
        ]
      },
      checkModal: false,
      checkModalTitle: '',
      copyModal: false,
      copyModalTitle: '',
      detailForm: {
        app_name: '',
        web_tag: '',
        env: '',
        publish_ip: [],
        git_url: '',
        jenkins_project: '',
        updated: '',
        pkg_name: '',
        mvn_opts: {},
        java_opts: {},
        jar_opts: {},
        gradle_opts: {},
        docker_opts: {},
        steps: {
          deploy_steps: [],
          rollback_steps: []
        },
        dockerfile: {}
      },
      changeIpForm: {
        envs: '',
        old_ip: '',
        new_ip: ''
      },
      copyForm: {
        envs: [],
        id: ''
      },
      envModal: false,
      envModalTitle: '',
      envCurrentMode: '',
      envForm: {
        id: '',
        env: ''
      },
      tabs: [
        {
          'id': 1,
          'env': 'ALL'
        }
      ],
      ruleChangeIpForm: {
        envs: [
          {
            required: true, message: '必须选择', trigger: 'change', type: 'array'
          }
        ],
        old_ip: [
          {
            required: true, message: '必须选择', trigger: 'change'
          }
        ],
        new_ip: [
          {
            required: true, message: '必须填写', trigger: 'blur'
          }
        ]
      },
      ruleCopyForm: {
        envs: [
          {
            required: true, message: '必须选择', trigger: 'change', type: 'array'
          }
        ]
      },
      ruleEnvForm: {
        env: [
          { required: true, message: '必须填写', trigger: 'blur' }
        ]
      },
      tableColumn: [
        {
          type: 'selection',
          width: 50,
          align: 'center'
        },
        {
          title: '应用名',
          key: 'app_name',
          width: 150,
          tooltips: true,
          sortable: true
        },
        {
          title: '环境',
          key: 'env',
          width: 100,
          sortable: true
        },
        {
          title: '发布IP',
          key: 'publish_ip',
          width: 150,
          render: (h, params) => {
            let ips = []
            for (let idx in params.row.publish_ip) {
              let ip = params.row.publish_ip[idx]
              ips.push(
                h('p', {}, `${ip}`)
              )
            }
            return h('div', {}, ips)
          }
        },
        {
          title: '(前/后) 端',
          key: 'web_tag',
          width: 150,
          sortable: true,
          render: (h, params) => {
            let color
            switch (params.row.web_tag) {
              case 'backend':
                color = 'volcano'
                break
              case 'frontend':
                color = 'green'
                break
            }
            return h('div', {}, [
              h('Tag', {
                props: {
                  color: color
                }
              }, params.row.web_tag)
            ])
          }
        },
        {
          title: 'Jenkins Project',
          key: 'jenkins_project',
          tooltips: true
        },
        {
          title: 'Server Mode',
          key: 'server_mode',
          tooltips: true,
          align: 'center',
          sortable: true
        },
        {
          title: '修改日期',
          align: 'center',
          key: 'updated',
          width: 150,
          sortable: true,
          sortType: 'desc'
        },
        {
          title: '操作',
          align: 'center',
          width: 180,
          render: (h, params) => {
            return h('div', {}, [
              h('a', {
                style: {
                  'margin-right': '10px'
                },
                on: {
                  click: () => {
                    this.checkModal = true
                    this.checkModalTitle = `查看${params.row.env}环境 ${params.row.app_name} 信息配置`
                    this.detailForm = params.row
                    this.currentWebTag = params.row.web_tag
                  }
                }
              }, '详细信息'),
              h('a', {
                on: {
                  click: () => {
                    this.copyModal = true
                    this.copyForm.id = params.row.id
                    this.copyModalTitle = `复制 ${params.row.app_name} 发布配置`
                    this.configForm.publish_ip = []
                  }
                }
              }, '复制'),
              h('a', {
                style: {
                  'margin-left': '10px'
                },
                on: {
                  click: () => {
                    try {
                      this.handleUpdateModal()
                      let data = params.row
                      console.log(this.appDetail)
                      this.configFormSelect.appEnvIp = this.appDetail[data.app_name][data.env.toLowerCase()]
                      // 通过判断没有IP 的至为空
                      if (!this.configFormSelect.appEnvIp) {
                        data.publish_ip = []
                      }
                      this.configForm = {
                        id: data.id,
                        app_name: data.app_name,
                        env: data.env,
                        publish_ip: data.publish_ip,
                        pkg_name: data.pkg_name,
                        server_mode: data.server_mode,
                        git_url: data.git_url,
                        jenkins_project: data.jenkins_project,
                        mvn_opts_id: data.mvn_opts.id,
                        java_opts_id: data.java_opts.id,
                        jar_opts_id: data.jar_opts.id,
                        gradle_opts_id: data.gradle_opts.id,
                        docker_opts_id: data.docker_opts.id,
                        steps_id: data.steps.id,
                        dockerfile_id: data.dockerfile.id,
                        web_tag: data.web_tag,
                        port: data.port
                      }
                      this.currentSelectAppName = data.app_name
                      this.currentWebTag = data.web_tag
                    } catch (err) {
                      sendNotice('error', '检查App管理中未允许 “发布”')
                      sendNotice('error', err)
                    }
                  }
                }
              }, '编辑')
            ])
          }
        }
      ],
      tableData: [],
      tmpTableData: [],
      originTableData: []
    }
  },
  methods: {
    handleServerMode (name) {
      this.tableLoading = true
      if (this.currentTab === 'ALL') {
        this.tableData = this.originTableData
      } else {
        this.tableData = this.originTableData.filter(item => {
          if (item.env === this.currentTab) {
            return item
          }
        })
      }
      this.tableData = this.tableData.filter(item => {
        if (item.server_mode === name) {
          return item
        }
      })
      this.tableLoading = false
    },
    handleCopyFormShow () {
      this.batchCopyForm.app_ids = this.tableSelectedIds
      if (this.batchCopyForm.app_ids.length !== 0) {
        this.batchCopyAppShowList = []
        this.batchCopyModal = true
        this.tableData.forEach(item => {
          if (this.batchCopyForm.app_ids.indexOf(item.id) !== -1) {
            this.batchCopyAppShowList.push(item.app_name)
          }
        })
      } else {
        this.$Message.error('请选择需要复制的APP。')
      }
    },
    // 处理 app name
    handleAppNameChange (appName) {
      if (appName) {
        this.currentSelectAppName = appName
        this.configForm.env = ''
        this.configForm.publish_ip = []
      }
    },
    // 处理env 触发
    handleEnvChange (env) {
      if (env) {
        console.log(this.appDetail[this.currentSelectAppName])
        this.configForm.publish_ip = []
        this.configFormSelect.appEnvIp = this.appDetail[this.currentSelectAppName][env.toLowerCase()]
      }
    },
    // 创建发布配置
    handleCreateModal () {
      this.createModal = true
      this.createModalTitle = '创建发布配置'
      this.currentCreateModal = 'create'
      this.refreshVarietyArgs()
      // this.configFormSelect.appEnvIp = []
    },
    //  更新发布配置
    handleUpdateModal () {
      this.createModal = true
      this.createModalTitle = '更新发布配置'
      this.currentCreateModal = 'update'
      this.refreshVarietyArgs()
    },
    handleReset (name) {
      this.$refs[name].resetFields()
    },
    // 操作配置
    handlePublishConfig (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          this.commitLoading = true
          if (this.currentCreateModal === 'create') {
            this.configForm.publish_ip = JSON.stringify(this.configForm.publish_ip)
            createWebMainConf(this.configForm).then(res => {
              this.$Message.success('成功配置创建')
              this.refresTabledata()
              this.commitLoading = false
              this.createModal = false
            }).catch(err => {
              sendNotice('error', err)
              this.commitLoading = false
              this.createModal = false
            })
          } else if (this.currentCreateModal === 'update') {
            this.configForm.publish_ip = JSON.stringify(this.configForm.publish_ip)
            updateWebMainConf(this.configForm.id, this.configForm).then(res => {
              this.$Message.success('更新配置创建')
              this.refreshChoseData()
              this.commitLoading = false
              this.createModal = false
            }).catch(err => {
              sendNotice('error', err)
              this.commitLoading = false
              this.createModal = false
            })
          }
        } else {
          this.$Message.error('提交失败，不可缺少必要参数')
        }
      })
    },
    // 刷新当前页的数据
    refreshChoseData () {
      this.tableLoading = true
      getMainConfs().then(res => {
        this.originTableData = res.data.reverse()
        this.choseTab(this.currentTab)
        this.tableLoading = false
      }).catch(err => {
        sendNotice('error', err)
        this.tableLoading = false
      })
    },
    // 获取所有旧IP
    getOldIps () {
      this.oldIps = []
      this.originTableData.forEach(item => {
        if (item.publish_ip) {
          item.publish_ip.forEach(ip => {
            if (this.oldIps.indexOf(ip) === -1) {
              this.oldIps.push(ip)
            }
          })
        }
      })
    },
    // 批量更换IP
    handleChangeIpModal (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          this.changeIpForm.envs.forEach(env => {
            let data = {
              'env': env,
              'old_ip': this.changeIpForm.old_ip,
              'new_ip': this.changeIpForm.new_ip
            }
            replaceIp(data).then(res => {
              this.$Message.success('切换IP成功')
            }).catch(err => {
              sendNotice('error', err)
            })
          })
        } else {
          this.$Message.error('请填写完整信息。')
        }
      })
    },
    // 搜索 app 名
    searchValue () {
      this.tableLoading = true
      if (this.currentTab === 'ALL') {
        this.tableData = this.originTableData
      } else {
        this.tableData = this.originTableData.filter(item => {
          if (item.env === this.currentTab) {
            return item
          }
        })
      }
      if (this.searchApp.length === 0) {
        this.tableLoading = false
        return
      }
      this.tableData = this.tableData.filter(item => {
        if (item.app_name.indexOf(this.searchApp) > -1) {
          return item
        }
      })
      this.tableLoading = false
    },
    // delete table data
    deleteData () {
      this.tableSelectedIds.forEach(id => {
        deleteMainConf(id).then(res => {
          this.$Message.success(`删除Table ${id}`)
          this.refreshChoseData()
        }).catch(err => {
          sendNotice('error', err)
        })
      })
    },
    // table data
    refresTabledata () {
      this.tableLoading = true
      getMainConfs().then(res => {
        this.tableData = res.data
        this.originTableData = res.data
        this.tableLoading = false
      }).catch(err => {
        sendNotice('error', err)
        this.tableLoading = false
      })
    },
    // 查看配置
    handleCheckModal () {},
    // 批量复制配置
    handleBatchCopyForm (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          batchCopyConfig(this.batchCopyForm).then(res => {
            this.$Message.success('批量复制发布配置成功')
          }).catch(err => {
            if (err.response.request.responseText.indexOf('Duplicate') > -1) {
              sendNotice('error', '某配置已存在, 请确认后再添加')
              return
            }
            sendNotice('error', err)
          })
        } else {
          this.$Message.error('完整填写信息')
        }
      })
    },
    // 复制app配置
    handleCopyForm (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          let data = {
            envs: this.copyForm.envs
          }
          copyConfig(this.copyForm.id, data).then(res => {
            this.$Message.success('复制发布配置成功')
          }).catch(err => {
            if (err.response.request.responseText.indexOf('Duplicate') > -1) {
              sendNotice('error', '配置已存在, 请确认后再添加')
              return
            }
            sendNotice('error', err)
          })
        } else {
          this.$Message.error('完整填写信息')
        }
      })
    },
    // 环境相关
    clearEnvForm () {
      this.envForm = {
        id: '',
        env: ''
      }
    },
    // 环境相关
    addEnv () {
      if (this.envForm.env.toUpperCase() === 'ALL') {
        this.$Message.error('环境名不能为 ALL/all')
        return
      }
      createEnv(this.envForm).then(res => {
        this.$Message.success('添加成功')
        this.refreshTabs()
        this.clearEnvForm()
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    // 环境相关
    _updateEnv () {
      if (this.envForm.env.toUpperCase() === 'ALL') {
        this.$Message.error('环境名不能为 ALL/all')
        return
      }
      updateEnv(this.envForm.id, this.envForm).then(res => {
        this.$Message.success('更新成功')
        this.refreshTabs()
        this.clearEnvForm()
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    // 环境相关
    deleteEnv () {
      if (this.envForm.env.toUpperCase() === 'ALL') {
        this.$Message.error('环境名不能为 ALL/all')
        return
      }
      this.tabs.forEach(tab => {
        if (tab.env === this.envForm.env) {
          deleteEnv(tab.id).then(res => {
            this.$Message.success('删除成功')
            this.refreshTabs()
            this.clearEnvForm()
          }).catch(err => {
            sendNotice('error', err)
          })
        }
      })
    },
    // 环境相关
    handleEnv (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          if (this.envCurrentMode === 'add') {
            this.addEnv()
          } else if (this.envCurrentMode === 'delete') {
            this.deleteEnv()
          } else if (this.envCurrentMode === 'update') {
            this._updateEnv()
          }
        } else {
          this.$Message.error('请填写完整信息')
        }
      })
    },
    // 环境相关
    hadnleDropDown (name) {
      console.log(name)
      if (name === 'add_env') {
        this.envModal = true
        this.envModalTitle = '增加 Env Tab'
        this.envCurrentMode = 'add'
      }
      if (name === 'delete_env') {
        this.envModal = true
        this.envModalTitle = '删除 Env Tab'
        this.envCurrentMode = 'delete'
      }
      if (name === 'update_env') {
        this.envModal = true
        this.envModalTitle = '更新 Env Tab'
        this.envCurrentMode = 'update'
      }
    },
    // 环境相关
    handleTabRemove (name) {
      let tabConfig = {
        title: `Tab 操作提示`,
        content: `是否删除Tab <${name}>`,
        onOk: () => { this['tab' + name] = false },
        onCancel: () => {
          this['tab' + name] = true
          this.mainTab = false
          this.mainTab = true
        }
      }
      this.$Modal.confirm(tabConfig)
    },
    // 环境相关
    refreshTabs () {
      getEnvs().then(res => {
        this.tabs = res.data
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    // 切换环境
    choseTab (tab) {
      this.tableLoading = true
      this.currentTab = tab
      if (tab === 'ALL') {
        this.tableData = this.originTableData
        this.tableLoading = false
        return
      }
      this.tableData = this.originTableData.filter(item => {
        if (item.env === tab) {
          return item
        }
      })
      this.tableLoading = false
    },
    // 获取 app env ip
    refreshAppIp () {
      this.appList = []
      getAppDetail().then(res => {
        for (let appName in res.data) {
          this.appList.push(appName)
        }
        this.appDetail = res.data
        console.log(this.appDetail)
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    // 获取 各选项参数
    refreshVarietyArgs () {
      getMvnOpts().then(res => {
        this.configFormSelect.mvn_opts = res.data
      }).catch(err => {
        sendNotice('error', err)
      })
      getGradleOpts().then(res => {
        this.configFormSelect.gradle_opts = res.data
      }).catch(err => {
        sendNotice('error', err)
      })
      getJavaOpts().then(res => {
        this.configFormSelect.java_opts = res.data
      }).catch(err => {
        sendNotice('error', err)
      })
      getJarOpts().then(res => {
        this.configFormSelect.jar_opts = res.data
      }).catch(err => {
        sendNotice('error', err)
      })
      getDockerOpts().then(res => {
        this.configFormSelect.docker_opts = res.data
      }).catch(err => {
        sendNotice('error', err)
      })
      getDockefile().then(res => {
        this.configFormSelect.dockerfile = res.data
      }).catch(err => {
        sendNotice('error', err)
      })
      getSteps().then(res => {
        this.configFormSelect.steps = res.data
      }).catch(err => {
        sendNotice('error', err)
      })
      getCodePublish().then(res => {
        this.configFormSelect.server_mode = res.data[0]['code_publish_setting']['server_mode']
        this.configFormSelect.jenkins_project = res.data[0]['code_publish_setting']['jenkins_project']
      }).catch(err => {
        sendNotice('error', err)
      })
    }
  },
  mounted () {
    this.refreshTabs()
    this.refresTabledata()
    this.refreshAppIp()
    this.refreshVarietyArgs()
  }
}
</script>
<style scoped>
/deep/ .ivu-form-item {
    margin-bottom: 18px;
    vertical-align: top;
    zoom: 1;
}
</style>
