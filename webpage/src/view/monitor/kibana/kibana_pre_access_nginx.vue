<template>
  <div>
    <Card>
      <p slot="title">Pre Access Nginx 统计图 (24小时)</p>
      <iframe
      src="http://192.168.1.158:5601/goto/d4c0e1be70c255020eb20c7ab97bca5f"
      style="width: 100%;height: 800px;border: 0" ></iframe>
    </Card>
  </div>
</template>
<script>
export default {
  name: 'monitor_kibana_preAccessNginx'
}
</script>
