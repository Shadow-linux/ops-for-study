<template>
  <div>
    <Modal
        v-model="ModalShow"
        title="修改页面权限"
        @on-ok="ok"
        on-text="保存">
        <Alert type="warning" show-icon>子页面授权只读或读写时，父页面需要授权可见，否则子页面不可见</Alert>
        <Collapse simple>
        <Panel name="page">
          <span style="color: #409eff; font-size: 14px;">页面权限</span>
          <div slot="content">
            <Row>
              <Col span="24">
                <!-- <Divider orientation="left" class="inner-divider-text">首页</Divider> -->
                <MPagePerm :saveSignal="saveSignal" :mPagePermData="mPagePermData" @setPagePerm="setPagePerm"></MPagePerm>
              </Col>
            </Row>
          </div>
        </Panel>
        <Panel name="publish">
          <span style="color: #409eff; font-size: 14px;">发布权限</span>
          <div slot="content">
            <Row>
              <Col span="24">
                <!-- <Divider orientation="left" class="inner-divider-text">首页</Divider> -->
              </Col>
            </Row>
          </div>
        </Panel>
    </Collapse>
    </Modal>
  </div>
</template>
<script>

import { MPagePerm } from './components'
import { updateGroupPerm } from '@/api/setting/permission_group'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'update_perm_modal',
  components: {
    MPagePerm
  },
  data () {
    return {
      saveSignal: true,
      pagePermData: {}
    }
  },
  props: [
    'updatePermModal',
    'mPagePermData'
  ],
  computed: {
    ModalShow: {
      get () {
        return this.updatePermModal
      },
      set (val) {
        this.$emit('switchUpdatePermModal', val)
      }
    }
  },
  methods: {
    setPagePerm (data) {
      this.pagePermData = data
    },
    ok () {
      // 保存页面权限时发送signal 给 页面权限组件 和 发布权限组件
      this.saveSignal = !this.saveSignal
      // 暂停一秒, 让数据赋值完成
      setTimeout(() => {
        console.log(this.pagePermData)
        updateGroupPerm(this.pagePermData['group_id'], { 'page_permission': this.pagePermData['page_permission'] }).then(res => {
          this.$Message.success('修改权限组成功')
        }).catch(err => {
          sendNotice('error', err)
        })
      }, 600)
    }
  }
}
</script>
<style  scoped>
.ivu-collapse {
  border: 0;
}
</style>
