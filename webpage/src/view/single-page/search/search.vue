<template>
  <div>
    <Card>
      <p slot="title">全局搜索</p>
      <h3>App 信息:</h3>
      <br>
      <Table :loading="tableLoading" :columns="appColumns" :data="appDatas"></Table>
      <br><br>
      <h3>Host 信息:</h3>
      <br>
      <Table :loading="tableLoading" :columns="hostColumns" :data="hostDatas"></Table>
    </Card>
  </div>
</template>
<script>
import { getGlobalSearch } from '@/api/no_perm.js'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'search',
  watch: {
    sval (newVal, oldVal) {
      this.reloadTable()
    }
  },
  computed: {
    sval () {
      return this.$store.state.app.globalSearchVal
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
    return {
      tableLoading: false,
      appColumns: [
        {
          'title': 'App 名',
          'key': 'app_name',
          'sortable': true,
          'width': 200,
          render: (h, params) => {
            let id = params.row.id
            let appName = params.row.app_name
            return h('a', {
              on: {
                click: () => {
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
            }, appName)
          }
        },
        {
          'title': 'App 端口',
          'key': 'port',
          'sortable': true,
          'width': 110
        },
        {
          'title': '使用中',
          'key': 'is_active',
          'sortable': true,
          'width': 100,
          render: (h, params) => {
            let check = params.row.is_active
            return checkIcon(h, check)
          }
        },
        {
          'title': '关联主机',
          'width': 450,
          'sortable': true,
          render: (h, params) => {
            let hostDict = params.row.hosts_dict
            let renderList = []
            Object.keys(hostDict).forEach(cmdb => {
              let hostsInfoList = hostDict[cmdb]
              for (let idx in hostsInfoList) {
                let hostObj = hostsInfoList[idx]
                let hostname = hostObj.hostname
                let privateIp = `（私）  ${hostObj.private_ip}`
                let publicIP = `（公）  ${hostObj.public_ip}`
                let env = hostObj.env
                renderList.push(
                  h('a', {
                    on: {
                      click: () => {
                        let id = hostObj.id
                        let cmdb = hostObj.cmdb
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
                  }, `【${cmdb} - ${env}】${hostname}`),
                  h('p', {}, privateIp),
                  h('p', {}, publicIP)
                )
              }
            })
            return h('div', {}, renderList)
          }
        },
        {
          'title': '服务类型',
          'key': 'server',
          'sortable': true,
          'width': 110
        },
        {
          'title': '描述',
          'key': 'desc'
        }
      ],
      hostColumns: [
        {
          'title': '主机名',
          'key': 'hostname',
          'sortable': true,
          'width': 350,
          render: (h, params) => {
            return h('a', {
              on: {
                click: () => {
                  let id = params.row.id
                  let hostname = params.row.hostname
                  let cmdb = params.row.cmdb
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
            }, params.row.hostname)
          }
        },
        {
          'title': 'IDC',
          'key': 'cmdb',
          'sortable': true
        },
        {
          'title': '环境',
          'sortable': true,
          'key': 'env'
        },
        {
          'title': '使用中',
          'key': 'is_active',
          'sortable': true,
          'width': 100,
          render: (h, params) => {
            let check = params.row.is_active
            return checkIcon(h, check)
          }
        },
        {
          'title': '私有IP',
          'key': 'private_ip'
        },
        {
          'title': '公有IP',
          'key': 'public_ip'
        },
        {
          'title': 'SSH',
          'width': 200,
          render: (h, params) => {
            return h('span', {}, `${params.row.ssh_ip}:${params.row.ssh_port}`)
          }
        }
      ],
      hostDatas: [],
      appDatas: []
    }
  },
  methods: {
    reloadTable () {
      if (!this.sval) { return }
      this.tableLoading = true
      getGlobalSearch(this.sval).then(res => {
        this.tableLoading = false
        this.hostDatas = res.data['hosts']
        this.appDatas = res.data['apps']
      }).catch(err => {
        this.tableLoading = false
        sendNotice('error', err)
      })
    }
  },
  mounted () {
    this.reloadTable()
  }
}
</script>
