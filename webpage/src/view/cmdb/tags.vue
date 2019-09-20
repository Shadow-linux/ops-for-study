<template>
  <div>
    <Row>
      <Col span="24">
        <Card>
          <p slot="title">标签管理</p>
          <Form inline @submit.native.prevent >
            <Row>
              <Col span="1">
                <FormItem >
                  <Poptip
                    confirm
                    title="确定删除吗 ?"
                    placement="right-start"
                    @on-ok="deleteOk">
                    <Button type="default" size="small">删除</Button>
                  </Poptip>
                </FormItem>
              </Col>
              <Col span="1">
                <FormItem>
                  <Button type="primary" ghost size="small" @click="addModal = true">添加</Button>
                </FormItem>
              </Col>
              <Col span="5" offset="17">
                <FormItem>
                  <Input search v-model="searchTag" @on-enter="searchInput" placeholder="搜索 tag key" style="width: 240px"></Input>
                </FormItem>
              </Col>
            </Row>
          </Form>
          <Table @on-selection-change="tableSelect" :columns="tableColunms" :data="tableDatas"></Table>
        </Card>
      </Col>
    </Row>
    <Modal
      v-model="addModal"
      title="添加 Tag"
      @on-ok="addOk('dataForm')"
      width="400"
      >
      <Form ref="dataForm" :model="dataForm" :rules="ruleDataForm" :label-width=80>
        <FormItem label="标签名:" prop="tag_key">
          <Input v-model="dataForm.tag_key"></Input>
        </FormItem>
        <FormItem label="标签值:" prop="tag_value">
          <Input v-model="dataForm.tag_value"></Input>
        </FormItem>
      </Form>
    </Modal>
  </div>
</template>
<script>

import { getTagsList, deleteTag, addTag } from '@/api/cmdb/tags.js'
import { sendNotice } from '@/libs/util.js'

export default {
  name: 'cmdb_tags',
  data () {
    return {
      tableColunms: [
        {
          type: 'selection',
          width: 50
        },
        {
          'title': 'Tag Key',
          'key': 'tag_key'
        },
        {
          'title': 'Tag Value',
          'key': 'tag_value'
        },
        {
          'title': 'Created',
          'key': 'created'
        }
      ],
      selectList: [],
      tableDatas: [],
      originTableDatas: [],
      searchTag: '',
      addModal: false,
      dataForm: {
        'tag_key': '',
        'tag_value': ''
      },
      ruleDataForm: {
        tag_key: [
          { required: true, message: '请填写标签名', trigger: 'blur' }
        ],
        tag_value: [
          { required: true, message: '请填写标签值', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    addOk (name) {
      this.$refs[name].validate((valid) => {
        if (valid) {
          addTag(this.dataForm).then(res => {
            this.$Message.success('添加成功!')
            this.reloadTable()
          }).catch(err => {
            sendNotice('error', err)
          })
        } else {
          this.$Message.error('添加失败!')
        }
      })
    },
    deleteOk () {
      this.selectList.forEach(item => {
        deleteTag(item.id).then(res => {
          this.$Message.success('删除成功')
          this.reloadTable()
        }).catch(err => {
          sendNotice('error', err)
        })
      })
    },
    tableSelect (selectList) {
      console.log(selectList)
      this.selectList = selectList
    },
    searchInput () {
      this.tableDatas = []
      this.originTableDatas.map(item => {
        if (item.tag_key.indexOf(this.searchTag) !== -1) {
          this.tableDatas.push(item)
        }
      })
    },
    reloadTable () {
      getTagsList().then(res => {
        this.tableDatas = res.data
        this.originTableDatas = res.data
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
