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
      <Col span="6" offset="8">
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
      v-model="editModal"
      :title="editModalTitle"
      @on-ok="modalOk"
      width="1200"
      >
      <Form ref="" :model="dataForm" :label-width="100" inline>
        <FormItem label="模版名字:">
          <Input v-model.trim="dataForm.name" placeholder="通用参数" style="width: 1050px"></Input>
        </FormItem>
        <FormItem label="模版:">
          <Input v-model="dataForm.gradle_opts" type="textarea" :rows="10" style="width: 1050px"></Input>
        </FormItem>
      </Form>
    </Modal>
  </div>
</template>
<script>
// 需修改
import { getOpts, createOpts, deleteOpts, updateOpts } from '@/api/code_publish/template/gradle_opts'
import { sendNotice } from '@/libs/util.js'

export default {
  // 修改
  name: 'tmpl_gradle_opts',
  data () {
    return {
      templateName: '',
      dataForm: {
        name: '',
        // 修改opts
        gradle_opts: ''
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
          width: 200,
          tooltip: true
        },
        {
          title: 'Template',
          // 需修改
          key: 'gradle_opts',
          tooltip: true
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
                  this.dataForm = {
                    'id': params.row.id,
                    'name': params.row.name,
                    // 修改opts
                    'gradle_opts': params.row.gradle_opts
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
        gradle_opts: ''
      }
    },
    createModal () {
      this.clearDataForm()
      this.editModal = true
      this.editModalTitle = '创建模版'
      this.modalAction = 'create'
    },
    modalOk () {
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
        this.tableData = res.data
        this.originTableData = res.data
        this.tableLoading = false
      }).catch(err => {
        sendNotice('error', err)
        this.tableLoading = false
      })
    }
  },
  mounted () {
    this.refreshTable()
  }
}
</script>
