import axios from '@/libs/api.request'
var md5 = require('md5')
var header = {
  pp: md5('setting_user')
}

// 获取用户列表
export const getUserList = () => {
  return axios.request({
    url: '/api/v1/users/operations/',
    method: 'get',
    headers: header
  })
}

// 获取组列表
export const getGroupList = () => {
  return axios.request({
    url: '/api/v1/users/group/',
    method: 'get',
    headers: header
  })
}

// 更新密码
export const updateUserPassword = (id, data) => {
  return axios.request({
    url: `/api/v1/users/change-passwd/${id}/`,
    method: 'put',
    data: data,
    headers: header
  })
}

// 更新用户信息
export const updateUserInfo = (id, data) => {
  return axios.request({
    url: `/api/v1/users/operations/${id}/`,
    method: 'put',
    data: data,
    headers: header
  })
}

// 创建用户
export const createUser = (data) => {
  return axios.request({
    url: `/api/v1/users/add/`,
    method: 'post',
    data: data,
    headers: header
  })
}

// 删除用户
export const deleteUser = (id) => {
  return axios.request({
    url: `/api/v1/users/operations/${id}/`,
    method: 'delete',
    headers: header
  })
}
