import axios from '@/libs/api.request'
var md5 = require('md5')
var header = {
  pp: md5('setting_commonSetting')
}

// 获取'消息设置'信息
export const getSettingMessage = () => {
  return axios.request({
    url: `/api/v1/common/setting/message/`,
    method: 'get',
    headers: header
  })
}

// 保存'消息设置'信息
export const saveSettingMessage = (data) => {
  var owner = 'global'
  return axios.request({
    url: `/api/v1/common/setting/message/${owner}/`,
    method: 'put',
    data: data,
    headers: header
  })
}

// 测试'消息设置'
export const testSettingMesssage = (action, data) => {
  return axios.request({
    url: `/api/v1/common/setting/message/test/${action}/`,
    method: 'put',
    data: data,
    headers: header
  })
}

// 获取cmdb设置
export const getCmdbSetting = () => {
  return axios.request({
    url: `/api/v1/common/setting/cmdb/`,
    method: 'get',
    headers: header
  })
}

// 更新cmdb设置
export const updateCmdbSetting = (data) => {
  let owner = 'global'
  return axios.request({
    url: `/api/v1/common/setting/cmdb/${owner}/`,
    method: 'put',
    data: data,
    headers: header
  })
}

// 获取 app 设置
export const getAppSetting = () => {
  return axios.request({
    url: `/api/v1/common/setting/app/`,
    method: 'get',
    headers: header
  })
}

// 更新 app 设置
export const updateAppSetting = (data) => {
  let owner = 'global'
  return axios.request({
    url: `/api/v1/common/setting/app/${owner}/`,
    method: 'put',
    data: data,
    headers: header
  })
}

// 获取aliyun access key 列表
export const getAliyunAccessKey = () => {
  return axios.request({
    url: `/api/v1/cmdb/aliyun/keys/`,
    method: 'get',
    headers: header
  })
}

// 添加 aliyun access key 列表
export const addAliyunAccessKey = (data) => {
  return axios.request({
    url: `/api/v1/cmdb/aliyun/keys/`,
    method: 'post',
    data: data,
    headers: header
  })
}

// 删除 aliyun access key
export const deleteAliyunAccessKey = (id) => {
  return axios.request({
    url: `/api/v1/cmdb/aliyun/keys/${id}/`,
    method: 'delete',
    headers: header
  })
}

// 更新 aliyun access key
export const updateAliyunAceessKey = (id, data) => {
  return axios.request({
    url: `/api/v1/cmdb/aliyun/keys/${id}/`,
    method: 'put',
    data: data,
    headers: header
  })
}

export const getSshProxy = () => {
  return axios.request({
    url: `/api/v1/common/setting/ssh-proxy/`,
    method: 'get',
    headers: header
  })
}

export const updateSshProxy = (proxyidc) => {
  return axios.request({
    url: `/api/v1/common/setting/ssh-proxy/`,
    method: 'post',
    headers: header,
    data: {
      proxy_idc: proxyidc
    }
  })
}

export const getCodePublish = () => {
  return axios.request({
    url: `/api/v1/common/setting/code-publish/`,
    method: 'get',
    headers: header
  })
}

export const updateCodePublish = (data) => {
  return axios.request({
    url: `/api/v1/common/setting/code-publish/global/`,
    method: 'put',
    headers: header,
    data: data
  })
}
