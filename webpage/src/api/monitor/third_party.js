import axios from '@/libs/api.request'
var md5 = require('md5')
var headers = {
  pp: md5('monitor_thirdParty')
}

// 获取 ecs 信息
export const getEcsInfo = () => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/ecs/`,
    method: 'get',
    headers: headers
  })
}

// 删除 ecs 信息
export const deleteEcsInfo = (id) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/ecs/${id}/`,
    method: 'delete',
    headers: headers
  })
}

// 更新 ecs 是否监控
export const updateEcsInfoMonitor = (id, isMonitor) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/ecs/${id}/`,
    method: 'put',
    data: {
      'is_monitor': isMonitor
    },
    headers: headers
  })
}

// 获取 rds 信息
export const getRdsInfo = () => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/rds/`,
    method: 'get',
    headers: headers
  })
}

// 删除 rds 信息
export const deleteRdsInfo = (id) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/rds/${id}/`,
    method: 'delete',
    headers: headers
  })
}

// 更新 rds 信息是否监控
export const updateRdsInfoMonitor = (id, isMonitor) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/rds/${id}/`,
    method: 'put',
    data: {
      'is_monitor': isMonitor
    },
    headers: headers
  })
}

// 获取 nas 信息
export const getNasInfo = () => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/nas/`,
    method: 'get',
    headers: headers
  })
}

// 删除 nas 信息
export const deleteNasInfo = (id) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/nas/${id}/`,
    method: 'delete',
    headers: headers
  })
}

// 更新 nas 信息是否监控
export const updateNasInfoMonitor = (id, isMonitor) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/nas/${id}/`,
    method: 'put',
    data: {
      'is_monitor': isMonitor
    },
    headers: headers
  })
}

// 获取 domain 信息
export const getDomainInfo = () => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/domain/`,
    method: 'get',
    headers: headers
  })
}

// 删除 domain 信息
export const deleteDomainInfo = (id) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/domain/${id}/`,
    method: 'delete',
    headers: headers
  })
}

// 更新 domain 信息是否监控
export const updateDomainInfoMonitor = (id, isMonitor) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/domain/${id}/`,
    method: 'put',
    data: {
      'is_monitor': isMonitor
    },
    headers: headers
  })
}

// 获取 vpn 信息
export const getVpnInfo = () => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/vpn/`,
    method: 'get',
    headers: headers
  })
}

// 删除 vpn 信息
export const deleteVpnInfo = (id) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/vpn/${id}/`,
    method: 'delete',
    headers: headers
  })
}

// 更新 vpn 信息是否监控
export const updateVpnInfoMonitor = (id, isMonitor) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/vpn/${id}/`,
    method: 'put',
    data: {
      'is_monitor': isMonitor
    },
    headers: headers
  })
}

// 获取 tencent sms 信息
export const getTencentSmsInfo = () => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/tencent-sms/`,
    method: 'get',
    headers: headers
  })
}

// 删除 tencent sms 信息
export const deleteTencentSmsInfo = (id) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/tencent-sms/${id}/`,
    method: 'delete',
    headers: headers
  })
}

// 更新 tencent sms 信息是否监控
export const updateTencentSmsInfoMonitor = (id, isMonitor) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/tencent-sms/${id}/`,
    method: 'put',
    data: {
      'is_monitor': isMonitor
    },
    headers: headers
  })
}

// 获取 万维易源 银行卡身份证实名认证 第三方监控信息
export const getWanweiyiyuanBankidentityInfo = () => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/wanweiyiyuan-bankidentity/`,
    method: 'get',
    headers: headers
  })
}

// 删除 万维易源 银行卡身份证实名认证 第三方监控信息
export const deleteWanweiyiyuanBankidentityInfo = (id) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/wanweiyiyuan-bankidentity/${id}/`,
    method: 'delete',
    headers: headers
  })
}

// 更新 万维易源 银行卡身份证实名认证 第三方监控信息 是否监控
export const updateWanweiyiyuanBankidentityInfoMonitor = (id, isMonitor) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/wanweiyiyuan-bankidentity/${id}/`,
    method: 'put',
    data: {
      'is_monitor': isMonitor
    },
    headers: headers
  })
}

// 获取 寻程 二要素 第三方监控信息
export const getXunchengEryaosuInfo = () => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/xuncheng-eryaosu/`,
    method: 'get',
    headers: headers
  })
}

// 删除 寻程 二要素 第三方监控信息
export const deleteXunchengEryaosuInfo = (id) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/xuncheng-eryaosu/${id}/`,
    method: 'delete',
    headers: headers
  })
}

// 删除 寻程 二要素 第三方监控信息 是否监控
export const updateXunchengEryaosuInfoMonitor = (id, isMonitor) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/xuncheng-eryaosu/${id}/`,
    method: 'put',
    data: {
      'is_monitor': isMonitor
    },
    headers: headers
  })
}

// 获取 yuexin 短信 第三方监控信息
export const getYuexinSmsInfo = () => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/yuexin-sms/`,
    method: 'get',
    headers: headers
  })
}

// 获取 yuexin 短信 第三方监控信息
export const deleteYuexinSmsInfo = (id) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/yuexin-sms/${id}/`,
    method: 'delete',
    headers: headers
  })
}

// 获取 yuexin 短信 第三方监控信息
export const updateYuexinSmsInfoMonitor = (id, isMonitor) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/info/yuexin-sms/${id}/`,
    method: 'put',
    data: {
      'is_monitor': isMonitor
    },
    headers: headers
  })
}

// 获取 第三方图表 信息
export const getTPChartData = (id, monitorItem, days) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/graph/?id=${id}&monitor_item=${monitorItem}&days=${days}`,
    method: 'get',
    headers: headers
  })
}

// 获取 第三方监控 基础策略
export const getTPStrategy = () => {
  return axios.request({
    url: `/api/v1/monitor/third-party/strategy/`,
    method: 'get',
    headers: headers
  })
}

// 创建 第三方监控 基础策略
export const createTPStrategy = (data) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/strategy/`,
    method: 'post',
    data: data,
    headers: headers
  })
}

// 更新 第三方监控策略
export const updateTPStrategy = (id, data) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/strategy/${id}/`,
    method: 'put',
    data: data,
    headers: headers
  })
}

// 删除 第三方监控策略
export const deleteTPStrategy = (id) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/strategy/${id}/`,
    method: 'delete',
    headers: headers
  })
}

// 获取 第三方监控 抖动策略
export const getTPJitterStrategy = () => {
  return axios.request({
    url: `/api/v1/monitor/third-party/jitter-strategy/`,
    method: 'get',
    headers: headers
  })
}

// 创建 第三方监控 抖动策略
export const createTPJitterStrategy = (data) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/jitter-strategy/`,
    method: 'post',
    data: data,
    headers: headers
  })
}

// 更新 第三方监控 抖动策略
export const updateTPJitterStrategy = (id, data) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/jitter-strategy/${id}/`,
    method: 'put',
    data: data,
    headers: headers
  })
}

// 删除 第三方监控 抖动策略
export const deleteTPJitterStrategy = (id) => {
  return axios.request({
    url: `/api/v1/monitor/third-party/jitter-strategy/${id}/`,
    method: 'delete',
    headers: headers
  })
}

// 获取 用户基础信息列表
export const getOpenUserList = () => {
  return axios.request({
    url: `/api/v1/users/open/`,
    method: 'get',
    headers: headers
  })
}

// 获取第三方监控 基础项目
export const getTPBaseItem = () => {
  return axios.request({
    url: `/api/v1/monitor/third-party/item/strategy-base/`,
    method: 'get',
    headers: headers
  })
}

// 获取第三方监控 基础项目
export const getTPJitterItem = () => {
  return axios.request({
    url: `/api/v1/monitor/third-party/item/strategy-jitter/`,
    method: 'get',
    headers: headers
  })
}

// 更新本地第三方监控信息，不推送到falcon
export const updateTPData = () => {
  return axios.request({
    url: `/api/v1/monitor/third-party/data/`,
    method: 'put',
    headers: headers
  })
}
