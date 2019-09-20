<template>
  <div>
    <Row>
      <Col span="24">
        <Card>
          <p slot="title">个人中心</p>
          <Form ref="dataForm" :model="dataForm" :rules="ruleDataForm" :label-width=100>
            <FormItem :label-width=50>
              <Button type="default" size="default" style="margin-right: 10px" @click="editForm" >编辑</Button>
              <Button type="primary" size="default" @click="saveForm('dataForm')">保存</Button>
            </FormItem>
            <FormItem label="用户名:">
              <Tag color="blue">{{ dataForm.username }}</Tag>
            </FormItem>
            <FormItem label="密码">
              <Button type="error" ghost size="small"  @click="changePassword">更改</Button>
            </FormItem>
            <FormItem label="姓名:" prop="real_name">
              <span v-if="!edit">{{ dataForm.real_name }}</span>
              <Input v-if="edit" v-model="dataForm.real_name" style="width: 300px" placeholder=""></Input>
            </FormItem>
            <FormItem label="Email:" prop="email">
              <span v-if="!edit">{{ dataForm.email }}</span>
              <Input v-if="edit" v-model="dataForm.email" style="width: 300px" placeholder=""></Input>
            </FormItem>
            <FormItem label="部门:" prop="department">
              <span v-if="!edit">{{ dataForm.department }}</span>
              <Input v-if="edit" v-model="dataForm.department" style="width: 300px" placeholder=""></Input>
            </FormItem>
            <FormItem label="岗位:" prop="position">
              <span v-if="!edit">{{ dataForm.position }}</span>
              <Input v-if="edit" v-model="dataForm.position" style="width: 300px" placeholder=""></Input>
            </FormItem>
            <FormItem label="角色:">
              <Tag color="default">{{ dataForm.role }}</Tag>
            </FormItem>
            <FormItem label="权限组:">
              <Tag color="default">{{ dataForm.groups }}</Tag>
            </FormItem>
          </Form>
        </Card>
      </Col>
    </Row>
    <Modal
        v-model="passwordModal"
        title="更改密码"
        @on-ok="ok('passwordForm')"
        :mask-closable="false"
        >
        <Form ref="passwordForm" :model="passwordForm" :rules="rulePasswordForm" :label-width=80 >
          <FormItem label="旧密码" prop="origin_password">
            <Input v-model="passwordForm.origin_password" placeholder="orgin password"></Input>
          </FormItem>
          <FormItem label="新密码" prop="password">
            <Input v-model="passwordForm.password" placeholder="new password"></Input>
          </FormItem>
          <FormItem label="确认密码" prop="password_check">
            <Input v-model="passwordForm.password_check" placeholder="confirm password"></Input>
          </FormItem>
        </Form>
    </Modal>
  </div>
</template>
<script>

import { getPersonalInfo, updatePersonalInfo, updatePersonalPassword } from '@/api/user'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'personal_center',
  data () {
    const validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else {
        if (this.passwordForm.password_check !== '') {
          // 对第二个密码框单独验证
          this.$refs.passwordForm.validateField('password_check')
        }
        callback()
      }
    }
    const validatePassCheck = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.passwordForm.password) {
        callback(new Error('两次密码不匹配!'))
      } else {
        callback()
      }
    }
    return {
      userId: this.$store.state.user.userId,
      edit: false,
      passwordModal: false,
      dataForm: {},
      ruleDataForm: {
        real_name: [{ required: true, message: 'The real_name cannot be empty', trigger: 'blur' }],
        email: [{ required: true, message: 'The email cannot be empty', trigger: 'blur' }],
        department: [{ required: true, message: 'The department cannot be empty', trigger: 'blur' }],
        position: [{ required: true, message: 'The position cannot be empty', trigger: 'blur' }]
      },
      passwordForm: {
        origin_password: '',
        password: '',
        password_check: ''
      },
      rulePasswordForm: {
        origin_password: [{ required: true, message: 'The origin password cannot be empty', trigger: 'blur' }],
        password: [{ required: true, validator: validatePass, trigger: 'blur' }],
        password_check: [{ required: true, validator: validatePassCheck, trigger: 'change' }]
      }
    }
  },
  methods: {
    editForm () {
      this.edit = true
    },
    saveForm (name) {
      this.edit = false
      this.$refs[name].validate((valid) => {
        if (valid) {
          updatePersonalInfo(this.userId, this.dataForm).then(res => {
            this.$Message.success('保存个人信息成功')
          }).catch(err => {
            sendNotice('error', err)
          })
        } else {
          this.$Message.error('保存个人信息失败!')
        }
      })
    },
    changePassword () {
      this.passwordModal = true
    },
    getUserRole () {
      var staff = this.dataForm.is_staff
      var admin = this.dataForm.is_superuser
      if (admin) return '管理员'
      if (staff) return '普通用户'
      return 'Guest'
    },
    ok (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          updatePersonalPassword(this.userId, this.passwordForm).then(res => {
            this.$Message.success('更新密码成功')
          }).catch(err => {
            sendNotice('error', err)
          })
        } else {
          this.$Message.error('更新密码失败!')
        }
      })
    }
  },
  mounted () {
    getPersonalInfo(this.userId).then(res => {
      this.dataForm = res.data
      this.dataForm['role'] = this.getUserRole()
      this.dataForm['groups'] = res.data['groups'][0]['name']
    }).catch(err => {
      sendNotice('error', err)
    })
  }
}
</script>
