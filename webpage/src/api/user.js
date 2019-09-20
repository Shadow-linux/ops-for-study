import axios from '@/libs/api.request'

// 登录
export const login = ({ username, password }) => {
  const data = {
    username,
    password
  }
  return axios.request({
    url: '/api/v1/users/login/',
    data,
    method: 'post'
  })
}

// 获取页面权限
export const getUserInfo = (token) => {
  return axios.request({
    url: '/api/v1/permission/page/check/',
    params: {
      token
    },
    method: 'get'
  })
}

// 注册用户
export const registerUser = (data) => {
  return axios.request({
    url: '/api/v1/users/register/',
    method: 'post',
    data: data
  })
}

// 登出
export const logout = (token) => {
  return axios.request({
    url: 'logout',
    method: 'post'
  })
}

// 获取未读的站内消息
export const getUnreadCount = () => {
  return axios.request({
    url: '/api/v1/message/count',
    method: 'get'
  })
}

// 获取消息列表
export const getMessage = () => {
  return axios.request({
    url: '/api/v1/message/inner/',
    method: 'get'
  })
}

// 获取消息内容
export const getContentByMsgId = msg_id => {
  return axios.request({
    url: `/api/v1/message/inner/${msg_id}/`,
    method: 'get'
  })
}

// 设置为已读消息
export const hasRead = msg_id => {
  return axios.request({
    url: `/api/v1/message/operation/${msg_id}/`,
    method: 'put',
    data: {
      status: 2
    }
  })
}

// 删除已读消息
export const removeReaded = msg_id => {
  return axios.request({
    url: `/api/v1/message/operation/${msg_id}/`,
    method: 'put',
    data: {
      status: 0
    }
  })
}

// 恢复回收站消息
export const restoreTrash = msg_id => {
  return axios.request({
    url: `/api/v1/message/operation/${msg_id}/`,
    method: 'put',
    data: {
      status: 2
    }
  })
}

// 获取个人中心信息
export const getPersonalInfo = (userId) => {
  return axios.request({
    url: `/api/v1/personal/info/${userId}/`,
    method: 'get'
  })
}

// 更新个人中心信息
export const updatePersonalInfo = (userId, data) => {
  return axios.request({
    url: `/api/v1/personal/info/${userId}/`,
    method: 'put',
    data: data
  })
}

// 更新个人中心密码
export const updatePersonalPassword = (userId, data) => {
  return axios.request({
    url: `/api/v1/personal/password/${userId}/`,
    method: 'put',
    data: data
  })
}
