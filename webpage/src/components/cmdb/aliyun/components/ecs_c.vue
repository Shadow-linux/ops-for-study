<template>
  <div>
    <div style="">
      <Form @submit.native.prevent inline>
        <FormItem >
          <Input v-model.trim="searchValue" search placeholder="模糊搜索 [hostname|host|instance_id]" @on-keyup.enter="enterSearch" style="width: 300px" />
        </FormItem>
        <FormItem>
          <Dropdown @on-click="tagSearch" >
            <Button type="default" size="small">
              Tag
              <Icon type="ios-arrow-down"></Icon>
            </Button>
            <DropdownMenu slot="list">
              <DropdownItem :name="item.id" :key="item.id" v-for="item in tagList" >{{ item.tag_key }}</DropdownItem>
            </DropdownMenu>
          </Dropdown>
        </FormItem>
        <FormItem >
          <Dropdown @on-click="envSearch">
            <Button type="default" size="small">
              Env
              <Icon type="ios-arrow-down"></Icon>
            </Button>
            <DropdownMenu slot="list">
              <DropdownItem :name="item" :key="item" v-for="item in envNameList">{{ item }}</DropdownItem>
            </DropdownMenu>
          </Dropdown>
        </FormItem>
        <FormItem>
          <Dropdown @on-click="usedSearch" >
            <Button type="default" size="small">
              Used
              <Icon type="ios-arrow-down"></Icon>
            </Button>
            <DropdownMenu slot="list">
              <DropdownItem name="true">使用中</DropdownItem>
              <DropdownItem name="false">回收</DropdownItem>
            </DropdownMenu>
          </Dropdown>
        </FormItem>
        <FormItem style="float: right">
          <Dropdown @on-click="settingSet" >
            <Button type="default" size="small">
              <Icon type="ios-settings" style="font-size: 18px"></Icon>
            </Button>
            <DropdownMenu slot="list">
              <DropdownItem name="export">Export Data</DropdownItem>
            </DropdownMenu>
            <DropdownMenu slot="list">
              <DropdownItem name="aliyunUpdate">Aliyun update</DropdownItem>
            </DropdownMenu>
            <DropdownMenu slot="list">
              <DropdownItem name="ansibleUpdate" disabled>Ansible Update</DropdownItem>
            </DropdownMenu>
          </Dropdown>
        </FormItem>
        <FormItem style="float: right">
          <Button type="default" size="small" :loading="loading" @click="reloadTableList">刷新</Button>
        </FormItem>
      </Form>
    </div>
    <div style="margin-bottom: 15px">
      <Poptip
          confirm
          title="你确定要删除吗 ?"
          @on-ok="deleteOk"
          placement="top-start"
          style="margin-top: 5px">
          <Button size="small">Delete</Button>
      </Poptip>
      <Page :total="pageTotal" show-sizer show-total
      :page-size="pageSize"
      :page-size-opts="pageSizeOpts"
      @on-change="pageChange"
      @on-page-size-change="pageSizeChange"
      style="float: right"
      />
    </div>
    <Table ref="table" @on-select="tableSelect" @on-select-all="tableAllSelect" :loading="loading" :columns="tableColunms" :data="tableDatas" style="margin-bottom: 10px"></Table>
    <Modal
      v-model="editModal"
      title="修改 ECS 信息"
      @on-ok="editOk">
      <Form ref="editFrom" :model="editFrom" :label-width=100>
        <FormItem label="主机名" prop="hostname">
          <Input v-model="editFrom.hostname" placeholder=""></Input>
        </FormItem>
        <FormItem label="环境" prop="environment">
          <Select v-model="editFrom.environment">
            <Option v-for="item in envNameList" :value="item" :key="item">{{ item }}</Option>
          </Select>
        </FormItem>
        <FormItem label="使用/回收" prop="is_active">
          <Select v-model="editFrom.is_active">
            <Option value="true" >
              <Icon type="md-checkmark-circle-outline" style="font-size: 15px;color: #67C23A"/> 使用
            </Option>
            <Option value="false" >
              <Icon type="ios-remove-circle-outline" style="font-size: 15px; color: #F56C6C"/> 回收
            </Option>
          </Select>
        </FormItem>
        <FormItem label="SSH IP" prop="ssh_ip">
          <Input v-model.trim="editFrom.ssh_ip" placeholder=""></Input>
        </FormItem>
        <FormItem label="SSH Port" prop="ssh_port">
          <Input v-model.trim="editFrom.ssh_port" placeholder=""></Input>
        </FormItem>
        <FormItem label="Ansible" prop="is_ansible">
          <Select v-model="editFrom.is_ansible" placeholder="ops 不可达时选择'禁用'">
            <Option value="true" >
              <Icon type="md-checkmark-circle-outline" style="font-size: 15px;color: #67C23A"/>  激活
            </Option>
            <Option value="false" >
              <Icon type="ios-close-circle-outline" style="font-size: 15px; color: #F56C6C"/> 禁用
            </Option>
          </Select>
        </FormItem>
      </Form>
    </Modal>
    <Modal
      v-model="tagModal"
      width="650"
      title="编辑标签"
    >
      <Card style="height: 100px">
        <Tag  @on-close="tagClose"  :name="item.id" :key="item.id" closable v-for="item in choseTagList">{{ item.tag['tag_key'] }}: {{ item.tag['tag_value'] }}</Tag>
      </Card>
      <br>
      <Form inline :label-width=40 style="height: 40px">
        <FormItem label="绑定:">
          <Select v-model="choseTagId"  style="width:150px;"  filterable placeholder="选择已有 Tag">
            <Option v-for="item in tagList" :value="item.id" :key="item.id">{{ item.tag_key }}</Option>
          </Select>
        </FormItem>
        <FormItem :label-width=2>
          <Button type="primary" ghost size="small" @click="addTagRel">确定</Button>
        </FormItem>
      </Form>
    </Modal>
  </div>
</template>
<script>

import {
  updateEcsAllList,
  updateEcsInfo,
  deleteEcsInfo,
  getAliyunEcsTagsRel,
  getTagsList,
  deleteAliyunEcsTagRel,
  addAliyunEcsTagRel
  // ansibleUpdateAliyunEcs
} from '@/api/cmdb/aliyun/resource'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'aliyun_resource_ecs',
  components: {},
  props: [
    'presourceOriginDatas',
    'loading',
    'envNameList',
    'keyNameList'
  ],
  watch: {
    presourceOriginDatas () {
      this.orginTableDatas = this.presourceOriginDatas
      this.tableDatas = this.presourceOriginDatas
      this.pageTotal = this.tableDatas.length
      this.spliceTableDatas(1)
    }
  },
  data () {
    return {
      tagModal: false,
      pageTotal: 0,
      pageSize: 10,
      pageSizeOpts: [10, 50, 100, 200],
      searchValue: '',
      searchList: ['hostname', 'private_ip', 'public_ip', 'instance_id'],
      orginTableDatas: [],
      tableDatas: [],
      tagList: [],
      addTagKeyValue: {
        'tag_key': '',
        'tag_value': ''
      },
      choseTagId: '',
      choseTargetId: '',
      choseTagList: [],
      editModal: false,
      deleteDataList: [],
      editFrom: {
        'hostname': '',
        'environment': '',
        'is_active': '',
        'ssh_port': '',
        'ssh_ip': '',
        'id': '',
        'is_ansible': ''
      },
      tableColunms: [
        {
          type: 'selection',
          width: 50,
          align: 'center'
        },
        {
          title: '主机名/实例ID',
          minWidth: 150,
          render: (h, params) => {
            return h('p', {}, [
              h('p', {}, [
                h('a', {
                  on: {
                    click: () => {
                      let id = params.row.id
                      let hostname = params.row.hostname
                      let cmdb = 'aliyun'
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
              ]),
              h('p', {}, params.row.instance_id)
            ])
          }
        },
        {
          title: 'Tag',
          minWidth: 50,
          maxwidth: 90,
          render: (h, params) => {
            let tags = []
            params.row.tags.forEach(item => {
              tags.push(` ${item.tag_key}:${item.tag_value}`)
            })
            return h('span', {}, [
              h('Poptip', {
                'props': {
                  'placement': 'left',
                  'trigger': 'hover',
                  'content': tags.join(',')
                }
              }, [
                h('Icon', {
                  'props': {
                    'color': '#909399',
                    'type': 'md-pricetags'
                  },
                  'style': {
                    'font-size': '20px',
                    'cursor': 'pointer'
                  },
                  'on': {
                    click: () => {
                      this.choseTargetId = params.row.id
                      this.tagModal = true
                      getAliyunEcsTagsRel(params.row.id).then(res => {
                        this.choseTagList = res.data
                      }).catch(err => {
                        sendNotice('error', err)
                      })
                    }
                  }
                })
              ]),
              h('Poptip', {
                'props': {
                  'placement': 'left',
                  'trigger': 'hover',
                  'content': params.row.os_name
                }
              }, [
                h('Icon', {
                  'props': {
                    'type': params.row.os_type.startsWith('linux') ? 'logo-tux' : 'logo-windows'
                  },
                  'style': {
                    'font-size': '20px'
                  }
                })
              ])
            ])
          }
        },
        {
          'title': '监控',
          'width': 60,
          render: (h, params) => {
            return h('a', {
              'style': {
                'margin-right': '10px'
              },
              'on': {
                click: () => {
                  this.$router.push({ 'name': 'cmdb_aliyun_monitor' })
                }
              }
            }, [
              h('Icon', {
                'props': {
                  'type': 'md-pulse'
                },
                'style': {
                  'font-size': '18px'
                }
              })
            ])
          }
        },
        {
          'title': '环境',
          'key': 'environment',
          'minWidth': 80,
          'maxWidth': 120,
          'sortable': true
        },
        {
          'title': 'IP 地址',
          'maxWidth': 160,
          'minWidth': 100,
          render: (h, params) => {
            var publicIpArr = JSON.parse(params.row.public_ip)
            var privateIpArr = JSON.parse(params.row.private_ip)
            var publicIpArrRender = []
            var privateIpArrRender = []
            publicIpArr.forEach(element => {
              publicIpArrRender.push(
                h('p', {}, `${element} (公)`)
              )
            })
            privateIpArr.forEach(element => {
              privateIpArrRender.push(
                h('p', {}, `${element} (私有)`)
              )
            })
            return h('p', {}, [
              ...publicIpArrRender,
              ...privateIpArrRender
            ])
          }
        },
        {
          'title': '状态',
          'key': 'status',
          'sortable': true,
          'width': 95,
          render: (h, params) => {
            var status = params.row.status
            var icon = 'md-arrow-dropright-circle'
            var color = '#67C23A'
            var text = '运行中'
            if (status !== 'Running') {
              icon = 'ios-pause'
              color = '#F56C6C'
              text = '停止'
            }
            return h('p', {}, [
              h('Icon', {
                props: {
                  type: icon
                },
                style: {
                  'color': color,
                  'font-size': '20px',
                  'margin-right': '2px'
                }
              }),
              h('span', {
                style: {
                  'color': color,
                  'margin-top': '1px'
                }
              }, text)
            ])
          }
        },
        {
          'title': 'Used',
          'key': 'is_active',
          'width': 85,
          'sortable': true,
          render: (h, params) => {
            var status = params.row.is_active
            var icon = 'md-checkmark-circle-outline'
            var color = '#67C23A'
            if (!status) {
              icon = 'ios-remove-circle-outline'
              color = '#F56C6C'
            }
            return h('Icon', {
              props: {
                type: icon
              },
              style: {
                'color': color,
                'font-size': '20px'
              }
            })
          }
        },
        {
          'title': '配置',
          'width': 145,
          render: (h, params) => {
            let memory = params.row.memory / 1024
            let diskObj = JSON.parse(params.row.disk)
            let diskArrRender = []
            for (let idx in diskObj) {
              diskArrRender.push(
                h('p', {}, `${idx} ${diskObj[idx]} GiB`)
              )
            }
            return h('div', {
              'style': {
                'margin-bottom': '5px'
              }
            }, [
              h('p', {}, [
                h('span', {
                  'style': {
                    'margin-right': '5px'
                  }
                }, `${params.row.cpu} vCPU`),
                h('span', {}, `${memory} GiB`)
              ]),
              h('p', {}, params.row.instance_type),
              ...diskArrRender
            ])
          }
        },
        {
          'title': '过期时间',
          'sortable': true,
          'maxWidth': 150,
          'minWidth': 100,
          'key': 'expired_time'
        },
        {
          'title': '操作',
          // 'fixed': 'right',
          'maxWidth': 80,
          'minWidth': 50,
          'align': 'right',
          render: (h, params) => {
            return h('div', {}, [
              h('a', {
                on: {
                  click: () => {
                    this.editModal = true
                    this.editFrom.hostname = params.row.hostname
                    this.editFrom.environment = params.row.environment
                    this.editFrom.is_active = params.row.is_active.toString()
                    this.editFrom.ssh_port = params.row.ssh_port
                    this.editFrom.ssh_ip = params.row.ssh_ip
                    this.editFrom.id = params.row.id
                    this.editFrom.is_ansible = params.row.is_ansible.toString()
                  }
                }
              }, [
                h('Icon', {
                  props: {
                    'type': 'md-open'
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
    // addTagRel
    addTagRel () {
      this.tagList.forEach(item => {
        if (item.id === this.choseTagId) {
          let data = {
            'tag_id': this.choseTagId,
            'target_id': this.choseTargetId
          }
          addAliyunEcsTagRel(data).then(res => {
            this.$Message.success('操作成功')
            // 重载 choseTagList
            getAliyunEcsTagsRel(this.choseTargetId).then(res => {
              this.choseTagList = res.data
            })
            this.choseTagId = ''
          }).catch(err => {
            sendNotice('error', err)
          })
        }
      })
    },
    // tag 与 ecs 的记录id
    tagClose (event, id) {
      deleteAliyunEcsTagRel(id).then(res => {
        this.$Message.success('解除与tag的绑定')
        // 重刷一下tagList
        this.reloadTagList()
        let _array = []
        // 删除掉已经删除的tag
        this.choseTagList.forEach(item => {
          if (item.id !== id) {
            _array.push(item)
          }
        })
        this.choseTagList = _array
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    // delete
    tableDelete (data) {
      deleteEcsInfo(data.id).then(res => {
        this.$Message.success('删除成功 ' + data.hostname)
        var datas = []
        this.orginTableDatas.forEach(item => {
          if (item.id !== data.id) {
            datas.push(item)
          }
        })
        this.pageTotal = datas.length
        this.spliceTableDatas(1, datas)
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    // tableSelect
    tableSelect (data) {
      this.deleteDataList = data
    },
    tableAllSelect (data) {
      this.deleteDataList = data
    },
    // export data
    exportData () {
      var columns = []
      for (let idx in this.tableDatas[0]) {
        columns.push({
          'title': idx,
          'key': idx
        })
      }
      var datas = this.orginTableDatas.map(item => {
        let disk = []
        let diskObj = JSON.parse(item.disk)
        for (let idx in diskObj) {
          disk.push(`${idx}: ${diskObj[idx]}`)
        }
        let tags = []
        item.tags.forEach(it => {
          tags.push(` ${it.tag_key}:${it.tag_value}`)
        })
        let privateips = JSON.parse(item.private_ip).join(';')
        let publicips = JSON.parse(item.public_ip).join(';')
        item.private_ip = privateips
        item.public_ip = publicips
        item.disk = disk.join(';')
        item.tags = tags.join(';')
        return item
      })
      this.$refs.table.exportCsv({
        'filename': 'OpsEcsDatas',
        'columns': columns,
        'data': datas
      })
    },
    // spin show
    spinShow () {
      this.$Spin.show({
        render: (h) => {
          return h('div', [
            h('Icon', {
              'class': 'demo-spin-icon-load',
              props: {
                type: 'ios-loading',
                size: 18
              }
            }),
            h('div', 'Loading')
          ])
        }
      })
    },
    // settingSet
    settingSet (name) {
      if (name === 'export') {
        this.exportData()
      }
      switch (name) {
        case 'export':
          this.exportData()
          break
        case 'aliyunUpdate':
          this.spinShow()
          this.keyNameList.forEach(item => {
            updateEcsAllList({ 'key_name': item[0] }).then(res => {
              this.$Message.success('ECS更新完毕')
              this.$emit('reloadTable')
              this.$Spin.hide()
            }).catch(err => {
              sendNotice('error', err)
              this.$Spin.hide()
            })
          })
          break
        case 'ansibleUpdate':
          this.$Message.error('需解决网络问题后再重新开启, 联系"林浩"')
          // this.spinShow()
          // ansibleUpdateAliyunEcs({ 'cmdb': 'aliyun' }).then(res => {
          //   this.$Message.success('操作成功')
          //   this.$emit('reloadTable')
          //   this.$Spin.hide()
          // }).catch(err => {
          //   sendNotice('error', err)
          //   this.$Spin.hide()
          // })
          break
      }
    },
    // 更新aliyun 信息
    updateEcs () {
      this.refreshLoading = true
      this.keyNameList.forEach(item => {
        updateEcsAllList({ 'key_name': item[0] }).then(res => {
          this.$Message.success('ECS更新完毕')
          this.refreshLoading = false
          this.$emit('reloadTable')
        }).catch(err => {
          sendNotice('error', err)
          this.refreshLoading = false
        })
      })
    },
    // 标签搜索
    tagSearch (tagId) {
      this.tableDatas = []
      this.orginTableDatas.forEach(oitem => {
        let tagsList = oitem.tags
        tagsList.forEach(item => {
          if (item.id === tagId) {
            this.tableDatas.push(oitem)
          }
        })
      })
    },
    // 环境搜索
    envSearch (name) {
      this.search(name, ['environment'])
    },
    // 使用/回收 搜索
    usedSearch (name) {
      this.search(name, ['is_active'])
    },
    // input 搜索
    enterSearch () {
      if (this.searchValue === '') {
        this.spliceTableDatas(1, this.orginTableDatas)
        this.pageTotal = this.orginTableDatas.length
        return
      }
      this.search(this.searchValue, this.searchList)
    },
    // 基础搜索函数
    search (name, searchList) {
      this.tableDatas = []
      searchList.forEach(idx => {
        this.orginTableDatas.forEach(item => {
          if (item[idx].toString().indexOf(name) > -1) {
            this.tableDatas.push(item)
          }
        })
      })
      this.uniqTableDatas()
      this.pageTotal = this.tableDatas.length
      this.spliceTableDatas(1, this.tableDatas)
    },
    // 去重
    uniqTableDatas () {
      var hash = {}
      this.tableDatas = this.tableDatas.reduce((item, next) => {
        if (!hash[next.hostname]) {
          hash[next.hostname] = true
          item.push(next)
        }
        return item
      }, [])
    },
    pageSizeChange (pageSize) {
      this.pageSize = pageSize
      this.spliceTableDatas(1)
    },
    pageChange (page) {
      this.spliceTableDatas(page)
    },
    spliceTableDatas (page, otableDatas) {
      if (!otableDatas) {
        otableDatas = this.orginTableDatas
      }
      this.tableDatas = otableDatas.slice(page * this.pageSize - this.pageSize, page * this.pageSize)
    },
    deleteOk () {
      var deleteIdLIst = []
      this.deleteDataList.forEach(item => {
        this.tableDelete(item)
        deleteIdLIst.push(item.id)
      })
      this.deleteDataList = []
    },
    editOk () {
      this.editFrom.is_active = this.editFrom.is_active === 'true' ? 1 : 0
      this.editFrom.is_ansible = this.editFrom.is_ansible === 'true' ? 1 : 0
      updateEcsInfo(this.editFrom.id, this.editFrom).then(res => {
        this.$Message.success('修改成功.')
        // this.$emit('reloadTable')
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    reloadTableList () {
      this.$emit('reloadTable')
    },
    reloadTagList () {
      // 获取所有的tags
      getTagsList().then(res => {
        this.tagList = res.data
      }).catch(err => {
        sendNotice('error', err)
      })
    }
  },
  mounted () {
    this.reloadTagList()
  }
}
</script>
<style>
.demo-spin-icon-load{
  animation: ani-demo-spin 1s linear infinite;
}
</style>
