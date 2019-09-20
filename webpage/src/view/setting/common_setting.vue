<template>
  <div >
      <!-- <p slot="title">通用设置</p> -->
      <Alert show-icon closable>全站的所有设置都从这里可以找到...</Alert>
      <Row>
        <Col :span="showMenu">
          <Menu active-name="cmdbSetting"
            class="setting-container"
            width="210"
            @on-select="menuSelector">
            <MenuGroup title="通用设置">
              <MenuItem name="baseSetting">
                <Icon type="ios-keypad" />
                <span class="select-title">基础设置</span>
              </MenuItem>
              <MenuItem name="cmdbSetting">
                <Icon type="logo-buffer" />
                <span class="select-title">CMDB设置</span>
              </MenuItem>
              <MenuItem name="appSetting">
                <Icon type="ios-appstore-outline" />
                <span class="select-title">APP设置</span>
              </MenuItem>
              <MenuItem name="publishSetting">
                <Icon type="ios-code-working" />
                <span class="select-title">代码发布设置</span>
              </MenuItem>
              <MenuItem name="messageSetting">
                <Icon type="ios-mail-open" />
                <span class="select-title">消息设置</span>
              </MenuItem>
            </MenuGroup>
          </Menu>
        </Col>
        <Col span="showCard">
          <Card class="setting-container">
            <a @click="switchMenu" class="show-icon"><Icon :type="showIcon" /></a>
            <MessageSetting v-show="selectObj.messageSetting"></MessageSetting>
            <b v-show="selectObj.baseSetting">Coming soon...</b>
            <CmdbSetting v-show="selectObj.cmdbSetting"></CmdbSetting>
            <AppSetting v-show="selectObj.appSetting"></AppSetting>
            <PublishSetting v-show="selectObj.publishSetting"></PublishSetting>
          </Card>
        </Col>
      </Row>
  </div>
</template>
<script>

import { MessageSetting, CmdbSetting, AppSetting, PublishSetting } from '_c/setting/common_setting'

export default {
  name: 'setting_setting',
  data () {
    return {
      showMenu: '4',
      showCard: '20',
      showIcon: 'ios-arrow-dropleft-circle',
      selectObj: {
        messageSetting: false,
        baseSetting: false,
        cmdbSetting: true,
        appSetting: false,
        publishSetting: false
      }
    }
  },
  components: {
    MessageSetting,
    CmdbSetting,
    AppSetting,
    PublishSetting
  },
  methods: {
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
    menuSelector (name) {
      for (var key in this.selectObj) {
        if (key === name) {
          this.selectObj[key] = true
        } else {
          this.selectObj[key] = false
        }
      }
    }
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
  height: calc(100vh - 130px);
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
