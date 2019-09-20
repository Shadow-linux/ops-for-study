<template>
  <div>
    <Row>
      <Col span="24">
        <Card>
          <p slot="title">权限组</p>
          <Row>
            <Col span="24" >
              <Col span="2">
                <Button type="primary" size="small" style="margin-bottom: 10px"  ghost @click="addPermissionGroup">添加权限组</Button>
              </Col>
              <Col span="6" offset="16">
                <Input v-model="search" search placeholder="搜索权限组" @on-keyup.enter="searchWord" style=" margin-bottom: 10px"></Input>
              </Col>
            </Col>
            <Col span="24" >
              <Table :loading="tableLoading" ref="selection" :columns="tableColumns" :data="tableData"></Table>
            </Col>
          </Row>
        </Card>
      </Col>
    </Row>
    <Modal
        v-model="addGroupModalShow"
        title="添加用户组"
        @on-ok="ok"
        @on-cancel="cancel">
        <Form :label-width="70">
          <FormItem label="用户组名">
            <Input v-model="groupName"  />
          </FormItem>
        </Form>
    </Modal>
    <PagePermModal
    :pagePermModal="pagePermModal"
    :groupPermObj="groupPermObj"
    @switchPagePermModal="switchPagePermModal"
    ></PagePermModal>
    <UpdatePermModal
    :updatePermModal="updatePermModal"
    :mPagePermData="mPagePermData"
    @switchUpdatePermModal="switchUpdatePermModal"
    ></UpdatePermModal>
  </div>
</template>
<script>

import { PagePermModal, UpdatePermModal } from '_c/setting/permission_group'
import { getGroupPerm, getGroupList, addGroup, deleteGroup } from '@/api/setting/permission_group'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'setting_permissionGroup',
  components: {
    PagePermModal,
    UpdatePermModal
  },
  data () {
    return {
      tableLoading: false,
      mPagePermData: {},
      addGroupModalShow: false,
      groupName: '',
      pagePermModal: false,
      updatePermModal: false,
      search: '',
      groupPermObj: '',
      tableData: [],
      originTableData: [],
      tableColumns: [
        {
          title: '用户组',
          align: 'center',
          key: 'name',
          width: 150
        },
        {
          title: '关联用户',
          width: 300,
          render: (h, params) => {
            let renderList = []
            for (let idx in params.row.users) {
              let user = params.row.users[idx]['username']
              renderList.push(
                h('p', {}, user)
              )
            }
            return h('div', {}, renderList)
          }
        },
        {
          title: '页面权限',
          align: 'center',
          render: (h, params) => {
            return h('a', {
              on: {
                click: () => {
                  this.pagePermModal = true
                  getGroupPerm(params.row.id).then(res => {
                    console.log(res.data)
                    this.groupPermObj = res.data
                  }).catch(err => {
                    sendNotice('error', err)
                  })
                }
              }
            }, '查看')
          }
        },
        {
          title: '发布权限',
          align: 'center',
          render: (h, params) => {
            return h('a', {
              on: {
                click: () => {}
              }
            }, '查看')
          }
        },
        {
          title: '操作',
          align: 'center',
          render: (h, params) => {
            return h('span', {}, [
              h('a', {
                style: {
                  'margin-right': '10px'
                },
                on: {
                  click: () => {
                    getGroupPerm(params.row.id).then(res => {
                      this.mPagePermData = res.data
                    }).catch(err => {
                      sendNotice('error', err)
                    })
                    this.updatePermModal = true
                  }
                }
              }, '修改权限'),
              h('Poptip', {
                props: {
                  confirm: true,
                  title: 'Are you sure?',
                  'ok-text': 'yes',
                  'cancel-text': 'no',
                  'placement': 'left-end'
                },
                on: {
                  'on-ok': () => {
                    deleteGroup(params.row.id).then(res => {
                      this.$Message.success('删除用户组成功')
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
      ]
    }
  },
  methods: {
    ok () {
      if (this.groupName.trim().length === 0) {
        this.$Message.error('创建用户失败')
        return
      }
      addGroup({ 'name': this.groupName }).then(res => {
        this.$Message.success('创建用户组成功')
        this.reloadTable()
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    cancel () {
      this.groupName = ''
    },
    addPermissionGroup () {
      this.addGroupModalShow = true
    },
    switchPagePermModal (val) {
      this.pagePermModal = val
    },
    switchUpdatePermModal (val) {
      this.updatePermModal = val
    },
    searchWord () {
      var groupname = this.search.trim()
      if (groupname) {
        this.tableData = this.originTableData.filter(item => {
          if (item.name.indexOf(groupname) !== -1) {
            return item
          }
        })
      } else {
        this.tableData = this.originTableData
      }
    },
    reloadTable () {
      this.tableLoading = true
      getGroupList().then(res => {
        this.tableData = this.originTableData = res.data.reverse()
        this.tableLoading = false
      }).catch(err => {
        sendNotice('error', err)
        this.tableLoading = false
      })
    }
  },
  mounted () {
    this.reloadTable()
  }
}
</script>
<style  >
.ivu-poptip-confirm .ivu-poptip-body .ivu-icon {
  left: 18px;
}
</style>
