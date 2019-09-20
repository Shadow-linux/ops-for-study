<template>
  <div>
    <!-- <Affix :offset-top="110"> -->
      <Tabs style="backgroup-color: #fff" name="resource">
        <TabPane :label="labelEcs" tab="resource">
          <AliyunEcs></AliyunEcs>
        </TabPane>
        <TabPane :label="labelRds" tab="resource">
          <AliyunRds></AliyunRds>
        </TabPane>
      </Tabs>
    <!-- </Affix> -->
  </div>
</template>
<script>
import { AliyunEcs, AliyunRds } from '_c/cmdb/aliyun'
export default {
  name: 'cmdb_aliyun_resource',
  components: {
    AliyunEcs,
    AliyunRds
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
/deep/ .iconfont {
  font-family: "iconfont" !important;
  font-size: 13px;
  font-style: normal;
  -webkit-font-smoothing: antialiased;
  margin-right: 10px;
}
/deep/ .ivu-tabs .ivu-tabs-bar {
  border-bottom: 1px solid #dcdee2;
  margin-bottom: 0;
  outline: none;
}
</style>
