import axios from '@/libs/api.request'
var md5 = require('md5')
var headers = {
  pp: md5('monitor_business_apiQuality')
}

// 获取开放用户列表
export const getUsersList = () => {
  return axios.request({
    url: '/api/v1/users/open/',
    method: 'get',
    headers: headers
  })
}

// 获取所有 access alarm 策略
export const getAccessAlarmStrategy = () => {
  return axios.request({
    url: `/api/v1/business/access-alarm/strategy/`,
    method: 'get',
    headers: headers
  })
}

// 创建 access alarm 策略
export const createAccessAlarmStrategy = (data) => {
  return axios.request({
    url: `/api/v1/business/access-alarm/strategy/`,
    method: 'post',
    data: data,
    headers: headers
  })
}

// 部分更新 access alarm 策略
export const updateAccessAlarmStrategy = (id, data) => {
  return axios.request({
    url: `/api/v1/business/access-alarm/strategy/${id}/`,
    method: 'patch',
    data: data,
    headers: headers
  })
}

// 删除 access alarm 策略
export const deleteAccessAlarmStrategy = (id) => {
  return axios.request({
    url: `/api/v1/business/access-alarm/strategy/${id}/`,
    method: 'delete',
    headers: headers
  })
}
