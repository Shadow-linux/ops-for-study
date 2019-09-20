<template>
  <div>
    <Row>
      <Col span="10">
        <Poptip
          confirm
          title="确定删除吗 ?"
          @on-ok="deleteData"
          placement="bottom-start"
          >
          <Button size="small">删除</Button>
        </Poptip>
        <Button type="primary" ghost size="small" style="margin-left: 10px" @click="createModal">创建</Button>
      </Col>
      <Col span="2" offset="4">
        <Button type="success" size="small" ghost @click="() => { createStepsModal = true }">增加发布步骤</Button>
      </Col>
      <Col span="7" offset="1">
        <Input v-model.trim="templateName" placeholder="搜索模版名字" search @on-enter="searchValue"></Input>
      </Col>
    </Row>
    <Table :loading="tableLoading"
    :columns="tableColumn"
    :data="tableData"
    @on-selection-change="selectChange"
    style="margin-top: 10px">
    </Table>
    <Modal
      v-model="createStepsModal"
      title="增加发布步骤"
      :mask-closable="false"
      >
      <Card>
        <Tag v-for="item in publish_steps" :key="item" :name="item" closable @on-close="handleRemoveStep" color="cyan" type="border">{{ item }}</Tag>
      </Card>
      <br>
      <Input v-model="control_publish_step" placeholder="步骤名" style="width: 60%; margin-right: 10px"></Input>
      <Button icon="ios-add" type="dashed" size="small" @click="handleAddStep">添加步骤</Button>
    </Modal>
    <Modal
      v-model="editModal"
      :title="editModalTitle"
      @on-ok="modalOk"
      width="1000"
      >
      <Form ref="" :model="dataForm" :label-width="100">
        <FormItem label="模版名字:">
          <Input v-model.trim="dataForm.name" placeholder="通用参数" style="width: 100%"></Input>
        </FormItem>
        <FormItem label="部署步骤:">
          <Select v-model="dataForm.deploy_steps" multiple filterable>
            <Option v-for="item in publish_steps" :value="item" :key="item">{{ item }}</Option>
          </Select>
        </FormItem>
        <FormItem label="同步步骤:">
          <Select v-model="dataForm.deploy_sync_steps" multiple filterable>
            <Option v-for="item in publish_steps" :value="item" :key="item">{{ item }}</Option>
          </Select>
        </FormItem>
        <FormItem label="回滚步骤:">
          <Select v-model="dataForm.rollback_steps" multiple filterable>
            <Option v-for="item in publish_steps" :value="item" :key="item">{{ item }}</Option>
          </Select>
        </FormItem>
      </Form>
    </Modal>
  </div>
</template>
<script>
// 需修改
import { getOpts, createOpts, deleteOpts, updateOpts, getSteps, addStep, deleteStep } from '@/api/code_publish/template/steps'
import { sendNotice } from '@/libs/util.js'

export default {
  // 修改
  name: 'tmpl_steps',
  data () {
    return {
      createStepsModal: false,
      publish_steps: [],
      control_publish_step: '',
      templateName: '',
      dataForm: {
        name: '',
        deploy_steps: [],
        rollback_steps: [],
        deploy_sync_steps: []
      },
      tableSelection: [],
      tableLoading: false,
      tableColumn: [
        {
          type: 'selection',
          width: 50,
          align: 'center'
        },
        {
          title: 'ID',
          key: 'id',
          width: 80
        },
        {
          title: 'Name',
          key: 'name',
          tooltip: true,
          width: 150
        },
        {
          title: '发布步骤',
          // 需修改
          render: (h, params) => {
            let steps = [
              h('p', {}, `部署: ${params.row.deploy_steps.join(' --> ')}`),
              h('p', {}, `同步: ${params.row.deploy_sync_steps.join(' --> ')}`),
              h('p', {}, `回滚: ${params.row.rollback_steps.join(' --> ')}`)
            ]
            return h('div', {}, steps)
          }
        },
        {
          title: '操作',
          fixed: 'right',
          width: 100,
          align: 'center',
          render: (h, params) => {
            return h('Button', {
              props: {
                type: 'primary',
                size: 'small',
                ghost: true
              },
              style: {
                marginRight: '5px'
              },
              on: {
                click: () => {
                  this.clearDataForm()
                  this.editModalTitle = '编辑模版'
                  this.editModal = true
                  this.modalAction = 'update'
                  this.getPublishSteps()
                  this.dataForm = {
                    'id': params.row.id,
                    'name': params.row.name,
                    // 修改opts
                    'deploy_sync_steps': params.row.deploy_sync_steps,
                    'deploy_steps': params.row.deploy_steps,
                    'rollback_steps': params.row.rollback_steps
                  }
                }
              }
            }, '编辑')
          }
        }
      ],
      tableData: [],
      originTableData: [],
      editModal: false,
      editModalTitle: '',
      modalAction: ''
    }
  },
  methods: {
    // 获取所有发布步骤
    getPublishSteps () {
      getSteps().then(res => {
        this.publish_steps = res.data
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    // 删除发布步骤
    handleRemoveStep (e, name) {
      console.log(name)
      deleteStep(name).then(res => {
        this.$Message.success('删除发布步骤成功')
        let index = this.publish_steps.indexOf(name)
        this.publish_steps.splice(index, 1)
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    // 添加发布步骤
    handleAddStep () {
      addStep({
        publish_step: this.control_publish_step
      }).then(res => {
        this.$Message.success('添加发布步骤成功')
        this.publish_steps.push(this.control_publish_step)
        this.control_publish_step = ''
      }).catch(err => {
        sendNotice('error', err)
      })
    },
    searchValue () {
      this.tableData = []
      if (this.templateName === '') {
        this.tableData = this.originTableData
        return
      }
      this.tableData = this.originTableData.filter(item => {
        if (item.name.indexOf(this.templateName) > -1) {
          return item
        }
      })
    },
    selectChange (items) {
      console.log(items)
      this.tableSelection = items
    },
    deleteData () {
      this.tableSelection.forEach(item => {
        deleteOpts(item.id).then(res => {
          this.$Message.success('删除成功')
          this.refreshTable()
        }).catch(err => {
          sendNotice('error', err)
        })
      })
    },
    clearDataForm () {
      this.dataForm = {
        name: '',
        // 修改 opts
        rollback_steps: [],
        deploy_steps: []
      }
    },
    createModal () {
      this.clearDataForm()
      this.editModal = true
      this.editModalTitle = '创建模版'
      this.modalAction = 'create'
      this.getPublishSteps()
    },
    modalOk () {
      this.dataForm.deploy_steps = JSON.stringify(this.dataForm.deploy_steps)
      this.dataForm.rollback_steps = JSON.stringify(this.dataForm.rollback_steps)
      this.dataForm.deploy_sync_steps = JSON.stringify(this.dataForm.deploy_sync_steps)
      if (this.modalAction === 'create') {
        createOpts(this.dataForm).then(res => {
          this.$Message.success('创建成功')
          this.refreshTable()
        }).catch(err => {
          sendNotice('error', err)
        })
      }
      if (this.modalAction === 'update') {
        updateOpts(this.dataForm.id, this.dataForm).then(res => {
          this.$Message.success('更新成功')
          this.refreshTable()
        }).catch(err => {
          sendNotice('error', err)
        })
      }
    },
    refreshTable () {
      this.tableLoading = true
      getOpts().then(res => {
        this.tableData = []
        this.originTableData = []
        res.data.forEach(item => {
          item.deploy_steps = JSON.parse(item.deploy_steps)
          item.rollback_steps = JSON.parse(item.rollback_steps)
          item.deploy_sync_steps = JSON.parse(item.deploy_sync_steps)
          this.tableData.push(item)
          this.originTableData.push(item)
        })
        this.tableLoading = false
      }).catch(err => {
        sendNotice('error', err)
        this.tableLoading = false
      })
    }
  },
  mounted () {
    this.refreshTable()
    this.getPublishSteps()
  }
}
</script>
