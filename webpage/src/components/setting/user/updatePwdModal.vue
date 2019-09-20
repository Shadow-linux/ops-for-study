<template>
  <div>
    <Modal
        v-model="ModalShow"
        title="修改密码"
        @on-ok="ok"
        ok-text="保存"
        @on-cancel="cancel"
        >
        <Form ref="shadowForm" :model="shadowForm" :rules="ruleShadowForm" inline :label-width=80>
          <FormItem label="用户名">
            <Tag color="blue">{{ shadowForm.username }}</Tag>
          </FormItem>
          <FormItem label="新密码"  prop="password" style="width: 100%">
            <Input type="password" v-model="shadowForm.password"></Input>
          </FormItem>
          <FormItem label="确认密码"  prop="password_check" style="width: 100%">
            <Input type="password" v-model="shadowForm.password_check"></Input>
          </FormItem>
        </Form>
    </Modal>
  </div>
</template>
<script>
import { updateUserPassword } from '@/api/setting/user'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'pwd-modal',
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
      shadowForm: {
        password: '',
        password_check: ''
      },
      ruleShadowForm: {
        password: [
          { validator: validatePass, trigger: 'change', required: true }
        ],
        password_check: [
          { validator: validatePassCheck, trigger: 'change', required: true }
        ]
      }
    }
  },
  watch: {
    pwdObj () {
      this.shadowForm = {
        id: this.pwdObj.id,
        username: this.pwdObj.username,
        password: '',
        password_check: ''
      }
    }
  },
  props: [
    'pwdModalShow',
    'pwdObj'
  ],
  computed: {
    ModalShow: {
      get () {
        return this.pwdModalShow
      },
      set (val) {
        this.$emit('switchPwdModalShow', val)
      }
    }
  },
  methods: {
    ok () {
      this.$refs['shadowForm'].validate((valid) => {
        if (valid) {
          updateUserPassword(this.shadowForm.id, this.shadowForm).then(res => {
            this.$Message.success('更新密码成功')
          }).catch(err => {
            sendNotice('error', err)
          })
        } else {
          this.$Message.error('更新密码失败')
        }
      })
    },
    cancel () {
      this.$Message.info('Clicked cancel')
    }
  }
}
</script>
