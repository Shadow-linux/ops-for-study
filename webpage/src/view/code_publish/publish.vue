<template>
  <div>
    <Task :taskModal="taskModal" @refreshTaskList="refreshTaskList" @switchTaskModal="switchTaskModal"></Task>
    <span class="demo-affix" @click="() => { drawerShow = true }"><Icon type="md-lock" style="font-size: 13px;"/> <b>环境锁</b></span>
      <EnvLock :pdrawerShow="drawerShow" @switchdrawerShow="switchdrawerShow"></EnvLock>
    <Card>
      <p slot="title" style="font-size: 13px; color: #909399">发布信息
      </p>
      <Row>
        <Col span="5" offset="">
          <Form inline>
            <FormItem>
              <Button icon="md-paper-plane" type="success" ghost @click="() => { taskModal = true }">
                发布 | 回滚
              </Button>
            </FormItem>
            <FormItem>
              <Poptip placement="right-start" :width="600"
               @on-popper-show="taskStatusShow"
               @on-popper-hide="taskStatusHide"
               >
                <Button type="info" icon="ios-timer-outline" ghost>待完成任务</Button>
                <div slot="content">
                  <Alert>自动刷新，间隔15s。
                    <div class="demo-spin-col" style="width: 10%; height: 10%; float: right; margin-top: 8px">
                      <Spin fix>
                        <Icon type="ios-loading" size=18 class="demo-spin-icon-load"></Icon>
                      </Spin>
                    </div>
                  </Alert>
                  <Table :columns="statusColumns" :data="statusDatas" :loading="statusTableLoading"></Table>
                </div>
              </Poptip>
            </FormItem>
          </Form>
        </Col>
        <Col span="2" offset="17">
          <Tooltip content="刷新发布列表, 频率: 60s" placement="left"  style="margin-left: 20px">
            <Button v-show="autoRefreshShow" type="default" @click="handleAutoRefreshBtnOn">自动刷新</Button>
            <Button v-show="!autoRefreshShow" type="default" @click="handleAutoRefreshBtnOff">关闭刷新</Button>
          </Tooltip>
        </Col>
      </Row>
      <Row>
        <Col span="2">
          <Form inline>
            <FormItem>
              <Dropdown  trigger="click" style="" @on-click="handleEnvChange">
              <Button type="primary" ghost>
                环境切换
                <Icon type="ios-arrow-down"></Icon>
              </Button>
              <DropdownMenu slot="list">
                  <DropdownItem v-for="env in envList" :key="env" :name="env">{{ env }}</DropdownItem>
              </DropdownMenu>
            </Dropdown>
            </FormItem>
          </Form>
        </Col>
        <Col span="2" offset="15">
          <Button type="default" style="margin-left: 10px"  icon="md-refresh" @click="() => {
            refreshTaskList()
          }" >刷新</Button>
        </Col>
        <Col span="5" >
          <Input v-model="searchVal" placeholder="App Name" search @on-keyup.enter="enterSearch"></Input>
        </Col>
      </Row>
      <Page :total="pageTotal"
        show-sizer show-total
        size="small"
        :page-size="pageSize"
        :page-size-opts="pageSizeOpts"
        :current="currentPage"
        @on-change="pageChange"
        @on-page-size-change="pageSizeChange"/>
      <br>
      <Table  ref="table" :columns="tableColumns" :loading="tableLoading" :data="tableDatas" @on-expand="handleExpand"></Table>
    </Card>
  </div>
</template>
<script>
import { Task, expandRow, EnvLock } from '_c/code_publish/publish'
import { getTasksList, getEnvs, updateTaskStatus, stopJenkinsBuild, getRealTimeTaskStatus, destroyPublishTask } from '@/api/code_publish/publish'
import { sendNotice } from '@/libs/util.js'
export default {
  name: 'code_publish_publish',
  components: {
    Task,
    expandRow,
    EnvLock
  },
  data () {
    return {
      envLockModalShow: false,
      drawerShow: false,
      taskModal: false,
      rollbackModal: false,
      searchVal: '',
      envList: ['ALL'],
      tableLoading: false,
      tableColumns: [
        {
          type: 'expand',
          width: 30,
          render: (h, params) => {
            return h(expandRow, {
              props: {
                row: params.row
              }
            })
          }
        },
        {
          title: '动作',
          sortable: true,
          key: 'action',
          width: 110,
          render: (h, params) => {
            let action
            let color
            switch (params.row.action) {
              case 'Deploy':
                action = '发布'
                color = 'green'
                break
              case 'Rollback':
                action = '回滚'
                color = 'red'
                break
              case 'DeploySync':
                action = '同步发布'
                color = 'cyan'
                break
              default:
                action = '未知'
                color = '#909399'
                break
            }
            return h('div', {}, [
              h('Tag', {
                props: {
                  color: color
                }
              }, action)
            ])
          }
        },
        {
          title: '应用名',
          key: 'app_name',
          width: 120
        },
        {
          title: '环境',
          key: 'env',
          width: 100,
          sortable: true,
          tooltip: true
        },
        {
          title: '发布IP',
          key: 'publish_ip',
          width: 120,
          tooltip: true
        },
        {
          title: 'ops版本 / 分支',
          render: (h, params) => {
            return h('div', {}, [
              h('p', {}, `版本: ${params.row.publish_version}`),
              h('p', {}, `分支: ${params.row.branch}`)
            ])
          }
        },
        {
          title: '发布者',
          key: 'creator',
          width: 130,
          tooltip: true,
          render: (h, params) => {
            return h('div', {}, [
              h('Tag', {
                props: {
                  type: 'border'
                }
              }, params.row.creator)
            ])
          }
        },
        {
          title: '更新时间',
          key: 'updated',
          align: 'center',
          width: 105,
          sortable: true
        },
        {
          title: '状态',
          align: 'center',
          width: 80,
          render: (h, params) => {
            // <Icon type="ios-water" />
            let error = '#F56C6C'
            let unknow = '#909399'
            let success = '#67C23A'
            let info = '#409EFF'
            let color
            let message
            switch (params.row.status) {
              case 1:
                color = success
                message = '发布成功'
                break
              case 2:
                color = error
                message = '发布失败'
                break
              case 3:
                color = info
                message = '执行中'
                break
              case 4:
                color = error
                message = '被终止'
                break
              default:
                color = unknow
                message = '未知/等待'
                break
            }
            return h('Tooltip', {
              props: {
                content: `${message}`,
                placement: 'left'
              }
            }, [
              h('Icon', {
                props: {
                  type: 'ios-radio-button-on'
                },
                style: {
                  'font-size': '20px',
                  'color': `${color}`
                }
              })
            ])
          }
        },
        {
          title: '操作',
          align: 'center',
          width: 120,
          render: (h, params) => {
            return h('div', {}, [
              h('Tooltip', {
                props: {
                  content: '终止发布',
                  placement: 'left'
                }
              }, [
                h('Icon', {
                  props: {
                    type: 'md-close'
                  },
                  style: {
                    'font-size': '20px',
                    'color': '#F56C6C',
                    'cursor': 'pointer'
                  },
                  on: {
                    click: () => {
                      this.tableLoading = true
                      this.$Message.info('发送 stop build 动作')
                      stopJenkinsBuild(params.row.id).then(res => {
                        this.$Message.success('停止build任务成功')
                        this.tableLoading = false
                      }).catch(err => {
                        sendNotice('error', err)
                        this.tableLoading = false
                      })
                    }
                  }
                })
              ]),
              h('Tooltip', {
                props: {
                  content: '删除该记录',
                  placement: 'left'
                }
              }, [
                h('Icon', {
                  props: {
                    type: 'md-trash'
                  },
                  style: {
                    'margin-left': '20px',
                    'font-size': '20px',
                    'color': '#909399',
                    'cursor': 'pointer'
                  },
                  on: {
                    click: () => {
                      destroyPublishTask(params.row.id).then(res => {
                        this.$Message.success('删除成功')
                        this.refreshTaskList()
                      }).catch(err => {
                        sendNotice('error', err)
                      })
                    }
                  }
                })
              ])
            ])
          }
        }
      ],
      tableDatas: [],
      tableOriginDatas: [],
      tmpTableOriginDatas: [],
      statusColumns: [
        {
          'title': 'App Name',
          key: 'app_name',
          width: 120
        },
        {
          'title': 'Env',
          key: 'env',
          width: 80
        },
        {
          'title': '发布IP',
          'key': 'publish_ip',
          width: 120
        },
        {
          'title': 'Branch',
          key: 'branch',
          tooltip: true
        },
        {
          title: '状态',
          align: 'center',
          width: 80,
          render: (h, params) => {
            // <Icon type="ios-water" />
            let error = '#F56C6C'
            let unknow = '#909399'
            let success = '#67C23A'
            let info = '#409EFF'
            let color
            let message
            switch (params.row.status) {
              case 1:
                color = success
                message = '发布成功'
                break
              case 2:
                color = error
                message = '发布失败'
                break
              case 3:
                color = info
                message = '执行中'
                break
              default:
                color = unknow
                message = '未知/等待'
                break
            }
            return h('Tooltip', {
              props: {
                content: `${message}`,
                placement: 'left'
              }
            }, [
              h('Icon', {
                props: {
                  type: 'ios-radio-button-on'
                },
                style: {
                  'font-size': '20px',
                  'color': `${color}`
                }
              })
            ])
          }
        }
      ],
      statusTableLoading: false,
      statusDatas: [],
      pageTotal: 0,
      pageSize: 10,
      pageSizeOpts: [10, 20, 50, 100],
      currentPage: 1,
      autoTaskRefreshTimer: Object,
      taskStatusTimer: Object,
      autoRefreshShow: true
    }
  },
  methods: {
    // 开关drawer
    switchdrawerShow (val) {
      this.drawerShow = val
    },
    handleAutoRefreshBtnOn () {
      // 定时发送整表更新
      this.autoRefreshShow = false
      this.refreshTaskList()
      this.autoTaskRefreshTimer = setInterval(() => {
        this.refreshTaskList()
      }, 30000)
    },
    handleAutoRefreshBtnOff () {
      clearInterval(this.autoTaskRefreshTimer)
      this.autoRefreshShow = true
    },
    enterSearch () {
      this.tableLoading = true
      if (!this.searchVal) {
        this.tableDatas = this.tableOriginDatas
        this.tableLoading = false
        return
      }
      this.tableDatas = this.tableOriginDatas.filter(item => {
        if (item.app_name.indexOf(this.searchVal) !== -1) {
          return item
        }
      })
      this.tableLoading = false
    },
    pageSizeChange (pageSize) {
      this.pageSize = pageSize
      this.spliceTableDatas(1, this.tableOriginDatas)
    },
    pageChange (page) {
      this.spliceTableDatas(page, this.tmpTableOriginDatas)
    },
    spliceTableDatas (page, originDatas) {
      this.tableDatas = originDatas.slice(page * this.pageSize - this.pageSize, page * this.pageSize)
    },
    handleTaskStatus () {
      getRealTimeTaskStatus().then(res => {
        this.statusDatas = res.data.reverse()
        this.statusTableLoading = false
      }).catch(err => {
        sendNotice('error', err)
        this.statusTableLoading = false
      })
    },
    taskStatusShow () {
      this.statusTableLoading = true
      this.handleTaskStatus()
      this.taskStatusTimer = setInterval(() => {
        this.statusTableLoading = true
        this.handleTaskStatus()
      }, 15000)
    },
    taskStatusHide () {
      clearInterval(this.taskStatusTimer)
    },
    handleExpand (row, status) {
      console.log(status)
      console.log(row)
    },
    switchTaskModal (val) {
      this.taskModal = val
    },
    refreshTaskList () {
      this.tableLoading = true
      this.currentPage = 1
      getTasksList().then(res => {
        this.tableOriginDatas = res.data
        this.tableDatas = res.data
        this.tmpTableOriginDatas = res.data
        this.pageTotal = res.data.length
        this.pageChange(1)
        this.tableLoading = false
      }).catch(err => {
        this.tableLoading = false
        sendNotice('error', err)
      })
    },
    handleEnvChange (env) {
      this.tableLoading = true
      this.tmpTableOriginDatas = []
      if (env !== 'ALL') {
        this.tableOriginDatas.forEach(item => {
          if (item.env === env) {
            this.tmpTableOriginDatas.push(item)
          }
        })
        this.pageTotal = this.tmpTableOriginDatas.length
        this.spliceTableDatas(1, this.tmpTableOriginDatas)
      } else if (env === 'ALL') {
        this.tmpTableOriginDatas = this.tableOriginDatas
        this.pageTotal = this.tableOriginDatas.length
        this.spliceTableDatas(1, this.tableOriginDatas)
      }
      this.tableLoading = false
    }
  },
  mounted () {
    this.handleTaskStatus()
    this.refreshTaskList()
    getEnvs().then(res => {
      this.envList = []
      res.data.forEach(item => {
        this.envList.push(item.env)
      })
    }).catch(err => {
      sendNotice('error', err)
    })
    // 定时发送刷新
    this.taskStatusTimer = setInterval(() => {
      updateTaskStatus().then(res => {
      }).catch(err => {
        sendNotice('error', '定时刷新发布状态失败')
        sendNotice('error', err)
      })
    }, 20000)
  },
  beforeDestroy () {
    clearInterval(this.taskStatusTimer)
    clearInterval(this.autoTaskRefreshTimer)
  }
}
</script>
<style scoped>
.demo-spin-col{
  height: 100px;
  position: relative;
}
.demo-spin-icon-load{
  animation: ani-demo-spin 1s linear infinite;
}
.ivu-alert {
  position: relative;
  padding: 8px 1px 8px 16px;
  border-radius: 4px;
  color: #515a6e;
  font-size: 12px;
  line-height: 16px;
  margin-bottom: 10px;
}
.demo-affix {
  border-top-left-radius: 25px;
  border-bottom-left-radius: 25px;
  top: 112px;
  right: calc(100% - 100%);
  width: 80px;
  position: fixed;
  z-index: 10;
  color: #fff;
  padding: 10px;
  text-align: center;
  background: #2db7f5;
  cursor: pointer;
}
.demo-affix:hover {
  width: 100px;
}
</style>
