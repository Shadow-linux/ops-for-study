<template>
  <div>
    <Alert type="info" show-icon>配置模版，用于发布配置。</Alert>
    <Row>
      <Col span="5">
        <Menu active-name="steps" class="menu-container" width="210" @on-select="menuSelector">
          <MenuGroup title="模版选择">
            <MenuItem name="steps">
              <Icon type="ios-code" size="18" />
              Steps
            </MenuItem>
            <MenuItem name="mvn_opts">
              <Icon type="ios-code" size="18" />
              Mvn opts
            </MenuItem>
            <MenuItem name="gradle_opts">
              <Icon type="ios-code" size="18" />
              Gradle opts
            </MenuItem>
            <MenuItem name="docker_opts">
              <Icon type="ios-code" size="18" />
              Docker opts
            </MenuItem>
            <MenuItem name="dockerfile">
              <Icon type="ios-code" size="18" />
              Dockerfile
            </MenuItem>
            <MenuItem name="java_opts">
              <Icon type="ios-code" size="18" />
              Java opts
            </MenuItem>
            <MenuItem name="jar_opts">
              <Icon type="ios-code" size="18" />
              Jar opts
            </MenuItem>
          </MenuGroup>
        </Menu>
      </Col>
      <Col span="19" >
        <Card class="menu-container">
          <p slot="title" style="color: #999; font-size:14px; font-weight: normal">{{ currentMenu }} 模版列表</p>
          <Steps v-if="currentMenu == 'steps'"></Steps>
          <MvnOpts v-if="currentMenu == 'mvn_opts'"></MvnOpts>
          <GradleOpts v-if="currentMenu == 'gradle_opts'"></GradleOpts>
          <JavaOpts v-if="currentMenu == 'java_opts'"></JavaOpts>
          <JarOpts v-if="currentMenu == 'jar_opts'"></JarOpts>
          <Dockerfile v-if="currentMenu == 'dockerfile'"></Dockerfile>
          <DockerOpts v-if="currentMenu == 'docker_opts'"></DockerOpts>
        </Card>
      </Col>
    </Row>
  </div>
</template>
<script>
import { MvnOpts, JavaOpts, JarOpts, Dockerfile, DockerOpts, Steps, GradleOpts } from '_c/code_publish/template'
export default {
  name: 'code_publish_template',
  data () {
    return {
      currentMenu: 'steps'
    }
  },
  components: {
    MvnOpts,
    JavaOpts,
    JarOpts,
    Dockerfile,
    DockerOpts,
    Steps,
    GradleOpts
  },
  methods: {
    menuSelector (name) {
      this.currentMenu = name
    }
  }
}
</script>
<style scoped>
.menu-container {
  padding-top: 0;
  overflow: auto;
  height: calc(100vh - 110px);
}
/deep/ .ivu-card-head {
    border-bottom: 1px solid #e8eaec;
    padding: 12px 16px;
    line-height: 1;
}
</style>
