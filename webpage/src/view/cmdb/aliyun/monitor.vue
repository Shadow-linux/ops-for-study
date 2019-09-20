<template>
  <div>
    <!-- <Affix :offset-top="110"> -->
      <Tabs name="monitor" >
        <TabPane :label="labelEcs" tab="monitor" class="setting-container">
          <AliyunMonitorEcs></AliyunMonitorEcs>
        </TabPane>
        <TabPane :label="labelRds" tab="monitor" class="setting-container">
          <AliyunMonitorRds></AliyunMonitorRds>
        </TabPane>
      </Tabs>
    <!-- </Affix> -->
  </div>
</template>
<script>
import { AliyunMonitorEcs, AliyunMonitorRds } from '_c/cmdb/aliyun'
export default {
  name: 'cmdb_aliyun_monitor',
  components: {
    AliyunMonitorEcs,
    AliyunMonitorRds
  },
  data () {
    return {
      labelRds: (h) => {
        return h('div', [
          h('i', {
            class: {
              'icon-RDS': true,
              'iconfont': true
            },
            'style': {
              'font-size': '14px'
            }
          }),
          h('span', {}, 'RDS')
        ])
      },
      labelEcs: (h) => {
        return h('div', [
          h('i', {
            class: {
              'icon-ecs': true,
              'iconfont': true
            },
            'style': {
              'font-size': '12px'
            }
          }),
          h('span', {}, 'ECS')
        ])
      }
    }
  }
}
</script>
<style scoped>
/* 为了vue页面样式模块化，不对全局造成污染，建议每个页面的style标签加上scoped，
表示他的样式只属于当前的页面，父组件的样式不会泄漏到子组件中。
但是scoped也会造成一些额外的负担，如无法覆盖原有组件的样式。 可以加 /deep/
*/
/deep/ .iconfont {
  font-family: "iconfont" !important;
  font-style: normal;
  -webkit-font-smoothing: antialiased;
  margin-right: 10px;
}
/deep/ .ivu-tabs-bar {
  border-bottom: 1px solid #dcdee2;
  margin-bottom: 0;
  outline: none;
}
.setting-container {
  overflow: auto;
  height: calc(100vh - 110px);
}
</style>
