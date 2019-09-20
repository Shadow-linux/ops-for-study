import axios from '@/libs/api.request'
var md5 = require('md5')
var headers = {
  pp: md5('app_management')
}

// 获取 app detail 信息
export const getAppDetail = () => {
  return axios.request({
    url: '/api/v1/app/detail/',
    method: 'get',
    headers: headers
  })
}

// 获取单个 app detail 信息
export const getSingleAppDetail = (id) => {
  return axios.request({
    url: `/api/v1/app/detail/${id}/`,
    method: 'get',
    headers: headers
  })
}

// 创建app detail 信息
export const createAppDetail = (data) => {
  return axios.request({
    url: '/api/v1/app/detail/',
    method: 'post',
    data: data,
    headers: headers
  })
}

// 更新 app detail 信息
export const updateAppDetail = (id, data) => {
  return axios.request({
    url: `/api/v1/app/detail/${id}/`,
    method: 'put',
    data: data,
    headers: headers
  })
}

// 删除单个 app
export const deleteAppDetail = (id) => {
  return axios.request({
    url: `/api/v1/app/detail/${id}/`,
    method: 'delete',
    headers: headers
  })
}

// 创建urlooker app alive 监控
export const createUrlookerAppAlive = (data) => {
  return axios.request({
    url: `/api/v1/app/alive/urlooker/`,
    method: 'post',
    data: data,
    headers: headers
  })
}

// 更新 urlooker app alive 是否告警
export const updateUrlookerAppAliveAlarm = (id, data) => {
  return axios.request({
    url: `/api/v1/app/alive/urlooker/${id}`,
    method: 'put',
    data: data,
    headers: headers
  })
}

// 删除 urlooker app alive 监控信息
export const deleteUrlookerAppAlive = (id) => {
  return axios.request({
    url: `/api/v1/app/alive/urlooker/${id}`,
    method: 'delete',
    headers: headers
  })
}

// 获取所有hosts
export const getAllHosts = () => {
  return axios.request({
    url: `/api/v1/cmdb/common/all-hosts/`,
    method: 'get',
    headers: headers
  })
}

// 获取开放用户
export const getAllUsers = () => {
  return axios.request({
    url: `/api/v1/users/open/`,
    method: 'get',
    headers: headers
  })
}

// 获取app 对应的hosts
export const getAppHostRel = (id) => {
  return axios.request({
    url: `/api/v1/app/rel/host/${id}/`,
    method: 'get',
    headers: headers
  })
}

// 获取 env 列表
export const getCmdbSetting = () => {
  return axios.request({
    url: `/api/v1/common/setting/cmdb/`,
    method: 'get',
    headers: headers
  })
}

// 获取 service list
export const getServiceList = () => {
  return axios.request({
    url: `/api/v1/common/setting/app/`,
    method: 'get',
    headers: headers
  })
}

// 获取 app 设置
export const getAppSetting = () => {
  return axios.request({
    url: `/api/v1/common/setting/app/`,
    method: 'get',
    headers: headers
  })
}
