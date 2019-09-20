<template>
  <div>
    <Card>
      <div>
        <Row>
          <Col span="6">
            <Select v-model="monitorItem" style="width:250px" @on-change="monitorItemChange">
              <Option v-for="(value, key) in monitorItemList" :value="key" :key="key">{{ value }}</Option>
            </Select>
          </Col>
          <Col span="2" >
            <Button type="default" @click="goToStrategy">配置监控策略 >></Button>
          </Col>
          <Col span="1" offset="1">
            <Button type="default" @click="updateTPData" :loading="uTPLoading">更新数据</Button>
          </Col>
        </Row>
        <Divider > <b style="color: #909399">监控图表 [ {{ monitorItemList[monitorItem] }} ] </b> </Divider>
        <br>
        <div v-if="monitorItem == 'ecs'">
          <TPEcs :selectItem="selectMonitorItem"></TPEcs>
        </div>
        <div v-if="monitorItem == 'rds'">
          <TPRds :selectItem="selectMonitorItem"></TPRds>
        </div>
        <div v-if="monitorItem == 'nas'">
          <TPNas :selectItem="selectMonitorItem"></TPNas>
        </div>
        <div v-if="monitorItem == 'vpn'">
          <TPVpn :selectItem="selectMonitorItem"></TPVpn>
        </div>
        <div v-if="monitorItem == 'domain'">
          <TPDomain :selectItem="selectMonitorItem"></TPDomain>
        </div>
        <div v-if="monitorItem == 'yuexin_sms'">
          <TPYuexinSms :selectItem="selectMonitorItem"></TPYuexinSms>
        </div>
        <div v-if="monitorItem == 'xuncheng_eryaosu'">
          <TPXunchengEryaosu :selectItem="selectMonitorItem"></TPXunchengEryaosu>
        </div>
        <div v-if="monitorItem == 'wanweiyiyuan_bankid'">
          <TPWanweiyiyuanBankid :selectItem="selectMonitorItem"></TPWanweiyiyuanBankid>
        </div>
        <div v-if="monitorItem == 'tencent_sms'">
          <TPTencentSms :selectItem="selectMonitorItem"></TPTencentSms>
        </div>
      </div>
    </Card>
  </div>
</template>
<script>
import { updateTPData } from '@/api/monitor/third_party.js'
import { sendNotice } from '@/libs/util.js'
import {
  TPEcs,
  TPRds,
  TPNas,
  TPVpn,
  TPDomain,
  TPTencentSms,
  TPYuexinSms,
  TPWanweiyiyuanBankid,
  TPXunchengEryaosu
} from '_c/monitor/third_party'
import { monitorItemList } from '_c/monitor/third_party/vars.js'

export default {
  name: 'monitor_thirdparty',
  components: {
    TPEcs,
    TPRds,
    TPNas,
    TPVpn,
    TPDomain,
    TPTencentSms,
    TPYuexinSms,
    TPWanweiyiyuanBankid,
    TPXunchengEryaosu
  },
  data () {
    return {
      // ('ecs', 'rds', 'nas', 'domain', 'vpn', 'yuexin_sms', 'xuncheng_eryaosu', 'wanweiyiyuan_bankid', 'tencent_sms')
      monitorItemList: monitorItemList,
      monitorItem: 'ecs',
      selectMonitorItem: 'ecs',
      uTPLoading: false
    }
  },
  methods: {
    monitorItemChange (value) {
      console.log(value)
      this.selectMonitorItem = value
    },
    goToStrategy () {
      const route = {
        name: 'monitor_thirdPartyStrategy'
      }
      this.$router.push(route)
    },
    updateTPData () {
      this.uTPLoading = true
      updateTPData().then(res => {
        this.$Message.success('操作成功')
        this.uTPLoading = false
      }).catch(err => {
        sendNotice('error', err)
        this.uTPLoading = false
      })
    }
  }
}
</script>
<style scope>
</style>
