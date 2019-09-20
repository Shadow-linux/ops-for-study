import axios from '@/libs/api.request'
let md5 = require('md5')
let headers = {
  pp: md5('cmdb_native_resource')
}

// 获取'cmdb'信息
export const getCmdbInfo = () => {
  return axios.request({
    url: `/api/v1/common/setting/cmdb/`,
    method: 'get',
    headers: headers
  })
}

// 获取 native list
export const getNativeHostList = () => {
  return axios.request({
    url: `/api/v1/cmdb/native/host/`,
    method: 'get',
    headers: headers
  })
}

// 获取 native 分类列表
export const getNativeClassify = (value) => {
  return axios.request({
    url: `/api/v1/cmdb/native/classify/?search=${value}`,
    method: 'get',
    headers: headers
  })
}

// 添加 tag 与 native 关系
export const addNativeHostTagRel = (data) => {
  return axios.request({
    url: `/api/v1/cmdb/tags-rel/native-host/`,
    method: 'post',
    data: data,
    headers: headers
  })
}

// 获取tag 与 native 关系
export const getNativeHostTagRel = (target_id) => {
  return axios.request({
    url: `/api/v1/cmdb/tags-rel/native-host/?target_id=${target_id}`,
    method: 'get',
    headers: headers
  })
}

// 删除 tag 与 native 关系
export const deleteTagRel = (id) => {
  return axios.request({
    url: `/api/v1/cmdb/tags-rel/native-host/${id}/`,
    method: 'delete',
    headers: headers
  })
}

// 获取所有tag
export const getTagsList = () => {
  return axios.request({
    url: `/api/v1/cmdb/tags/`,
    method: 'get',
    headers: headers
  })
}

// 添加host
export const addNativeHostInfo = (data) => {
  return axios.request({
    url: `/api/v1/cmdb/native/host/`,
    method: 'post',
    data: data,
    headers: headers
  })
}

// 更新host
export const updateNativeHostInfo = (id, data) => {
  return axios.request({
    url: `/api/v1/cmdb/native/host/${id}/`,
    method: 'put',
    data: data,
    headers: headers
  })
}

// 获取 Host 单个实例信息
export const readNativeHostInfo = (id) => {
  return axios.request({
    url: `/api/v1/cmdb/native/host/${id}/`,
    method: 'get',
    headers: headers
  })
}

// 删除 ECS 信息
export const deleteNativeHostInfo = (id) => {
  return axios.request({
    url: `/api/v1/cmdb/native/host/${id}/`,
    method: 'delete',
    headers: headers
  })
}

// 通过ansible 更新信息
export const ansibleUpdateNativeHost = (data) => {
  return axios.request({
    url: `/api/v1/cmdb/ansible/update/`,
    method: 'post',
    data: data,
    headers: headers
  })
}

// 通过ansible 自动 添加机器信息
export const ansibleAutoAddNativeHost = (data) => {
  return axios.request({
    url: `/api/v1/cmdb/ansible/add/`,
    method: 'post',
    data: data,
    headers: headers
  })
}

// 获取主机关联的app
export const getNativeHostAppRel = (hostId) => {
  return axios.request({
    url: `/api/v1/cmdb/native/rel/host-app/${hostId}/`,
    method: 'get',
    headers: headers
  })
}
