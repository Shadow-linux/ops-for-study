<template>
  <div>
    <Row>
      <Col span="24">
        <Tabs type="card" size="small" :value="tabName" @on-click="addParams">
          <TabPane label="通用" name="common">
            <CmdbSettingCommon></CmdbSettingCommon>
          </TabPane>
          <TabPane label="阿里云" icon="ios-cloudy-outline" name="aliyun">
            <CmdbSettingAliyun></CmdbSettingAliyun>
          </TabPane>
          <TabPane label="腾讯云" icon="ios-cloudy-outline" name="tencent" disabled>Comming soon...</TabPane>
          <TabPane label="UCloud" icon="ios-cloudy-outline" name="ucloud" disabled>Comming soon ...</TabPane>
          <TabPane label="AWS" icon="ios-cloudy-outline" name="aws" disabled>Comming soon ...</TabPane>
        </Tabs>
      </Col>
    </Row>
  </div>
</template>
<script>

import { CmdbSettingCommon, CmdbSettingAliyun } from './cmdb_components'

export default {
  name: 'cmdb_setting',
  data () {
    return {
      tabName: 'common'
    }
  },
  components: {
    CmdbSettingCommon,
    CmdbSettingAliyun
  },
  methods: {
    addParams (name) {
      console.log(this.$route.query)
      this.$router.push({ 'name': 'setting_setting', 'query': { 'tab': name } })
    }
  },
  mounted () {
    if (this.$route.query.tab) {
      this.tabName = this.$route.query.tab
    }
  }
}
</script>
<style >
.ivu-tabs-tab {
  font-size: 13px;
}
</style>
