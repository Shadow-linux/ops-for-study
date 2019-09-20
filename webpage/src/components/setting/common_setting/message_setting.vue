<template>
  <div>
    <Form ref="messageForm" :model="messageForm" :rules="ruleMessageForm" :label-width="150">
      <Button type="primary" style="float: right" ghost  @click="saveForm">保存</Button>
      <Divider orientation="left">&nbsp;<span class="divider-text">站内消息</span>&nbsp;</Divider>
        <FormItem label="启用站内消息:">
          <i-switch :value="messageForm.is_inner" @on-change="isInnerSw">
            <span slot="open">开</span>
            <span slot="close">关</span>
          </i-switch>
        </FormItem>
      <Divider orientation="left">&nbsp;<span class="divider-text">邮件消息</span>&nbsp;</Divider>
        <FormItem label="启用邮件消息:">
          <i-switch :value="messageForm.is_mail" @on-change="isMailSw">
            <span slot="open">开</span>
            <span slot="close">关</span>
          </i-switch>
        </FormItem>
        <FormItem label="SMTP 服务地址:" prop="mail.smtp_host">
          <Input v-model.trim="messageForm.mail.smtp_host"  placeholder="smtp host" class="input-width"></Input>
        </FormItem>
        <FormItem label="SMTP 端口:" prop="mail.smtp_port">
          <InputNumber :max="65535" :min="1" v-model="messageForm.mail.smtp_port"></InputNumber>
        </FormItem>
        <FormItem label="SMTP SSL:">
          <Checkbox v-model="messageForm.mail.smtp_ssl">&nbsp;启用</Checkbox>
        </FormItem>
        <FormItem label="Mail 推送账户:" prop="mail.mail_user">
          <Input v-model.trim="messageForm.mail.mail_user" placeholder="mail username" class="input-width"></Input>
        </FormItem>
        <FormItem label="Mail 账户密码:" prop="mail.mail_password">
          <Input v-model.trim="messageForm.mail.mail_password" type="password" placeholder="mail password" class="input-width"></Input>
        </FormItem>
        <FormItem label="Test 测试邮箱:">
          <Input v-model.trim="messageForm.mail.mail_test" placeholder="mail test" style="margin-right: 10px" class="input-width"></Input>
          <Button type="primary"  :loading="mailLoading" size="small"  @click="mailTest">
            <span v-if="!mailLoading">Test</span>
            <span v-else>Loading</span>
          </Button>
        </FormItem>
        <FormItem :label-width="50">
        </FormItem>
      <Divider orientation="left">&nbsp;<span style="color: #c5c8ce">Other</span>&nbsp;</Divider>
    </Form>
  </div>
</template>
<script>

import { getSettingMessage, saveSettingMessage, testSettingMesssage } from '@/api/setting/common_setting'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'message_setting',
  data () {
    return {
      switch1: true,
      mailLoading: false,
      messageForm: {
        is_inner: false,
        is_mail: false,
        mail: {
          smtp_host: '',
          smtp_port: 1,
          smtp_ssl: false,
          mail_user: '',
          mail_password: '',
          mail_test: ''
        }
      },
      ruleMessageForm: {
        'mail.smtp_host': [ { required: true, message: 'Can not be empty.', trigger: 'blur' } ],
        'mail.mail_user': [ { required: true, message: 'Can not be empty.', trigger: 'blur' } ],
        'mail.mail_password': [ { required: true, message: 'Can not be empty.', trigger: 'blur' } ],
        'mail.smtp_port': [ { required: true } ]
      }
    }
  },
  methods: {
    isInnerSw (bool) { this.messageForm.is_inner = bool },
    isMailSw (bool) { this.messageForm.is_mail = bool },
    mailTest () {
      if (this.messageForm.mail.mail_test.length === 0) {
        this.$Message.error('测试邮件不能为空.')
        return
      }
      this.mailLoading = true
      this.saveForm()
      setTimeout(() => {
        testSettingMesssage('mail', {
          'mail_test': this.messageForm.mail.mail_test
        }).then(res => {
          this.$Message.success('测试邮件已发送，请注意查收')
          this.mailLoading = false
        }).catch(err => {
          sendNotice('error', err)
          this.mailLoading = false
        })
      }, 1500)
    },
    saveForm () {
      var saveData = {
        'is_mail': this.messageForm.is_mail,
        'is_inner': this.messageForm.is_inner,
        'message_setting': JSON.stringify({
          mail: this.messageForm.mail
        })
      }
      saveSettingMessage(saveData).then(res => {
        this.$Message.success('保存成功')
      }).catch(err => {
        sendNotice('error', err)
      })
    }
  },
  mounted () {
    getSettingMessage().then(res => {
      this.messageForm.mail = res.data[0]['message_setting']['mail']
      this.messageForm.is_inner = res.data[0]['is_inner']
      this.messageForm['is_mail'] = res.data[0]['is_mail']
    }).catch(err => {
      sendNotice('error', err)
    })
  }
}
</script>
<style scoped>
/* .ivu-switch-checked {
  border-color: #67C23A;
  background-color: #67C23A;
} */
.input-width {
  width: 300px;
}
.divider-text {
  color: #515a6e;
  font-size: 14px;
}
</style>
