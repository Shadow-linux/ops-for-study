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
          <AliyunEcs
          :keyNameList="keyNameList"
          :envNameList="envNameList"
          :loading="loading"
          :presourceOriginDatas="resourceOriginDatas"
          @reloadTable="reloadTable"
          ></AliyunEcs>
        </Card>
      </Col>
    </Row>
  </div>
</template>
<script>

import AliyunEcs from './components/ecs_c.vue'
import { getCmdbInfo, getAccessKeyInfo, getClassfiyEcsInfo, getEcsInfo } from '@/api/cmdb/aliyun/resource'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'cmdb_aliyun_ecs',
  components: {
    AliyunEcs
  },
  data () {
    return {
      accessKeyName: '',
      loading: false,
      showMenu: '4',
      showCard: '20',
      showIcon: 'ios-arrow-dropleft-circle',
      envNameList: [],
      keyNameList: [],
      resourceOriginDatas: []
    }
  },
  methods: {
    menuSelector (name) {
      this.loading = true
      getClassfiyEcsInfo(name).then(res => {
        this.resourceOriginDatas = res.data
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
    },
    closeLoading () {
      this.loading = false
    },
    reloadTable () {
      this.loading = true
      getEcsInfo().then(res => {
        this.resourceOriginDatas = res.data
        this.loading = false
      }).catch(err => {
        sendNotice('error', err)
      })
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
  height: calc(100vh - 100px);
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
