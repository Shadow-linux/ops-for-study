<template>
  <div>
    <Row>
      <Col :span="showMenu">
        <Menu
          class="setting-container"
          width="210"
          @on-select="menuSelector">
          <MenuGroup title="资源">
            <Submenu name="key_name">
              <template slot="title">
                阿里云账户
              </template>
              <MenuItem :name="item[1]" v-for="item in keyNameList" :key="item[1]">
                <span class="select-title">{{ item[0] }}</span>
              </MenuItem>
            </Submenu>
            <Submenu name="env">
              <template slot="title">
                全局环境
              </template>
              <MenuItem :name="item" v-for="item in envNameList" :key="item">
                <span class="select-title">{{ item }}</span>
              </MenuItem>
            </Submenu>
          </MenuGroup>
        </Menu>
      </Col>
      <Col span="showCard">
        <Card class="setting-container">
          <a @click="switchMenu" class="show-icon"><Icon :type="showIcon" /></a>
          <br>
          <Form @submit.native.prevent inline>
            <FormItem>
              <Input v-model.trim="searchVal" placeholder="" @on-keyup.enter="enterSearch"  search style="width: 250px"></Input>
            </FormItem>
            <FormItem>
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
            <FormItem style="float: right">
              <Button type="default" size="small" :loading="loading" @click="reloadTable">刷新</Button>
            </FormItem>
          </Form>
          <Table :loading="loading" :columns="tableColumns" :data="tableDatas"></Table>
        </Card>
      </Col>
    </Row>
    <Modal
      v-model="tableModal"
      title="修改数据库信息"
      okText="保存"
      @on-ok="tableModalOk"
      >
      <Form :model="dataForm" :label-width="80">
        <FormItem label="环境: ">
          <Select v-model="dataForm.environment">
            <Option v-for="item in envNameList" :value="item" :key="item">{{ item }}</Option>
          </Select>
        </FormItem>
        <FormItem label="Used: ">
          <RadioGroup v-model="dataForm.is_active">
            <Radio label="true" style="color: #67C23A">
                <Icon type="md-checkmark-circle-outline"></Icon>
                <span>使用</span>
            </Radio>
            <Radio label="false" style="color: #F56C6C">
                <Icon type="ios-remove-circle-outline"></Icon>
                <span>回收</span>
            </Radio>
          </RadioGroup>
        </FormItem>
      </Form>
    </Modal>
  </div>
</template>
<script>
import { getAccessKeyInfo, getClassfiyRdsInfo, getCmdbInfo, getRdsInfo, updateRdsInfo } from '@/api/cmdb/aliyun/resource'
import { sendNotice } from '@/libs/util.js'
export default {
  name: 'cmdb_aliyun_rds',
  data () {
    return {
      searchList: ['instance_id', 'instance_desc'],
      searchVal: '',
      tableModal: false,
      loading: false,
      showMenu: '4',
      showCard: '20',
      showIcon: 'ios-arrow-dropleft-circle',
      keyNameList: [],
      dataForm: {
        'environment': '',
        'is_active': 'false'
      },
      editDataId: 0,
      originTableDatas: [],
      tableDatas: [],
      tableColumns: [
        {
          'title': '数据库名称',
          'width': 220,
          render: (h, params) => {
            return h('div', {}, [
              h('p', {}, params.row.instance_desc),
              h('p', {
                'style': {
                  'color': '#2d8cf0'
                }
              }, params.row.instance_id)
            ])
          }
        },
        {
          'title': '环境',
          'key': 'environment',
          'sortable': true,
          'width': 100
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
          'title': '运行状态',
          'key': 'status',
          'sortable': true,
          'width': 110,
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
          'title': '创建时间',
          'align': 'center',
          'key': 'create_time',
          'sortable': true,
          'width': 150
        },
        {
          'title': '过期时间',
          'align': 'center',
          'key': 'expire_time',
          'sortable': true,
          'width': 150
        },
        {
          'title': '操作',
          'align': 'right',
          render: (h, params) => {
            return h('a', {
              'on': {
                'click': () => {
                  this.tableModal = true
                  this.editDataId = params.row.id
                  this.dataForm.environment = params.row.environment
                  this.dataForm.is_active = params.row.is_active.toString()
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
          }
        }
      ],
      envNameList: []
    }
  },
  methods: {
    // 去重
    uniqTableDatas () {
      let hash = {}
      this.tableDatas = this.tableDatas.reduce((item, next) => {
        if (!hash[next.instance_id]) {
          hash[next.instance_id] = true
          item.push(next)
        }
        return item
      }, [])
    },
    enterSearch () {
      if (this.searchVal === '') {
        this.tableDatas = this.originTableDatas
        return
      }
      let tmpTableDatas = []
      this.searchList.forEach(searchIdx => {
        this.originTableDatas.forEach(item => {
          if (item[searchIdx].indexOf(this.searchVal) !== -1) {
            tmpTableDatas.push(item)
          }
        })
      })
      this.tableDatas = tmpTableDatas
      this.uniqTableDatas()
    },
    envSearch (name) {
      this.tableDatas = this.originTableDatas.filter(item => {
        if (item.environment === name) {
          return item
        }
      })
    },
    reloadTable () {
      this.loading = true
      getRdsInfo().then(res => {
        this.originTableDatas = this.tableDatas = res.data
        this.loading = false
      }).catch(err => {
        sendNotice('error', err)
        this.loading = false
      })
    },
    tableModalOk () {
      this.dataForm.is_active = this.dataForm.is_active === 'true' ? 1 : 0
      updateRdsInfo(this.editDataId, this.dataForm).then(res => {
        this.$Message.success('修改成功')
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    menuSelector (name) {
      this.loading = true
      getClassfiyRdsInfo(name).then(res => {
        this.originTableDatas = this.tableDatas = res.data
        console.log(this.originTableDatas)
        this.loading = false
      })
    },
    switchMenu () {
      if (this.showMenu === '0') {
        this.showMenu = '4'
        this.showCard = '20'
        this.showIcon = 'ios-arrow-dropleft-circle'
      } else {
        this.showMenu = '0'
        this.showCard = '24'
        this.showIcon = 'ios-arrow-dropright-circle'
      }
    }
  },
  mounted () {
    this.loading = true
    getCmdbInfo().then(res => {
      this.envNameList = res.data[0]['cmdb_setting']['base']['env']
      console.log(this.envNameList[0])
    }).catch(err => {
      sendNotice('error', err)
    })
    getAccessKeyInfo().then(res => {
      this.keyNameList = res.data.map(item => {
        return [item.key_name, item.id]
      })
    }).catch(err => {
      sendNotice('error', err)
    })
    this.reloadTable()
  }
}
</script>
<style scoped>
.select-title {
  font-size: 13px;
}
.ivu-menu-light {
  background-color: hsl(210, 10%, 92%);
}
.ivu-menu-light.ivu-menu-vertical .ivu-menu-item-active:not(.ivu-menu-submenu) {
  background-color: #ffffff;
}
.ivu-menu-light.ivu-menu-vertical .ivu-menu-item-active:not(.ivu-menu-submenu):after {
  background-color: #ffffff;
}
.setting-container {
  padding-top: 0;
  overflow: auto;
  height: calc(100vh - 110px);
}
.ivu-card-body {
  padding: 5px
}
.show-icon {
  color: #c5c8ce;
  font-size: 20px;
  position: relative;
  right: 15px;
  bottom: 20px;
}
.show-icon:hover {
  font-size: 23px
}
</style>
