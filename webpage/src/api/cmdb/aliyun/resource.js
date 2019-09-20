import axios from '@/libs/api.request'
let md5 = require('md5')
let headers = {
  pp: md5('cmdb_aliyun_resource')
}

// 获取'cmdb'信息
export const getCmdbInfo = () => {
  return axios.request({
    url: `/api/v1/common/setting/cmdb/`,
    method: 'get',
    headers: headers
  })
}

// 获取 access key 信息
export const getAccessKeyInfo = () => {
  return axios.request({
    url: `/api/v1/cmdb/aliyun/keys/`,
    method: 'get',
    headers: headers
  })
}

// 获取 Ecs 分类信息
export const getClassfiyEcsInfo = (content) => {
  return axios.request({
    url: `/api/v1/cmdb/aliyun/classify/?search=${content}`,
    method: 'get',
    headers: headers
  })
}

// 获取 ECS 所有列表
export const getEcsInfo = () => {
  return axios.request({
    url: `/api/v1/cmdb/aliyun/ecs/`,
    method: 'get',
    headers: headers
  })
}

// 向阿里云更新ecs所有列表
export const updateEcsAllList = (data) => {
  return axios.request({
    url: `/api/v1/cmdb/aliyun/ecs-auto/`,
    method: 'post',
    data: data,
    headers: headers
  })
}

// 更新ECS 信息
export const updateEcsInfo = (id, data) => {
  return axios.request({
    url: `/api/v1/cmdb/aliyun/ecs/${id}/`,
    method: 'put',
    data: data,
    headers: headers
  })
}

// 删除 ECS 信息
export const deleteEcsInfo = (id) => {
  return axios.request({
    url: `/api/v1/cmdb/aliyun/ecs/${id}/`,
    method: 'delete',
    headers: headers
  })
}

// 获取 ECS 单个实例信息
export const readEcsInfo = (id) => {
  return axios.request({
    url: `/api/v1/cmdb/aliyun/ecs/${id}/`,
    method: 'get',
    headers: headers
  })
}

// 获取aliyun tags relation
export const getAliyunEcsTagsRel = (target_id) => {
  return axios.request({
    url: `/api/v1/cmdb/tags-rel/aliyun-ecs/?target_id=${target_id}`,
    method: 'get',
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

// 删除aliyun tag relation
export const deleteAliyunEcsTagRel = (id) => {
  return axios.request({
    url: `/api/v1/cmdb/tags-rel/aliyun-ecs/${id}/`,
    method: 'delete',
    headers: headers
  })
}

// 添加 aliyun tag relation
export const addAliyunEcsTagRel = (data) => {
  return axios.request({
    url: `/api/v1/cmdb/tags-rel/aliyun-ecs/`,
    method: 'post',
    data: data,
    headers: headers
  })
}

// 通过ansible 更新信息
export const ansibleUpdateAliyunEcs = (data) => {
  return axios.request({
    url: `/api/v1/cmdb/ansible/update/`,
    method: 'post',
    data: data,
    headers: headers
  })
}

// 获取主机关联的app
export const getAliyunEcsAppRel = (hostId) => {
  return axios.request({
    url: `/api/v1/cmdb/aliyun/rel/ecs-app/${hostId}/`,
    method: 'get',
    headers: headers
  })
}

// 获取rds 分类信息
// @ac_key_id
// @environment
export const getClassfiyRdsInfo = (search) => {
  return axios.request({
    url: `/api/v1/cmdb/aliyun/rds/classify/?search=${search}`,
    method: 'get',
    headers: headers
  })
}

// 获取rds 全部信息
export const getRdsInfo = () => {
  return axios.request({
    url: `/api/v1/cmdb/aliyun/rds/classify/`,
    method: 'get',
    headers: headers
  })
}

// 修改rds 信息
export const updateRdsInfo = (id, data) => {
  return axios.request({
    url: `/api/v1/cmdb/aliyun/rds/classify/${id}/`,
    method: 'put',
    headers: headers,
    data: data
  })
}
