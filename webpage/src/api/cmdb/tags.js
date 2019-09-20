import axios from '@/libs/api.request'
let md5 = require('md5')
let headers = {
  pp: md5('cmdb_tag')
}

// 获取 tags list 信息
export const getTagsList = () => {
  return axios.request({
    url: `/api/v1/cmdb/tags/`,
    method: 'get',
    headers: headers
  })
}

// 删除 tag
export const deleteTag = (id) => {
  return axios.request({
    url: `/api/v1/cmdb/tags/${id}/`,
    method: 'delete',
    headers: headers
  })
}

// 添加 tag
export const addTag = (data) => {
  return axios.request({
    url: `/api/v1/cmdb/tags/`,
    method: 'post',
    data: data,
    headers: headers
  })
}
