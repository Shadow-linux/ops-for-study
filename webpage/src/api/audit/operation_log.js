import axios from '@/libs/api.request'
var md5 = require('md5')
var headers = {
  pp: md5('audit_operationLog')
}

// 获取全局操作记录
export const getGlobalOperatingLog = (queryFrom) => {
  var params = ''
  for (var key in queryFrom) {
    params = `${key}=${queryFrom[key]}&&` + params
  }
  return axios.request({
    url: `/api/v1/operation/log/global/?${params}`,
    method: 'get',
    headers: headers
  })
}

// 获取用户列表
export const getUserList = () => {
  return axios.request({
    url: '/api/v1/users/open/',
    method: 'get',
    headers: headers
  })
}

// 删除30天前的操作记录
export const delete30DaysAgo = () => {
  return axios.request({
    url: '/api/v1/operation/log/global/30/',
    method: 'delete',
    headers: headers
  })
}
