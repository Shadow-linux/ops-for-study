import axios from '@/libs/api.request'
var md5 = require('md5')
var header = {
  pp: md5('setting_permissionGroup')
}

// 获取组列表
export const getGroupList = () => {
  return axios.request({
    url: '/api/v1/users/group/',
    method: 'get',
    headers: header
  })
}

// 获取用户组权限
export const getGroupPerm = (group_id) => {
  return axios.request({
    url: `/api/v1/permission/group/${group_id}/`,
    method: 'get',
    headers: header
  })
}

// 更新用户组权限
export const updateGroupPerm = (group_id, data) => {
  return axios.request({
    url: `/api/v1/permission/group/${group_id}/`,
    method: 'put',
    data: data,
    headers: header
  })
}

// 添加用户组
export const addGroup = (data) => {
  return axios.request({
    url: `/api/v1/users/group/`,
    method: 'post',
    data: data,
    headers: header
  })
}

// 删除用户组
export const deleteGroup = (group_id) => {
  return axios.request({
    url: `/api/v1/users/group/${group_id}`,
    method: 'delete',
    headers: header
  })
}

// 删除用户组权限
export const deleteGroupPerm = (group_id) => {
  return axios.request({
    url: `/api/v1/permission/group/${group_id}/`,
    method: 'delete',
    headers: header
  })
}
