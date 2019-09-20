import axios from '@/libs/api.request'
var md5 = require('md5')
var header = {
  pp: md5('setting_sendMessage')
}

// 获取消息推送记录
export const getPushMessage = () => {
  return axios.request({
    url: `/api/v1/message/push/`,
    method: 'get',
    headers: header
  })
}

// 创建推送消息
export const createPushMessage = (data) => {
  return axios.request({
    url: `/api/v1/message/push/`,
    method: 'post',
    data: data,
    headers: header
  })
}

// 获取推送消息用户列表
export const getMessageUserList = () => {
  return axios.request({
    url: '/api/v1/users/operations/',
    method: 'get',
    headers: header
  })
}
