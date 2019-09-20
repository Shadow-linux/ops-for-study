import axios from '@/libs/api.request'
// 不需要权限的请求

// 获取消息列表
export const getGlobalSearch = (sval) => {
  return axios.request({
    url: `/api/v1/operation/global-search/?sval=${sval}`,
    method: 'get'
  })
}
