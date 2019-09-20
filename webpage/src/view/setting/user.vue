<template>
  <div>
    <Row>
      <Col span="24">
        <Card :bordered="false">
          <p slot="title">
            用户管理
          </p>
          <Row>
            <Col span="24" >
              <Col span="2">
                <Button type="primary" size="small" style="margin-bottom: 10px"  ghost @click="createUser">添加用户</Button>
              </Col>
              <Col span="6" offset="16">
                <Input v-model="search" search placeholder="搜索用户名" @on-keyup.enter="searchUsername" style=" margin-bottom: 10px"></Input>
              </Col>
            </Col>
            <Col span="24" >
              <Table :loading="tableLoading" ref="selection" :columns="tableColumns" :data="tableData"></Table>
            </Col>
          </Row>
         </Card>
      </Col>
    </Row>
    <CreateModal :modalTitle="modalTtile"
    @switchUserModal="switchUserModal"
    @reloadTable="reloadTable"
    :groupList="groupList"
    :userModalShow="userModalShow">
    </CreateModal>
    <UpdateModal :updateModalObj="updateModalObj"  @reloadTable="reloadTable" :groupList="groupList" :updateModalShow="updateModalShow" @switchUpdateModal="switchUpdateModal" >
    </UpdateModal>
    <PwdModal :pwdModalShow="pwdModalShow" @switchPwdModalShow="switchPwdModalShow" :pwdObj="pwdObj" ></PwdModal>
  </div>
</template>
<script>

import { CreateModal, UpdateModal, PwdModal } from '_c/setting/user'
import { getUserList, getGroupList, deleteUser } from '@/api/setting/user'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'setting_user',
  components: {
    CreateModal,
    UpdateModal,
    PwdModal
  },
  data () {
    return {
      tableLoading: false,
      groupList: [],
      modalTtile: '创建用户',
      userModalShow: false,
      updateModalShow: false,
      updateModalObj: {},
      pwdModalShow: false,
      pwdObj: {},
      search: '',
      tableColumns: [
        {
          title: '用户',
          key: 'username',
          width: 150
        },
        {
          title: '姓名',
          key: 'real_name',
          width: 100
        },
        {
          title: '角色',
          key: 'role',
          align: 'center',
          render: (h, params) => {
            return h('span', {}, this.getUserRole(params))
          }
        },
        {
          title: '权限组',
          key: 'group',
          render: (h, params) => {
            if (params.row.groups.length !== 0) {
              return h('span', {}, params.row.groups[0]['name'])
            }
          }
        },
        {
          title: '部门',
          key: 'department'
        },
        {
          title: '岗位',
          key: 'position'
        },
        {
          title: '邮箱',
          key: 'email'
        },
        {
          title: '操作',
          key: 'operation',
          width: 200,
          align: 'center',
          render: (h, params) => {
            return h('div', {}, [
              h('a', {
                style: {
                  'margin-right': '10px'
                },
                on: {
                  click: () => {
                    this.updateModalShow = true
                    var group
                    var role
                    if (params.row.groups.length !== 0) {
                      group = params.row.groups[0]['name']
                    }
                    role = this.getUserRole(params)
                    this.updateModalObj = {
                      id: params.row.id,
                      username: params.row.username,
                      real_name: params.row.real_name,
                      role: role,
                      group: group,
                      department: params.row.department,
                      email: params.row.email,
                      position: params.row.position,
                      mobile: params.row.mobile
                    }
                  }
                }
              }, '修改'),
              h('a', {
                style: {
                  'margin-right': '10px'
                },
                on: {
                  click: () => {
                    this.pwdModalShow = true
                    this.pwdObj = {
                      'id': params.row.id,
                      'username': params.row.username
                    }
                  }
                }
              }, '更改密码'),
              h('Poptip', {
                props: {
                  confirm: true,
                  title: 'Are you sure?',
                  'ok-text': 'yes',
                  'cancel-text': 'no ',
                  'placement': 'left-end'
                },
                on: {
                  'on-ok': () => {
                    deleteUser(params.row.id).then(res => {
                      this.$Message.success('删除用户成功')
                      this.reloadTable()
                    }).catch(err => {
                      sendNotice('error', err)
                    })
                  }
                }
              }, [
                h('a', {
                  style: {
                    'color': '#c5c8ce'
                  }
                }, '删除')
              ])
            ])
          }
        }
      ],
      tableData: [],
      fullData: []
    }
  },
  methods: {
    handleSelectAll (status) {
      this.$refs.selection.selectAll(status)
    },
    createUser () {
      this.userModalShow = true
    },
    switchUserModal (val) {
      this.userModalShow = val
    },
    switchUpdateModal (val) {
      this.updateModalShow = val
    },
    switchPwdModalShow (val) {
      this.pwdModalShow = val
    },
    getUserRole (params) {
      var staff = params.row.is_staff
      var admin = params.row.is_superuser
      if (admin) return '管理员'
      if (staff) return '普通用户'
      return 'Guest'
    },
    searchUsername () {
      var username = this.search.trim()
      if (username) {
        this.tableData = this.fullData.filter(item => {
          if (item.username.indexOf(username) !== -1) {
            return item
          }
        })
      } else {
        this.tableData = this.fullData
      }
    },
    reloadTable () {
      this.tableLoading = true
      getUserList().then(res => {
        this.tableData = res.data.reverse()
        this.tableLoading = false
      }).catch(err => {
        sendNotice('error', err)
        this.tableLoading = false
      })
    }
  },
  mounted () {
    getUserList().then(res => {
      console.log(res.data)
      this.tableData = this.fullData = res.data.reverse()
    }).catch(err => {
      sendNotice('error', err)
    })
    getGroupList().then(res => {
      this.groupList = res.data
    }).catch(err => {
      sendNotice('error', err)
    })
  }
}
</script>
<style  >
.ivu-poptip-confirm .ivu-poptip-body .ivu-icon {
  left: 18px;
}
</style>
