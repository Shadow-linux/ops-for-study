<template>
  <div>
    <div style="">
      <Form @submit.native.prevent inline>
        <FormItem >
          <Input v-model.trim="searchValue" search placeholder="模糊搜索 [hostname|ip]" @on-keyup.enter="enterSearch" style="width: 300px" />
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
              <DropdownItem name="true">
                <Icon type="md-checkmark-circle-outline" style="font-size: 15px;color: #67C23A"/> 使用中
              </DropdownItem>
              <DropdownItem name="false">
                <Icon type="ios-remove-circle-outline" style="font-size: 15px; color: #F56C6C"/> 回收
              </DropdownItem>
            </DropdownMenu>
          </Dropdown>
        </FormItem>
        <FormItem style="float: right">
          <Dropdown @on-click="settingSet" >
            <Button type="default" size="small">
              <Icon type="ios-settings" style="font-size: 18px"></Icon>
            </Button>
            <DropdownMenu slot="list">
              <DropdownItem name="ansibleUpdate">Ansible Update</DropdownItem>
            </DropdownMenu>
            <DropdownMenu slot="list">
              <DropdownItem name="export">Export Data</DropdownItem>
            </DropdownMenu>
          </Dropdown>
        </FormItem>
        <FormItem style="float: right">
          <Dropdown @on-click="addDropdown">
            <Button type="default" size="small">
              添加 <Icon type="ios-arrow-down"></Icon>
            </Button>
            <DropdownMenu slot="list">
              <DropdownItem name="autoAdd">
                自动添加 <Tag color="red" style="margin-left: 5px; font-size: 12px">推荐</Tag>
              </DropdownItem>
              <DropdownItem name="manualAdd">
                手动添加
              </DropdownItem>
            </DropdownMenu>
          </Dropdown>
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
      :title="editModalTitle"
      @on-ok="editOk('editFrom')"
      :mask-closable="false">
      <Alert type="warning" show-icon>以下信息需要完整填写。</Alert>
      <Form ref="editFrom" :model="editFrom" :rules="ruleEditForm" :label-width=100>
        <FormItem label="主机名" prop="hostname">
          <Input v-model="editFrom.hostname" placeholder=""></Input>
        </FormItem>
        <FormItem label="环境" prop="environment">
          <Select v-model="editFrom.environment">
            <Option v-for="item in envNameList" :value="item" :key="item">{{ item }}</Option>
          </Select>
        </FormItem>
        <FormItem label="IDC" prop="idc">
           <Select v-model="editFrom.idc">
            <Option v-for="item in idcList" :value="item" :key="item">{{ item }}</Option>
          </Select>
        </FormItem>
        <FormItem label="CPU" prop="cpu">
          <Input  v-model="editFrom.cpu" style="width: 100%">
          </Input>
        </FormItem>
        <FormItem label="内存 (MiB)" prop="memory">
          <Input v-model="editFrom.memory" style="width: 100%">
            <span slot="append">MiB</span>
          </Input>
        </FormItem>
        <FormItem label="Swap (MiB)" prop="swap">
          <Input v-model="editFrom.swap" style="width: 100%">
          <span slot="append">MiB</span>
          </Input>
        </FormItem>
        <FormItem label="Disk" prop="disk">
          <Input v-model.trim="editFrom.disk" placeholder='需要为JSON格式 {"/dev/sda": "557.75", "/dev/sdb": "100"}'></Input>
        </FormItem>
        <FormItem label="公网" prop="public_ip">
          <Input v-model.trim="editFrom.public_ip" placeholder='需要为JSON格式 ["1.1.1.1", "2.2.2.2"]'></Input>
        </FormItem>
        <FormItem label="私有网" prop="private_ip">
          <Input v-model.trim="editFrom.private_ip" placeholder='需要为JSON格式 ["1.1.1.1", "2.2.2.2"]'></Input>
        </FormItem>
        <FormItem label="操作系统" prop="os_name">
          <Input v-model.trim="editFrom.os_name" placeholder=""></Input>
        </FormItem>
        <FormItem label="系统类型" prop="os_type">
          <Input v-model.trim="editFrom.os_type" placeholder=""></Input>
        </FormItem>
        <FormItem label="序列号" prop="serial_number">
          <Input v-model.trim="editFrom.serial_number" placeholder=""></Input>
        </FormItem>
        <FormItem label="运行状态" prop="status">
          <Select v-model="editFrom.status">
            <Option value="Running" >
              <Icon type="md-arrow-dropright-circle" style="font-size: 15px;color: #67C23A" /> 运行中
            </Option>
            <Option value="Stopped" >
              <Icon type="md-pause" style="font-size: 15px; color: #F56C6C"/> 停止
            </Option>
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
        <FormItem label="SSH IP" prop="ssh_ip">
          <Input v-model.trim="editFrom.ssh_ip" placeholder=""></Input>
        </FormItem>
        <FormItem label="SSH Port" prop="ssh_port">
          <Input v-model="editFrom.ssh_port" placeholder=""></Input>
        </FormItem>
        <FormItem label="描述" prop="description">
          <Input v-model.trim="editFrom.description" placeholder=""></Input>
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
    <Modal
      v-model="autoAddModal"
      title="自动添加"
      :mask-closable="false"
      @on-ok="autoAddConfirm('autoAddForm')"
      >
      <Alert type="warning" show-icon>请确保ops平台服务器可以通过使用key远程登录到被添加的服务器</Alert>
      <Form ref="autoAddForm" :model="autoAddForm" :rules="ruleAutoAddForm" :label-width=90>
        <FormItem label="IDC:" prop="uniq">
          <Select v-model="autoAddForm.uniq">
            <Option v-for="item in idcList" :value="item" :key="item">{{ item }}</Option>
          </Select>
        </FormItem>
        <FormItem label="SSH IP:" prop="ssh_ip">
          <Input v-model="autoAddForm.ssh_ip" placeholder=""></Input>
        </FormItem>
        <FormItem label="SSH PORT:" prop="ssh_port">
          <Input v-model="autoAddForm.ssh_port" placeholder=""></Input>
        </FormItem>
      </Form>
    </Modal>
  </div>
</template>
<script>

import {
  updateNativeHostInfo,
  addNativeHostInfo,
  addNativeHostTagRel,
  getNativeHostTagRel,
  deleteNativeHostInfo,
  getTagsList,
  deleteTagRel,
  ansibleUpdateNativeHost,
  ansibleAutoAddNativeHost
} from '@/api/cmdb/native/resource'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'native_resource_main',
  components: {},
  props: [
    'presourceOriginDatas',
    'loading',
    'envNameList',
    'idcList'
  ],
  watch: {
    presourceOriginDatas () {
      this.orginTableDatas = this.presourceOriginDatas
      console.log(this.orginTableDatas)
      this.tableDatas = this.presourceOriginDatas
      this.pageTotal = this.tableDatas.length
      this.spliceTableDatas(1)
    }
  },
  data () {
    const validateIp = (rule, value, callback) => {
      try {
        let valueArr = JSON.parse(value)
        if (typeof valueArr !== 'object') {
          callback(new Error('请输入 JSON 格式, 如 ["1.1.1.1", "2.2.2.2"]'))
        }
        callback()
      } catch (err) {
        callback(new Error('请输入 JSON 格式, 如 ["1.1.1.1", "2.2.2.2"]'))
      }
    }
    const validateDisk = (rule, value, callback) => {
      try {
        let valueArr = JSON.parse(value)
        if (typeof valueArr !== 'object') {
          callback(new Error('请输入 JSON 格式, 如  {"/dev/sda": "557.75", "/dev/sdb": "100"}'))
        }
        JSON.parse(value)
        callback()
      } catch (err) {
        callback(new Error('请输入 JSON 格式, 如 {"/dev/sda": "557.75", "/dev/sdb": "100"}'))
      }
    }
    return {
      autoAddForm: {
        cmdb: 'native',
        uniq: '',
        ssh_ip: '',
        ssh_port: ''
      },
      ruleAutoAddForm: {
        uniq: [
          { required: true, message: '不能为空', trigger: 'change' }
        ],
        ssh_ip: [
          { required: true, message: '不能为空', trigger: 'blur' }
        ],
        ssh_port: [
          { required: true, message: '不能为空', trigger: 'blur' }
        ]
      },
      ruleEditForm: {
        hostname: [
          { required: true, message: '不能为空', trigger: 'blur' }
        ],
        environment: [
          { required: true, message: '不能为空', trigger: 'change' }
        ],
        idc: [
          { required: true, message: '不能为空', trigger: 'change' }
        ],
        public_ip: [
          { required: true, validator: validateIp, trigger: 'blur' }
        ],
        private_ip: [
          { required: true, validator: validateIp, trigger: 'blur' }
        ],
        disk: [
          { required: true, validator: validateDisk, trigger: 'blur' }
        ],
        os_name: [
          { required: true, message: '不能为空', trigger: 'blur' }
        ],
        os_type: [
          { required: true, message: '不能为空', trigger: 'blur' }
        ],
        serial_number: [
          { required: true, message: '不能为空', trigger: 'blur' }
        ],
        status: [
          { required: true, message: '不能为空', trigger: 'change' }
        ],
        is_active: [
          { required: true, message: '不能为空', trigger: 'change' }
        ],
        is_ansible: [
          { required: true, message: '不能为空', trigger: 'change' }
        ],
        ssh_ip: [
          { required: true, message: '不能为空', trigger: 'blur' }
        ],
        description: [
          { required: true, message: '不能为空', trigger: 'blur' }
        ]
      },
      autoAddModal: false,
      tagModal: false,
      pageTotal: 0,
      pageSize: 10,
      pageSizeOpts: [10, 50, 100, 200],
      searchValue: '',
      searchList: ['hostname', 'private_ip', 'public_ip'],
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
      currentEditModalAction: '',
      deleteDataList: [],
      editModalTitle: '',
      editFrom: {
        'hostname': '',
        'environment': '',
        'is_active': '',
        'cpu': 0,
        'memory': 0,
        'swap': 0,
        'ssh_port': '',
        'ssh_ip': '',
        'id': '',
        'idc': '',
        'public_ip': '[]',
        'private_ip': '[]',
        'serial_number': '',
        'os_type': '',
        'os_name': '',
        'status': 'Running',
        'description': 'none',
        'is_ansible': '',
        'disk': ''
      },
      tableColunms: [
        {
          type: 'selection',
          width: 45,
          align: 'center'
        },
        {
          title: '主机名/SN',
          minWidth: 150,
          render: (h, params) => {
            return h('p', {}, [
              h('p', {}, [
                h('a', {
                  on: {
                    click: () => {
                      let id = params.row.id
                      let hostname = params.row.hostname
                      let cmdb = 'native'
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
              h('p', {}, params.row.serial_number)
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
                      getNativeHostTagRel(params.row.id).then(res => {
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
                    'font-size': '20px',
                    'color': '#909399'
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
                  this.$router.push({ 'name': 'cmdb_native_monitor' })
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
            let memory = parseInt(params.row.memory / 1024)
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
          'title': '更新时间',
          'sortable': true,
          'maxWidth': 150,
          'minWidth': 100,
          'key': 'updated'
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
                    this.currentEditModalAction = 'edit'
                    this.editModal = true
                    this.editModalTitle = '编辑 Host 信息'
                    this.editFrom = params.row
                    console.log(params.row.is_active.toString())
                    this.editFrom.is_active = params.row.is_active.toString()
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
    // autoAddConfirm
    autoAddConfirm (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          this.spinShow()
          ansibleAutoAddNativeHost(this.autoAddForm).then(res => {
            this.$Message.success('操作成功')
            this.$emit('reloadTable')
            this.$Spin.hide()
          }).catch(err => {
            sendNotice('error', err)
            this.$Spin.hide()
          })
        } else {
          this.$Message.error('操作失败')
        }
      })
    },
    // addDropDown
    addDropdown (name) {
      if (name === 'manualAdd') {
        this.currentEditModalAction = 'add'
        this.editModalTitle = '添加 Host 信息'
        this.editModal = true
        for (let key in this.editFrom) {
          this.editFrom[key] = ''
        }
        this.editFrom.description = 'none'
        return
      }
      if (name === 'autoAdd') {
        this.autoAddModal = true
      }
    },
    // addTagRel
    addTagRel () {
      this.tagList.forEach(item => {
        if (item.id === this.choseTagId) {
          let data = {
            'tag_id': this.choseTagId,
            'target_id': this.choseTargetId
          }
          addNativeHostTagRel(data).then(res => {
            this.$Message.success('操作成功')
            // 重载 choseTagList
            getNativeHostTagRel(this.choseTargetId).then(res => {
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
      deleteTagRel(id).then(res => {
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
      deleteNativeHostInfo(data.id).then(res => {
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
      switch (name) {
        case 'export':
          this.exportData()
          break
        case 'ansibleUpdate':
          this.spinShow()
          ansibleUpdateNativeHost({ 'cmdb': 'native' }).then(res => {
            this.$Message.success('操作成功')
            this.$emit('reloadTable')
            this.$Spin.hide()
          }).catch(err => {
            sendNotice('error', err)
            this.$Spin.hide()
          })
          break
      }
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
        if (!hash[next.id]) {
          hash[next.id] = true
          item.push(next)
        }
        return item
      }, [])
      console.log(this.tableDatas)
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
    editOk (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          this.editFrom.is_active = this.editFrom.is_active === 'true' ? 1 : 0
          this.editFrom.is_ansible = this.editFrom.is_ansible === 'true' ? 1 : 0
          switch (this.currentEditModalAction) {
            case 'add':
              addNativeHostInfo(this.editFrom).then(res => {
                this.$Message.success('操作成功.')
                this.$emit('reloadTable')
              }).catch(err => {
                sendNotice('error', err)
              })
              break
            case 'edit':
              updateNativeHostInfo(this.editFrom.id, this.editFrom).then(res => {
                this.$Message.success('操作成功.')
                this.$emit('reloadTable')
              }).catch(err => {
                sendNotice('error', err)
              })
              break
          }
        } else {
          this.$Message.error('操作失败!')
        }
      })
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
