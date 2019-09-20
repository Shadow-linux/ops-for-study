<template>
  <div>
     <Row class="expand-row">
      <Col span="24">
        <b class="expand-key">创建时间: </b>
        <span>&nbsp;&nbsp;{{ row.created }}</span>
        <br><br>
        <b class="expand-key">进度条: </b>
        <Tooltip content="刷新时长：3min，频率：20s" placement="right">
          <Button type="default" v-show="ttButon" size="small" style="margin-left: 10px" @click="handleRTRefresh">实时刷新</Button>
          <Button type="default" v-show="!ttButon" size="small" style="margin-left: 10px" @click="stopRTRefresh">关闭刷新</Button>
        </Tooltip>
        <br><br>
        <Card>
          <Spin v-if="stepsSpin" size="large" fix></Spin>
          <Steps :current="stepsSize" size="small" :status="stepsStatus">
            <Step :title="item" :key="item" v-for="item in standerSteps"></Step>
          </Steps>
        </Card>
        <br>
        <b class="expand-key">日志信息: </b>
        <a :href="row.console_url" target="_blank">&nbsp;&nbsp;<Icon type="ios-log-out" style="font-size: 18px"/>
          {{ row.console_url }}
        </a>
        <br><br>
        <b class="expand-key">Ops版本号: </b>
        <span>&nbsp;&nbsp;{{ row.publish_version }}</span>
        <br><br>
        <b class="expand-key">分支: </b>
        <span>&nbsp;&nbsp;{{ row.branch }}</span>
        <br><br>
        <b class="expand-key">Git Log: </b>
        <span>&nbsp;&nbsp;{{ row.git_log }}</span>
        <br><br>
        <b class="expand-key">Jenkins Job / Build Num: </b>
        <span>&nbsp;&nbsp;{{ row.jenkins_job }} / {{ row.build_num }}</span>
        <br><br>
        <b class="expand-key">Jenkins Params: </b>
        <span>&nbsp;&nbsp;{{ row.jenkins_params }}</span>
        <br><br>
        <b class="expand-key">是否同步: </b>
        <span v-if="row.is_sync == 1">&nbsp;&nbsp;是</span>
        <span v-if="row.is_sync == 0">&nbsp;&nbsp;否</span>
        <br><br>
        <b class="expand-key">同步环境: </b>
        <span>&nbsp;&nbsp;{{ row.sync_env }}</span>
        <b class="expand-key" style="margin-left: 20px">同步IP: </b>
        <span>&nbsp;&nbsp;{{ row.sync_ip }}</span>
      </Col>
    </Row>
  </div>
</template>
<script>
import { getRealTimeSteps } from '@/api/code_publish/publish'
import { sendNotice } from '@/libs/util.js'
export default {
  name: 'publish_expand',
  props: {
    row: Object
  },
  data () {
    return {
      stepsSpin: false,
      stepsSize: this.row.steps_size,
      stepsStatus: this.row.steps_status,
      standerSteps: JSON.parse(this.row.stander_steps),
      tt: Object,
      ttButon: true
    }
  },
  methods: {
    stopRTRefresh () {
      clearInterval(this.tt)
      this.ttButon = true
    },
    handleRealTimeSteps () {
      getRealTimeSteps(this.row.id).then(res => {
        this.stepsSize = res.data['steps_size']
        this.stepsStatus = res.data['status']
        this.stepsSpin = false
      }).catch(err => {
        sendNotice('error', err)
        this.stepsSpin = false
      })
    },
    handleRTRefresh () {
      this.ttButon = false
      console.log(this.row)
      this.stepsSpin = true
      this.handleRealTimeSteps()
      this.tt = setInterval(() => {
        this.stepsSpin = true
        this.handleRealTimeSteps()
      }, 20000)
      setTimeout(() => {
        clearInterval(this.tt)
        this.ttButon = true
      }, 180000)
    }
  }
}
</script>
<style>
.expand-row{
  margin-bottom: 16px;
}
td.ivu-table-expanded-cell {
  padding: 20px 50px;
  background: #ffffff
}
</style>
