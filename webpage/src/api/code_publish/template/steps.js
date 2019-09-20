import axios from '@/libs/api.request'
var md5 = require('md5')
var headers = {
  pp: md5('code_publish_template')
}

// 获取 mvn 列表
export const getOpts = () => {
  return axios.request({
    url: `/api/v1/code-publish/web/steps/`,
    method: 'get',
    headers: headers
  })
}

// 创建 Opts
export const createOpts = (data) => {
  return axios.request({
    url: `/api/v1/code-publish/web/steps/`,
    method: 'post',
    data: data,
    headers: headers
  })
}

// 更新 Opts
export const updateOpts = (id, data) => {
  return axios.request({
    url: `/api/v1/code-publish/web/steps/${id}/`,
    method: 'put',
    data: data,
    headers: headers
  })
}

// 删除 Opts
export const deleteOpts = (id) => {
  return axios.request({
    url: `/api/v1/code-publish/web/steps/${id}/`,
    method: 'delete',
    headers: headers
  })
}

// 获取所有发布步骤
export const getSteps = () => {
  return axios.request({
    url: `/api/v1/code-publish/web/setting/steps/`,
    method: 'get',
    headers: headers
  })
}

// 添加发布步骤
export const addStep = (data) => {
  return axios.request({
    url: `/api/v1/code-publish/web/setting/steps/`,
    method: 'post',
    headers: headers,
    data: data
  })
}

// 删除发布步骤
export const deleteStep = (publish_step) => {
  return axios.request({
    url: `/api/v1/code-publish/web/setting/steps/1/?publish_step=${publish_step}`,
    method: 'delete',
    headers: headers
  })
}
