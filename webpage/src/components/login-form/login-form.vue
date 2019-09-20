<template>
  <div>
    <Form ref="loginForm" :model="form" :rules="rules" @keydown.enter.native="handleSubmit">
      <FormItem prop="username">
        <Input v-model="form.username" placeholder="请输入用户名">
          <span slot="prepend">
            <Icon :size="16" type="ios-person"></Icon>
          </span>
        </Input>
      </FormItem>
      <FormItem prop="password">
        <Input type="password" v-model="form.password" placeholder="请输入密码">
          <span slot="prepend">
            <Icon :size="14" type="md-lock"></Icon>
          </span>
        </Input>
      </FormItem>
      <FormItem>
        <Button @click="handleSubmit" :loading="loginBtnLoading" type="primary" long style="margin-bottom: 10px">登录</Button>
        <Button @click="registerModal = true" type="default" long>注册</Button>
      </FormItem>
    </Form>
    <Modal
        title="注册用户"
        v-model="registerModal"
        @on-ok="registerHandle"
        :mask-closable="false">
        <Form ref="shadowForm" :model="shadowForm" :rules="ruleShadowForm" :label-width="80">
          <FormItem label="用户名" prop="username">
              <Input type="email" v-model="shadowForm.username"></Input>
          </FormItem>
          <FormItem label="密码" prop="password">
              <Input type="password" v-model="shadowForm.password"></Input>
          </FormItem>
          <FormItem label="确认密码" prop="password_check">
              <Input type="password" v-model="shadowForm.password_check"></Input>
          </FormItem>
          <FormItem label="姓名" prop="real_name">
              <Input type="text" v-model="shadowForm.real_name"></Input>
          </FormItem>
          <FormItem label="Email" prop="email">
              <Input type="text" v-model="shadowForm.email"></Input>
          </FormItem>
          <FormItem label="Mobile" prop="mobile">
              <Input type="text" v-model="shadowForm.mobile"></Input>
          </FormItem>
          <FormItem label="部门" prop="department">
              <Input type="text" v-model="shadowForm.department"></Input>
          </FormItem>
          <FormItem label="岗位" prop="position">
              <Input type="text" v-model="shadowForm.position"></Input>
          </FormItem>
        </Form>
    </Modal>
  </div>
</template>
<script>

import { registerUser } from '@/api/user'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'LoginForm',
  props: {
    loginBtnLoading: {
      type: Boolean,
      default: false
    },
    usernameRules: {
      type: Array,
      default: () => {
        return [
          { required: true, message: '账号不能为空', trigger: 'blur' }
        ]
      }
    },
    passwordRules: {
      type: Array,
      default: () => {
        return [
          { required: true, message: '密码不能为空', trigger: 'blur' }
        ]
      }
    }
  },
  data () {
    const validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        if (this.shadowForm.password_check !== '') {
          // 对第二个密码框单独验证
          this.$refs.shadowForm.validateField('password_check')
        }
        callback()
      }
    }
    const validatePassCheck = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.shadowForm.password) {
        callback(new Error('两次密码不匹配!'))
      } else {
        callback()
      }
    }
    return {
      form: {
        username: '',
        password: ''
      },
      registerModal: false,
      shadowForm: {
        username: '',
        password: '',
        password_check: '',
        department: '',
        position: '',
        real_name: '',
        email: ''
      },
      ruleShadowForm: {
        username: [
          { required: true, message: '请填写用户名, 必须为邮箱', trigger: 'blur', type: 'email' }
        ],
        password: [
          { validator: validatePass, trigger: 'change', required: true }
        ],
        password_check: [
          { validator: validatePassCheck, trigger: 'change', required: true }
        ],
        real_name: [
          { required: true, message: '请填写姓名', trigger: 'blur' }
        ],
        department: [
          { required: true, message: '请填写部门', trigger: 'blur' }
        ],
        position: [
          { required: true, message: '请填写岗位', trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请填写Email', trigger: 'blur' }
        ],
        mobile: [
          { required: true, message: '请填写Mobile', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    rules () {
      return {
        username: this.usernameRules,
        password: this.passwordRules
      }
    }
  },
  methods: {
    handleSubmit () {
      this.$refs.loginForm.validate((valid) => {
        if (valid) {
          this.$emit('on-success-valid', {
            username: this.form.username,
            password: this.form.password
          })
        }
      })
    },
    registerHandle () {
      this.$refs.shadowForm.validate((valid) => {
        if (valid) {
          registerUser(this.shadowForm).then(res => {
            this.$Message.success('注册成功')
          }).catch(err => {
            var msg = err
            if (err.response.data['username']) {
              msg = err.response.data['username']
            }
            sendNotice('error', msg)
          })
        } else {
          this.$Message.error('请填写完整信息.')
        }
      })
    }
  }
}
</script>
