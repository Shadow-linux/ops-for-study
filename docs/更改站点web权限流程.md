### 准备

`本内容如有疑问，请阅读源码或询问开发者` 

```
权限命名:  level1_level2_level3
如: audit_operationLog (审计 -> 全局操作记录)
以下示例全部以 audit_operationLog 开展
```

### 页面修改(前端)

**webpage/src/components/setting/permission_group/components/mPagePerm.vue (修改权限的modal)**

1 . 添加html 

```
<Divider orientation="left" class="inner-divider-text">审计</Divider>  // 一级目录，判断是否可见
	<FormItem label="是否可见">
	    <Checkbox v-model="formData.audit">是</Checkbox>
	  </FormItem>
	<FormItem label="全局操作记录">
	  <RadioGroup v-model="formData.audit_operationLog">。 // 二级目录, 从二级目录开始需要划分读写权限
	    <Radio label='0' >无</Radio>
	    <Radio label='1'>只读</Radio>
	    <Radio label='2'>读写</Radio>
	  </RadioGroup>
	</FormItem>
```

2. 添加js

```
data () {
	return {
		...
		// 可视目录，新目录需要添加, 只需添加1级目录
      	visiblePerm: ['setting', 'audit'],
      	formData: {
        home: 1,
        audit: 0,
        audit_operationLog: 0,   // 添加 0 即可
        setting: 0,
        setting_user: 0,
        setting_permissionGroup: 0,
        setting_sendMessage: 0
      }
	}
}
```

**webpage/src/components/setting/permission_group/pagePermModal.vue (查看权限的modal)**
1. 添加html
```
<Divider orientation="left" class="inner-divider-text">审计 <b class="none-perm-tag">( {{ perm.audit.tag }} )</b></Divider>  // 一级目录
	<FormItem label="全局操作记录">									// 二级目录
	<span :class="{ 'rw-perm-tag': perm.audit_operationLog.rw,
	  'ro-perm-tag': perm.audit_operationLog.ro,
	  'none-perm-tag': perm.audit_operationLog.none
	  }">{{ perm.audit_operationLog.tag }}</span>
	</FormItem>
```

2. 添加js

```
data () {
    return {
      // home 是不需要放在visiblePerm里，因为home是永远可见，只需添加一级目录
      visiblePerm: ['setting', 'audit'],
      perm: {
        home: { tag: '无', ro: false, rw: false, none: true },
        setting: { tag: '无', ro: false, rw: false, none: true },
        setting_user: { tag: '无', ro: false, rw: false, none: true },
        setting_permissionGroup: { tag: '无', ro: false, rw: false, none: true },
        setting_sendMessage: { tag: '无', ro: false, rw: false, none: true },
        audit: { tag: '无', ro: false, rw: false, none: true },
        audit_operationLog: { tag: '无', ro: false, rw: false, none: true } //
      }
    }
  }
```

**另外还需在 src/router/router.js 和 src/api/data.js 中使用**
* router.js

```
{
	path: 'operation-log',
	name: 'audit_operationLog',
	meta: {
	  icon: 'ios-film',
	  title: '全局操作记录',
	  access: ['audit_operationLog']
	},
	component: () => import('@/view/audit/operating_log.vue')
}
```
* data.js


参照其他api 即可, 需要添加header ，用于权限传递


### 程序修改(后端)

* **src/public/permission/perms (添加权限组时使用的模版)**

```
# 数据格式
#   key 格式: level1_level2_level3
#   value: 0 是不具有权限，1 只读， 2 读写
PAGE_PERMS_TEMPLATE = {
    'home': 1,
    'setting': 0,
    'setting_user': 0,
    'setting_permissionGroup': 0,
    'setting_sendMessage': 0,
    'audit': 0,
    'audit_operationLog': 0
}
```

* **还需为对应的ViewSet 加上 src/public/permission/perms 下的 IsPagePermissionRW 这是一个permission_class, 如不懂请阅读源码**


### 最后重新在权限组页面上点就修改，更新下新的权限即可








