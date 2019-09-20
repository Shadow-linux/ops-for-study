<template>
  <div>
    <Drawer placement="right" :closable="false" v-model="drawerShow" width="450">
      <p slot="header" style="color: #909399; height: 32px;" >
        <span >已锁定环境列表</span>
        <Button type="error" ghost style="height: 30px; float: right" icon="ios-lock-outline" @click="handleCreateLockBtn">建锁</Button>
        <Button type="default" shape="circle" style="float:right; margin-right: 10px; height: 30px" @click="() => { refreshAll() }" ><Icon type="md-refresh" /></Button>
      </p>
      <Card v-for="item in publishLockData" :key="item.id" style="margin-bottom: 10px;">
        <p slot="title" style="height: 24px;">
          <span style="display:inline-block; overflow:hidden; width: 60%; text-overflow: ellipsis;" :title="item.env">
            <Tag color="success"> {{ item.env }}</Tag>
          </span>
          <span style="display: inline-block; float: right">
            <Button type="primary" ghost size="small" icon="ios-open-outline" style="margin-right: 10px" @click="handleUpdateLockBtn(item)">编辑</Button>
            <Button type="default"  size="small" icon="ios-unlock-outline" @click="handleUnlockEnv(item)">释放</Button>
          </span>
        </p>
        <div style="height: 170px; overflow: auto">
          <Form :label-width="70">
            <FormItem label="组名:" class="shadow-ivu-form-item">
              <b style="margin-right: 20px">{{ item.lock_grp_name }}</b>
              属主:<Tag color="blue" style="margin-left: 10px">{{ item.creator_info.real_name }}</Tag>
            </FormItem>
            <FormItem label="成员:" class="shadow-ivu-form-item">
              <Tag type="border" v-for="user in item.user_ids" :key="user.id">{{ user.real_name }}</Tag>
            </FormItem>
            <FormItem label="锁定周期:" class="shadow-ivu-form-item">
              <b>{{ item.lock_time }} min</b>
            </FormItem>
            <FormItem label="绑定应用:" class="shadow-ivu-form-item">
              <Tag color="default" v-for="app in item.app_ids" :key="app.id">{{ app.app_name }}</Tag>
            </FormItem>
            <FormItem label="创建时间:" class="shadow-ivu-form-item">
              <b>{{ item.created }}</b>
            </FormItem>
            <FormItem label="过期时间:" class="shadow-ivu-form-item">
              <b>{{ item.expired }}</b>
            </FormItem>
          </Form>
        </div>
      </Card>
    </Drawer>
    <Modal
      v-model="envLockModal"
      :title="envLockModalTitle"
      :mask-closable="false"
      @on-ok="handleEnvLock"
      okText="提交"
      width="700"
      >
      <Form ref="envLockForm" :model="envLockForm" :label-width="110" :rules="ruleEnvLockForm">
        <FormItem label="自定义名:" prop="lock_grp_name">
          <Input v-model.trim="envLockForm.lock_grp_name" style="width: 70%" placeholder="组名，长度128字符"></Input>
        </FormItem>
        <FormItem label="锁定时间(分钟):" prop="lock_time">
          <InputNumber v-model="envLockForm.lock_time" style="width: 70%" :max="1440"
          placeholder="max = 1400(min) = 1(day)">
          </InputNumber>
        </FormItem>
        <FormItem label="成员:" prop="user_ids">
          <Select v-model="envLockForm.user_ids" multiple filterable style="width: 70%">
            <Option v-for="item in usernameList" :value="item.id" :key="item.id">{{ item.real_name }}</Option>
          </Select>
        </FormItem>
        <FormItem label="环境:" prop="env">
          <Tag color="volcano" v-show="!lockEnvShow"> {{ envLockForm.env }}</Tag>
          <Select v-model="envLockForm.env" v-show="lockEnvShow" filterable style="width: 70%" @on-change="handleEnvChange">
            <Option v-for="env in envList" :value="env" :key="env">{{ env }}</Option>
          </Select>
        </FormItem>
        <FormItem label="应用:" prop="app_ids">
           <Transfer
            :data="srcAppDatas"
            :target-keys="envLockForm.app_ids"
            filterable
            :filter-method="filterMethod"
            :titles="['可绑定的应用', '已绑定的应用']"
            @on-change="handleTransferChange"
            style="width: 90%"></Transfer>
        </FormItem>
      </Form>
    </Modal>
  </div>
</template>
<script>
import { envLockList, getEnvs, getUsersList, getLockEnvAppList, getBindLockEnvAppList, createEnvLock, updateEnvLock,
  unlockEnv } from '@/api/code_publish/publish'
import { sendNotice, getUserId } from '@/libs/util.js'
export default {
  name: 'env_lock',
  props: [
    'pdrawerShow'
  ],
  computed: {
    drawerShow: {
      get () {
        return this.pdrawerShow
      },
      set (val) {
        this.$emit('switchdrawerShow', val)
      }
    }
  },
  watch: {
    drawerShow (newVal, oldVal) {
      if (newVal) {
        this.refreshAll()
      }
    }
  },
  data () {
    return {
      userID: getUserId(),
      lockEnvShow: true,
      srcAppDatas: [],
      usernameList: [],
      envLockModal: false,
      envLockModalTitle: '',
      currentAction: 'create',
      envLockForm: {
        lock_grp_name: '',
        lock_time: 60,
        user_ids: [],
        env: '',
        app_ids: [],
        creator: 0,
        delay_lock_time: 0
      },
      envList: [],
      ruleEnvLockForm: {
        lock_grp_name: [
          { required: true, message: '必须填写，长度128字符', trigger: 'blur' }
        ],
        lock_time: [
          { required: true, message: '必须填写，最大值1400', trigger: 'blur', type: 'number' }
        ],
        user_ids: [
          { required: true, message: '必须填写', trigger: 'blur', type: 'array' }
        ],
        env: [
          { required: true, message: '必须填写', trigger: 'blur', type: 'string' }
        ],
        app_ids: [
          { required: true, message: '必须填写', trigger: 'blur', type: 'array' }
        ]
      },
      publishLockData: [],
      choseUpdateEnvLockItem: {}
    }
  },
  methods: {
    // 释放环境
    handleUnlockEnv (item) {
      unlockEnv(item.id).then(res => {
        this.$Message.success('成功释放')
        this.refreshAll()
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    // 环境变化是更换IP
    handleEnvChange (env) {
      getLockEnvAppList(env).then(res => {
        this.srcAppDatas = res.data
        this.envLockForm.app_ids = []
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    // 点击创建
    handleCreateLockBtn () {
      this.currentAction = 'create'
      this.envLockModal = true
      this.envLockModalTitle = '创建环境锁'
      this.lockEnvShow = true
      this.envLockForm = {
        'lock_grp_name': '',
        'lock_time': 60,
        'user_ids': [],
        'env': '',
        'app_ids': [],
        'creator': this.userID
      }
    },
    // 点击更新
    handleUpdateLockBtn (item) {
      if (this.userID !== item.creator) {
        this.$Modal.warning({
          title: '权限警告',
          content: '您不是该环境锁的Creator，请联系Creator'
        })
        return
      }
      this.currentAction = 'update'
      this.envLockModal = true
      this.envLockModalTitle = '更新环境锁'
      this.lockEnvShow = false
      this.envLockForm.id = item.id
      this.envLockForm.env = item.env
      this.envLockForm.lock_grp_name = item.lock_grp_name
      this.envLockForm.lock_time = item.lock_time
      this.envLockForm.creator = item.creator
      this.envLockForm.user_ids = []
      item.user_ids.forEach(item => {
        this.envLockForm.user_ids.push(item.id)
      })
      // 左侧列表
      getLockEnvAppList(item.env).then(res => {
        this.srcAppDatas = res.data
      }).catch(err => {
        sendNotice('error', err)
      })
      // 右侧列表
      getBindLockEnvAppList(item.id).then(subres => {
        this.envLockForm.app_ids = subres.data
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    // 提交envLockForm
    handleEnvLock () {
      if (this.currentAction === 'create') {
        createEnvLock(this.envLockForm).then(res => {
          this.$Message.success('成功锁定')
          this.refreshAll()
        }).catch(err => {
          if (err.response.data['non_field_errors'][0].indexOf('唯一') >= -1) {
            sendNotice('error', '您已创建该环境的锁，无需重复建锁.')
          }
          sendNotice('error', err)
        })
      } else if (this.currentAction === 'update') {
        updateEnvLock(this.envLockForm.id, this.envLockForm).then(res => {
          this.$Message.success('更新锁成功')
          this.refreshAll()
        }).catch(err => {
          sendNotice('error', err)
        })
      }
    },
    handleTransferChange (newTargetDatas) {
      console.log(newTargetDatas)
      this.envLockForm.app_ids = newTargetDatas
    },
    filterMethod (data, query) {
      return data.label.indexOf(query) > -1
    },
    refreshEnvLockList () {
      envLockList().then(res => {
        this.publishLockData = res.data
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    refreshAll () {
      this.refreshEnvLockList()
      getEnvs().then(res => {
        this.envList = []
        res.data.forEach(item => {
          if (item.env !== 'ALL') {
            this.envList.push(item.env)
          }
        })
      }).catch(err => {
        sendNotice('error', err)
      })
      getUsersList().then(res => {
        this.usernameList = res.data
      }).catch(err => {
        sendNotice('error', err)
      })
    }
  },
  mounted () {
    this.refreshAll()
  }
}
</script>
<style scoped>
/deep/ .ivu-card-head {
  border-bottom: 1px solid #e8eaec;
  padding: 10px 16px;
  line-height: 1;
}
/deep/ .shadow-ivu-form-item {
  margin-bottom: 5px;
  vertical-align: top;
  zoom: 1;
}
/deep/ .ivu-transfer-list {
  display: inline-block;
  width: 40%;
  height: 250px;
  font-size: 12px;
  vertical-align: middle;
  position: relative;
  padding-top: 35px;
}
</style>
