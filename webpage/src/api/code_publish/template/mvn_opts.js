import axios from '@/libs/api.request'
var md5 = require('md5')
var headers = {
  pp: md5('code_publish_template')
}

// 获取 mvn 列表
export const getOpts = () => {
  return axios.request({
    url: `/api/v1/code-publish/web/mvn-opts/`,
    method: 'get',
    headers: headers
  })
}

// 创建 Opts
export const createOpts = (data) => {
  return axios.request({
    url: `/api/v1/code-publish/web/mvn-opts/`,
    method: 'post',
    data: data,
    headers: headers
  })
}

// 更新 Opts
export const updateOpts = (id, data) => {
  return axios.request({
    url: `/api/v1/code-publish/web/mvn-opts/${id}/`,
    method: 'put',
    data: data,
    headers: headers
  })
}

// 删除 Opts
export const deleteOpts = (id) => {
  return axios.request({
    url: `/api/v1/code-publish/web/mvn-opts/${id}/`,
    method: 'delete',
    headers: headers
  })
}
