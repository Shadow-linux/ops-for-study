<template>
  <div>
    <Alert show-icon><b>基础策略：</b>用于监控最新数值与策略相符则进行告警; &nbsp;&nbsp;<b>抖动策略：</b>用于(指定时间点的数值 - 最新数值)与策略相符则进行告警。</Alert>
    <Card>
      <Tabs size="small">
        <TabPane label="基础策略" icon="md-list-box">
          <TPBaseStrategy></TPBaseStrategy>
        </TabPane>
        <TabPane label="抖动策略" icon="md-list-box">
          <TPJitterStrategy></TPJitterStrategy>
        </TabPane>
    </Tabs>
    </Card>
  </div>
</template>
<script>
import { TPBaseStrategy, TPJitterStrategy } from '_c/monitor/third_party'

export default {
  name: 'monitor_thirdPartyStrategy',
  components: {
    TPBaseStrategy,
    TPJitterStrategy
  }
}
</script>
