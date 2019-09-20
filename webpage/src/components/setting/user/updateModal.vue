<template>
  <div>
    <Modal
        v-model="ModalShow"
        title="修改用户"
        @on-ok="ok"
        ok-text="保存"
        :mask-closable="false"
        >
        <Form ref="shadowForm" :model="shadowForm" :label-width=80>
          <FormItem label="用户名" prop="username">
              <Tag color="blue">{{ shadowForm.username }}</Tag>
          </FormItem>
          <FormItem label="姓名" prop="department">
              <Input type="text" v-model="shadowForm.real_name"></Input>
          </FormItem>
          <FormItem label="部门" prop="department">
              <Input type="text" v-model="shadowForm.department"></Input>
          </FormItem>
          <FormItem label="岗位" prop="position">
              <Input type="text" v-model="shadowForm.position"></Input>
          </FormItem>
          <FormItem label="Email" prop="email">
              <Input type="text" v-model="shadowForm.email"></Input>
          </FormItem>
          <FormItem label="Mobile" prop="mobile">
              <Input type="text" v-model="shadowForm.mobile"></Input>
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

import { updateUserInfo } from '@/api/setting/user'
import { getRole, getGroup } from './libs.js'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'update-modal',
  data () {
    return {
      shadowForm: {
        id: '',
        username: '',
        department: '',
        position: '',
        role: '',
        group: '',
        real_name: '',
        email: '',
        mobile: ''
      }
    }
  },
  props: [
    'updateModalShow',
    'updateModalObj',
    'groupList'
  ],
  watch: {
    updateModalObj () {
      this.shadowForm = this.updateModalObj
    }
  },
  computed: {
    ModalShow: {
      get () {
        return this.updateModalShow
      },
      set (val) {
        this.$emit('switchUpdateModal', val)
      }
    }
  },
  methods: {
    ok () {
      var roleObj = getRole(this.shadowForm['role'])
      var gid = getGroup(this.shadowForm['group'], this.groupList)
      var formObj = Object.assign(this.shadowForm, roleObj)
      formObj['gid'] = gid
      updateUserInfo(this.shadowForm.id, formObj).then(res => {
        this.$Message.success('修改用户信息成功')
        this.$emit('reloadTable')
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    cancel () {
      this.$Message.info('Clicked cancel')
    }
  }
}
</script>
