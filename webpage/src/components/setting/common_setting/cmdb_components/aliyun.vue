<template>
  <div>
    <span v-if="!showAlert">
      <a style=" font-size: 12px" @click="showAlert = true" >HELP</a>
      <Icon type="ios-help-circle-outline" style="color: #2D8cF0; margin-left: 3px"/>
    </span>
    <Alert v-if="showAlert" type="warning" closable @on-close="showAlert = false">
      <span slot="desc">
          <b>Key Name: </b>设置后用于对ECS等阿里云资产做分类（类似于机房）<br>
      </span>
    </Alert>
    <Divider orientation="left">
      <span class="divider-text">Access Key 设置</span>
    </Divider>
    <div style="margin-left: 20px">
      <Form ref="dataForm" :model="dataForm" :rules="ruleDataForm" inline>
        <FormItem label="" prop="key_name">
          <Input v-model="dataForm.key_name" placeholder="Key Name" style="width: 200px"></Input>
        </FormItem>
        <FormItem label="" prop="access_key">
          <Input v-model="dataForm.access_key" placeholder="Access Key" style="width: 200px"></Input>
        </FormItem>
        <FormItem label="" prop="access_secret">
          <Input v-model="dataForm.access_secret" placeholder="Access Secret" style="width: 200px"></Input>
        </FormItem>
        <FormItem label="" prop="region_id">
          <Input v-model="dataForm.region_id" placeholder="Region Id" style="width: 120px"></Input>
        </FormItem>
        <FormItem>
          <Button type="primary" @click="addAccessKey('dataForm')" ghost>添加</Button>
        </FormItem>
      </Form>
      <Table :columns="tableColumns" :data="tableDatas"></Table>
    </div>
    <Modal
        v-model="keyModal"
        title="修改 Access Key"
        @on-ok="keyModalOk('mDataFrom')"
        >
        <Form ref="mDataFrom" :model="mDataForm" :rules="ruleDataForm" :label-width=110 >
          <FormItem label="Key Name:">
            <Tag color="blue">{{ mDataForm.key_name }}</Tag>
          </FormItem >
          <FormItem prop="access_key"  label="Access Key:">
            <Input v-model="mDataForm.access_key" placeholder="access key"></Input>
          </FormItem>
          <FormItem prop="access_secret"  label="Access Secret:">
            <Input v-model="mDataForm.access_secret" placeholder="access secret"></Input>
          </FormItem>
          <FormItem prop="region_id"  label="Region Id:">
            <Input v-model="mDataForm.region_id" placeholder="region id"></Input>
          </FormItem>
        </Form>
    </Modal>
  </div>
</template>
<script>

import { getAliyunAccessKey, addAliyunAccessKey, deleteAliyunAccessKey, updateAliyunAceessKey } from '@/api/setting/common_setting'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'cmdb_setting_aliyun',
  data () {
    return {
      showAlert: false,
      keyModal: false,
      dataForm: {},
      mDataForm: {
      },
      ruleDataForm: {
        key_name: [
          { required: true, message: 'Cannot be empty.', trigger: 'blur' }
        ],
        access_key: [
          { required: true, message: 'Cannot be empty.', trigger: 'blur' }
        ],
        access_secret: [
          { required: true, message: 'Cannot be empty.', trigger: 'blur' }
        ],
        region_id: [
          { required: true, message: 'Cannot be empty.', trigger: 'blur' }
        ]
      },
      tableColumns: [
        {
          title: 'Key Name',
          key: 'key_name'
        },
        {
          title: 'Access Key',
          key: 'access_key'
        },
        {
          title: 'Region ID',
          key: 'region_id'
        },
        {
          title: 'Update Time',
          key: 'updated',
          align: 'center'
        },
        {
          title: 'Action',
          key: 'action',
          align: 'center',
          render: (h, params) => {
            console.log(params.row)
            return h('span', {}, [
              h('a', {
                style: {
                  'margin-right': '20px'
                },
                on: {
                  'click': () => {
                    this.mDataForm = {
                      'id': params.row['id'],
                      'key_name': params.row['key_name'],
                      'access_key': params.row['access_key'],
                      'access_secret': '',
                      'region_id': params.row['region_id']
                    }
                    this.keyModal = true
                  }
                }
              }, '修改'),
              h('Poptip', {
                props: {
                  'confirm': true,
                  'title': 'Are you sure ?',
                  'placement': 'left-end'
                },
                on: {
                  'on-ok': () => {
                    deleteAliyunAccessKey(params.row.id).then(
                      res => {
                        this.$Message.success('删除成功')
                        this.reloadTable()
                      }
                    ).catch(err => {
                      sendNotice('error', err)
                    })
                  }
                }
              }, [
                h('a', {
                  style: {
                    'color': '#c5c8ce'
                  }
                }, '删除')
              ])
            ])
          }
        }
      ],
      tableDatas: []
    }
  },
  methods: {
    keyModalOk (name) {
      this.$refs[name].validate((valid) => {
        console.log(valid)
        if (valid) {
          updateAliyunAceessKey(this.mDataForm.id, this.mDataForm).then(res => {
            this.$Message.success('修改成功')
            this.reloadTable()
          }).catch(err => {
            sendNotice('error', err)
          })
        } else {
          this.$Message.error('修改失败!')
        }
      })
    },
    addAccessKey (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          addAliyunAccessKey(this.dataForm).then(res => {
            this.$Message.success('添加成功')
            this.reloadTable()
          }).catch(err => {
            if (err.response.data['key_name']) {
              err = err.response.data['key_name'][0]
            }
            sendNotice('error', err)
          })
        } else {
          this.$Message.error('修改失败!')
        }
      })
    },
    reloadTable () {
      getAliyunAccessKey().then(res => {
        this.tableDatas = res.data
      }).catch(err => {
        sendNotice('error', err)
      })
    }
  },
  mounted () {
    this.reloadTable()
  }
}
</script>
<style>
.divider-text {
  color: #515a6e;
  font-size: 14px;
}
.content-text {
  padding-left: 30px;
}
.ivu-poptip-confirm .ivu-poptip-body .ivu-icon {
  left: 18px;
}
</style>
