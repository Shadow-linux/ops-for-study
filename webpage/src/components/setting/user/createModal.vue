<template>
  <div>
    <Modal
      v-model="ModalShow"
      :title="modalTitle"
      @on-ok="ok"
      :mask-closable="false"
      >
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
        <FormItem label="角色" prop="role">
            <Select v-model="shadowForm.role" style="width:100%">
              <Option value="Guest">Guest</Option>
              <Option value="普通用户">普通用户</Option>
              <Option value="管理员">管理员</Option>
            </Select>
        </FormItem>
        <FormItem label="权限组" prop="group">
            <Select v-model="shadowForm.group" style="width:100%">
              <Option v-for="item in groupList" :value="item.name" :key="item.id">{{ item.name }}</Option>
            </Select>
        </FormItem>
      </Form>
    </Modal>
  </div>
</template>

<script>

import { createUser } from '@/api/setting/user'
import { getRole, getGroup } from './libs.js'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'user-modal',
  props: [
    'userModalShow',
    'modalTitle',
    'groupList'
  ],
  computed: {
    ModalShow: {
      get () {
        return this.userModalShow
      },
      set (val) {
        this.$emit('switchUserModal', val)
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
      title: '',
      shadowForm: {
        username: '',
        password: '',
        password_check: '',
        department: '',
        position: '',
        role: 'Guest',
        group: 'guest',
        real_name: '',
        email: ''
      },
      ruleShadowForm: {
        username: [
          { required: true, message: '请填写用户名', trigger: 'blur' }
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
        ],
        role: [
          { required: true, message: '请选择角色', trigger: 'blur' }
        ],
        group: [
          { required: true, message: '请选择权限组', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    ok () {
      this.$refs['shadowForm'].validate((valid) => {
        console.log(valid)
        if (valid) {
          var roleObj = getRole(this.shadowForm['role'])
          var gid = getGroup(this.shadowForm['group'], this.groupList)
          var formObj = Object.assign(this.shadowForm, roleObj)
          formObj['gid'] = gid
          createUser(formObj).then(res => {
            this.$Message.success('创建用户成功.')
            this.$emit('reloadTable')
          }).catch(err => {
            var msg = err
            if (err.response.data['username']) {
              msg = err.response.data['username']
            }
            sendNotice('error', msg)
          })
        } else {
          this.$Message.error('创建用户失败')
        }
      })
    }
  }
}
</script>
