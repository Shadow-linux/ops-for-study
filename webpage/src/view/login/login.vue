<style lang="less">
  @import './login.less';
</style>

<template>
  <div class="login">
    <div class="login-con">
      <Card icon="log-in" title="欢迎登录 Ops" :bordered="false">
        <div class="form-con">
          <login-form :loginBtnLoading="loginBtnLoading" @on-success-valid="handleSubmit"></login-form>
          <p class="login-tip">v1.0.0</p>
        </div>
      </Card>
    </div>
  </div>
</template>

<script>
import LoginForm from '_c/login-form'
import { mapActions } from 'vuex'
import { sendNotice } from '@/libs/util.js'

export default {
  components: {
    LoginForm
  },
  data () {
    return {
      loginBtnLoading: false
    }
  },
  methods: {
    ...mapActions([
      'handleLogin',
      'getUserInfo'
    ]),
    handleSubmit ({ username, password }) {
      // console.log({ username, password })
      this.loginBtnLoading = true
      this.handleLogin({ username, password }).then(res => {
        this.getUserInfo().then(res => {
          this.$router.push({
            name: this.$config.homeName
          })
          this.loginBtnLoading = false
        })
      }).catch(err => {
        sendNotice('error', '登陆失败，请联系管理员')
        if (err.response.data.non_field_errors) {
          err = err.response.data.non_field_errors[0]
        }
        sendNotice('error', err)
        this.loginBtnLoading = false
      })
    }
  }
}
</script>

<style>

</style>
