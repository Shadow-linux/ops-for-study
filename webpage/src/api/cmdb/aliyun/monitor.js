import axios from '@/libs/api.request'
var md5 = require('md5')
var headers = {
  pp: md5('cmdb_aliyun_monitor')
}

// 获取 access key 信息
export const getAccessKeyInfo = () => {
  return axios.request({
    url: `/api/v1/cmdb/aliyun/keys/`,
    method: 'get',
    headers: headers
  })
}

// 通过access key id 获取 ecs 信息
export const getAccessKey2Ecs = (acKeyId) => {
  return axios.request({
    url: `/api/v1/cmdb/aliyun/key2ecs/?ac_key_id=${acKeyId}`,
    method: 'get',
    headers: headers
  })
}

// 通过access key id 获取 ecs 信息
export const getAccessKey2Rds = (acKeyId) => {
  return axios.request({
    url: `/api/v1/cmdb/aliyun/key2rds/?ac_key_id=${acKeyId}`,
    method: 'get',
    headers: headers
  })
}

// 获取监控数据
export const getGraphdata = (key_name, action, kwargs) => {
  return axios.request({
    url: `/api/v1/cmdb/aliyun/graph/${key_name}/?action=${action}&kwargs=${kwargs}`,
    method: 'get',
    headers: headers
  })
}

// 获取RDS 监控数据
export const getRdsGraphData = (rds_id, metric_name, start_time, end_time) => {
  return axios.request({
    url: `/api/v1/cmdb/aliyun/rds/graph/${rds_id}/?metric_name=${metric_name}&start_time=${start_time}&end_time=${end_time}`,
    method: 'get',
    headers: headers
  })
}

// 获取 rds process list数据
export const getRdsProcessList = (rds_id) => {
  return axios.request({
    url: `/api/v1/cmdb/aliyun/rds/processlist/${rds_id}/`,
    method: 'get',
    headers: headers
  })
}
