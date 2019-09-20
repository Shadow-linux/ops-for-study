import axios from '@/libs/api.request'
var md5 = require('md5')
var headers = {
  pp: md5('app_aliveMonitor')
}

// 获取 env 列表
export const getCmdbSetting = () => {
  return axios.request({
    url: `/api/v1/common/setting/cmdb/`,
    method: 'get',
    headers: headers
  })
}

// 获取 app detail 列表
export const getAppDetailList = () => {
  return axios.request({
    url: `/api/v1/app/detail/`,
    method: 'get',
    headers: headers
  })
}

// 获取App alive data
export const getAppAliveData = (data) => {
  return axios.request({
    url: `/api/v1/monitor/app/alive-data/latest/`,
    method: 'post',
    data: {
      http_method: 'GET',
      data: data
    },
    headers: headers
  })
}

// 更新 App alive 是否告警
export const updateAppAliveAlarm = (data) => {
  return axios.request({
    url: `/api/v1/app/alive/urlooker/1/`,
    method: 'put',
    data: data,
    headers: headers
  })
}

// 统计 App Alive
export const tacticsAppAlive = (data) => {
  return axios.request({
    url: `/api/v1/monitor/app/tactics/`,
    method: 'post',
    data: {
      'http_method': 'GET',
      'data': data
    },
    headers: headers
  })
}

// 获取 App Alive graph
export const getAppAliveGraph = (appId, env, checkApi) => {
  return axios.request({
    url: `/api/v1/monitor/app/alive-graph/${appId}/?env=${env}&check_api=${checkApi}`,
    method: 'get'
  })
}
