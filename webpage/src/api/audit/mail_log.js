import axios from '@/libs/api.request'
var md5 = require('md5')
var headers = {
  pp: md5('audit_messageLog')
}

// 获取用户列表
export const getUserList = () => {
  return axios.request({
    url: '/api/v1/users/operations/',
    method: 'get',
    headers: headers
  })
}

// 获取mail log
export const messageMailLog = () => {
  return axios.request({
    url: `/api/v1/operation/log/message/mail/`,
    method: 'get',
    headers: headers
  })
}

// 删除邮件邮件记录（保留30天）
export const delete30DaysAgo = () => {
  return axios.request({
    url: `/api/v1/operation/log/message/mail/30/`,
    method: 'delete',
    headers: headers
  })
}
