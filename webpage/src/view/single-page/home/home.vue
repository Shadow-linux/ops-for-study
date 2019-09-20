<template>
  <div>
    <Card class="container">
      <Row>
        <Col span="5">
          <Card>
            <p slot="title" style="font-size: 13px; color: #909399" >运维工具</p>
            <Form>
              <FormItem label="SQL 审核平台:">
                <Tooltip content="http://sql-auditor.aiyuangong.com/#/login" placement="right">
                  <a href="http://sql-auditor.aiyuangong.com/#/login" target="_blank"><b><Icon type="ios-link" /> LINK</b></a>
                </Tooltip>
              </FormItem>
              <FormItem label="Open Falcon 后台:">
                <Tooltip content="http://192.168.1.158:8081/" placement="right">
                  <a href="http://192.168.1.158:8081/" target="_blank"><b><Icon type="ios-link" /> LINK</b></a>
                </Tooltip>
              </FormItem>
              <FormItem label="Urlooker 后台:">
                <Tooltip content="http://192.168.1.158:1984/auth/login" placement="right">
                  <a href="http://192.168.1.158:1984/auth/login" target="_blank"><b><Icon type="ios-link" /> LINK</b></a>
                </Tooltip>
              </FormItem>
              <FormItem label="ELK 后台:">
                <Tooltip content="http://192.168.1.158:5601/app/kibana" placement="right">
                  <a href="http://192.168.1.158:5601/app/kibana" target="_blank"><b><Icon type="ios-link" /> LINK</b></a>
                </Tooltip>
              </FormItem>
            </Form>
          </Card>
        </Col>
      </Row>
    </Card>
  </div>
</template>
<script>
export default {
  name: 'home'
}
</script>
<style scoped>
.container {
  padding-top: 0;
  height: calc(100vh - 110px);
}
/deep/ .ivu-form-item {
    margin-bottom: 5px;
    vertical-align: top;
    zoom: 1;
}
</style>
