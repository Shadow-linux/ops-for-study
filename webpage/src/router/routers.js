import Main from '@/components/main'
import parentView from '@/components/parent-view'

/**
 * iview-admin中meta除了原生参数外可配置的参数:
 * meta: {
 *  title: { String|Number|Function }
 *         显示在侧边栏、面包屑和标签栏的文字
 *         使用'{{ 多语言字段 }}'形式结合多语言使用，例子看多语言的路由配置;
 *         可以传入一个回调函数，参数是当前路由对象，例子看动态路由和带参路由
 *  hideInBread: (false) 设为true后此级路由将不会出现在面包屑中，示例看QQ群路由配置
 *  hideInMenu: (false) 设为true后在左侧菜单不会显示该页面选项
 *  notCache: (false) 设为true后页面在切换标签后不会缓存，如果需要缓存，无需设置这个字段，而且需要设置页面组件name属性和路由配置的name一致
 *  access: (null) 可访问该页面的权限数组，当前路由设置的权限会影响子路由
 *  icon: (-) 该页面在左侧菜单、面包屑和标签导航处显示的图标，如果是自定义图标，需要在图标名称前加下划线'_'
 *  beforeCloseName: (-) 设置该字段，则在关闭当前tab页时会去'@/router/before-close.js'里寻找该字段名对应的方法，作为关闭前的钩子函数,
 *  showAlways: (false) 如果子菜单都没有权限，就不显示该级菜单
 * }
 * 命名规范:
 *  path: level-one
 *  name: levelOne_levelTwo_levelThree
 */

export default [
  {
    path: '/login',
    name: 'login',
    meta: {
      title: 'Login - 登录',
      hideInMenu: true
    },
    component: () => import('@/view/login/login.vue')
  },
  {
    path: '/',
    name: '_home',
    redirect: '/home',
    component: Main,
    meta: {
      hideInMenu: true,
      notCache: true
    },
    children: [
      {
        path: '/home',
        name: 'home',
        meta: {
          access: ['home'],
          hideInMenu: true,
          title: '首页',
          notCache: true,
          icon: 'ios-home'
        },
        component: () => import('@/view/single-page/home')
      },
      {
        path: '/search',
        name: 'search',
        meta: {
          title: route => `全局搜索`,
          notCache: true,
          icon: 'ios-search'
        },
        component: () => import('@/view/single-page/search')
      }
    ]
  },
  {
    path: '',
    name: 'doc',
    meta: {
      hideInMenu: true,
      title: '文档',
      href: 'https://lison16.github.io/iview-admin-doc/#/',
      icon: 'ios-book'
    }
  },
  {
    path: '/owner',
    name: 'owner',
    component: Main,
    meta: {
      hideInBread: true,
      hideInMenu: true
    },
    children: [
      {
        path: 'message_page',
        name: 'message_page',
        meta: {
          icon: 'md-notifications',
          title: '消息中心',
          notCache: true
        },
        component: () => import('@/view/single-page/message/index.vue')
      },
      {
        path: 'personal_center',
        name: 'personal_center',
        meta: {
          icon: '',
          title: '个人中心'
        },
        component: () => import('@/view/single-page/personal_center/index.vue')
      }
    ]
  },
  {
    path: '/tools_methods',
    name: 'tools_methods',
    meta: {
      hideInBread: true,
      hideInMenu: true
    },
    component: Main,
    children: [
      {
        path: 'tools_methods_page',
        name: 'tools_methods_page',
        meta: {
          icon: 'ios-hammer',
          title: '工具方法',
          beforeCloseName: 'before_close_normal'
        },
        component: () => import('@/view/tools-methods/tools-methods.vue')
      }
    ]
  },
  {
    path: '/argu',
    name: 'argu',
    meta: {
      hideInMenu: true
    },
    component: Main,
    children: [
      {
        path: 'params/:id',
        name: 'params',
        meta: {
          icon: 'md-flower',
          title: route => `Aliyun-${route.params.id}`,
          notCache: true,
          beforeCloseName: 'before_close_normal'
        },
        component: () => import('@/view/argu-page/params.vue')
      },
      {
        path: 'query',
        name: 'query',
        meta: {
          icon: 'md-flower',
          // notCache: true,
          title: route => `{{ query }}-${route.query.id}`
        },
        component: () => import('@/view/argu-page/query.vue')
      }
    ]
  },
  {
    path: '/cmdb',
    name: 'cmdb',
    meta: {
      icon: '_CMDB',
      showAlways: true,
      title: 'CMDB',
      access: ['cmdb']
    },
    component: Main,
    children: [
      {
        path: 'aliyun',
        name: 'aliyun',
        meta: {
          icon: '_aliyun',
          title: '阿里云',
          showAlways: true
        },
        component: parentView,
        children: [
          {
            path: 'resource',
            name: 'cmdb_aliyun_resource',
            meta: {
              icon: 'logo-buffer',
              title: '资源 (aliyun)',
              access: ['cmdb_aliyun_resource'],
              notCache: true
            },
            component: () => import('@/view/cmdb/aliyun/resource.vue')
          },
          {
            path: 'monitor',
            name: 'cmdb_aliyun_monitor',
            meta: {
              icon: 'ios-pulse',
              title: '监控 (aliyun)',
              access: ['cmdb_aliyun_monitor']
            },
            component: () => import('@/view/cmdb/aliyun/monitor.vue')
          }
        ]
      },
      {
        path: 'native',
        name: 'native',
        meta: {
          icon: 'ios-pin',
          title: '本地机房',
          showAlways: true
        },
        component: parentView,
        children: [
          {
            path: 'resource',
            name: 'cmdb_native_resource',
            meta: {
              icon: 'logo-buffer',
              title: '资源 (native)',
              access: ['cmdb_native_resource'],
              notCache: true
            },
            component: () => import('@/view/cmdb/native/resource.vue')
          },
          {
            path: 'monitor',
            name: 'cmdb_native_monitor',
            meta: {
              icon: 'ios-pulse',
              title: '监控 (naitive)',
              access: ['cmdb_native_monitor']
            },
            component: () => import('@/view/cmdb/native/monitor.vue')
          }
        ]
      },
      {
        path: '/resource',
        name: 'resource',
        meta: {
          hideInMenu: true,
          notCache: true
        },
        component: parentView,
        children: [
          {
            path: 'host/:id',
            name: 'cmdb_host_info',
            meta: {
              icon: 'md-browsers',
              title: route => `${route.query.hostname}`,
              access: ['cmdb_native_resource', 'cmdb_aliyun_resource']
            },
            component: () => import('@/view/cmdb/common/single_instance.vue')
          }
        ]
      },
      {
        path: 'tags',
        name: 'cmdb_tags',
        meta: {
          icon: 'ios-pricetag',
          title: '标签',
          access: ['cmdb_tag']
        },
        component: () => import('@/view/cmdb/tags.vue')
      }
    ]
  },
  {
    path: '/apps',
    name: 'apps',
    meta: {
      icon: 'ios-appstore-outline',
      showAlways: true,
      title: 'App',
      access: ['app']
    },
    component: Main,
    children: [
      {
        path: 'management',
        name: 'app_management',
        meta: {
          icon: 'ios-apps',
          title: 'App 管理',
          access: ['app_management'],
          notCache: true
        },
        component: () => import('@/view/apps/app_management.vue')
      },
      {
        path: 'alive-monitor',
        name: 'app_aliveMonitor',
        meta: {
          icon: 'ios-pulse',
          title: 'App Alive 监控',
          access: ['app_aliveMonitor'],
          notCache: true
        },
        component: () => import('@/view/apps/app_alive_monitor.vue')
      },
      {
        path: '',
        name: '',
        meta: {
          hideInMenu: true,
          notCache: true
        },
        component: parentView,
        children: [
          {
            path: 'app/:id',
            name: 'apps_app_detail',
            meta: {
              icon: 'md-browsers',
              title: route => `${route.query.app_name}`
            },
            component: () => import('@/view/apps/single_app_detail.vue')
          }
        ]
      }
    ]
  },
  {
    path: '/code-publish',
    name: 'code-publish',
    meta: {
      icon: 'md-code-working',
      showAlways: true,
      title: '代码发布',
      access: ['code_publish']
    },
    component: Main,
    children: [
      {
        path: 'publish',
        name: 'code_publish_publish',
        meta: {
          icon: 'ios-paper-plane',
          title: '发布',
          access: ['code_publish_issue'],
          notCache: true
        },
        component: () => import('@/view/code_publish/publish.vue')
      },
      {
        path: 'config',
        name: 'code_publish_conf',
        meta: {
          icon: 'ios-options',
          title: '发布配置',
          access: ['code_publish_config'],
          notCache: true
        },
        component: () => import('@/view/code_publish/config.vue')
      },
      {
        path: 'template',
        name: 'code_publish_template',
        meta: {
          icon: 'ios-paper',
          title: '模版配置',
          access: ['code_publish_template'],
          notCache: true
        },
        component: () => import('@/view/code_publish/template.vue')
      }
    ]
  },
  {
    path: '/monitor',
    name: 'monitor',
    meta: {
      icon: 'ios-podium',
      showAlways: true,
      title: '监控中心',
      access: ['monitor']
    },
    component: Main,
    children: [
      {
        path: 'business',
        name: 'monitor_business',
        meta: {
          icon: 'ios-briefcase',
          showAlways: true,
          title: '业务监控'
        },
        component: parentView,
        children: [
          {
            path: 'resource',
            name: 'monitor_business_apiQuality',
            meta: {
              icon: 'ios-cloud-done',
              title: 'API 质量监控',
              access: ['monitor_business_apiQuality']
            },
            component: () => import('@/view/monitor/business/api_quality.vue')
          }
        ]
      },
      {
        path: 'kibana',
        name: 'monitor_kibana',
        meta: {
          icon: '_kibana',
          showAlways: true,
          title: 'Kibana 统计信息'
        },
        component: parentView,
        children: [
          {
            path: 'pre-access-nginx',
            name: 'monitor_kibana_preAccessNginx',
            meta: {
              icon: '_nginx',
              title: 'Pre Access Nginx',
              access: ['monitor_kibana_preAccessNginx']
            },
            component: () => import('@/view/monitor/kibana/kibana_pre_access_nginx.vue')
          }
        ]
      },
      {
        path: 'third-party',
        name: 'monitor_thirdparty',
        meta: {
          icon: 'ios-link',
          title: '服务监控 (第三方)',
          access: ['monitor_thirdParty']
        },
        component: () => import('@/view/monitor/third_party.vue')
      },
      {
        path: 'docker',
        name: 'monitor_docker',
        meta: {
          icon: '_docker',
          title: 'Docker 监控',
          access: ['monitor_docker']
        },
        component: () => import('@/view/monitor/docker.vue')
      },
      {
        path: '',
        name: 'single',
        meta: {
          hideInMenu: true,
          notCache: true
        },
        component: parentView,
        children: [
          {
            path: 'strategy',
            name: 'monitor_thirdPartyStrategy',
            meta: {
              icon: 'md-options',
              title: '监控策略（第三方）',
              notCache: true
            },
            component: () => import('@/view/monitor/third_party_strategy.vue')
          }
        ]
      }
    ]
  },
  {
    path: '/audit',
    name: 'audit',
    meta: {
      icon: 'ios-locate-outline',
      showAlways: true,
      title: '审计',
      access: ['audit']
    },
    component: Main,
    children: [
      {
        path: 'operation-log',
        name: 'audit_operationLog',
        meta: {
          icon: 'ios-paper',
          title: '全局操作记录',
          access: ['audit_operationLog']
        },
        component: () => import('@/view/audit/operating_log.vue')
      },
      {
        path: 'send-message-log',
        name: 'audit_sendMessageLog',
        meta: {
          icon: 'ios-chatbubbles',
          title: '消息日志',
          access: ['audit_messageLog']
        },
        component: () => import('@/view/audit/send_message_log.vue')
      }
    ]
  },
  {
    path: '/setting',
    name: 'setting',
    meta: {
      icon: 'ios-settings',
      title: '全局设置',
      showAlways: true,
      access: ['setting']
    },
    component: Main,
    children: [
      {
        path: 'setting',
        name: 'setting_setting',
        meta: {
          title: '通用设置',
          icon: 'ios-cog-outline',
          access: ['setting_commonSetting']
        },
        component: () => import('@/view/setting/common_setting.vue')
      },
      {
        path: 'user',
        name: 'setting_user',
        meta: {
          title: '用户管理',
          icon: 'ios-person',
          access: ['setting_user'],
          notCache: true
        },
        component: () => import('@/view/setting/user.vue')
      },
      {
        path: 'permission-group',
        name: 'setting_permissionGroup',
        meta: {
          title: '权限组',
          icon: 'ios-people',
          access: ['setting_permissionGroup'],
          notCache: true
        },
        component: () => import('@/view/setting/permission_group.vue')
      },
      {
        path: 'message',
        name: 'setting_sendMessage',
        meta: {
          title: '消息推送',
          icon: 'ios-send',
          access: ['setting_sendMessage']
        },
        component: () => import('@/view/setting/send_message.vue')
      }
    ]
  },
  {
    path: '/401',
    name: 'error_401',
    meta: {
      hideInMenu: true
    },
    component: () => import('@/view/error-page/401.vue')
  },
  {
    path: '/500',
    name: 'error_500',
    meta: {
      hideInMenu: true
    },
    component: () => import('@/view/error-page/500.vue')
  },
  {
    path: '*',
    name: 'error_404',
    meta: {
      hideInMenu: true
    },
    component: () => import('@/view/error-page/404.vue')
  }
]
