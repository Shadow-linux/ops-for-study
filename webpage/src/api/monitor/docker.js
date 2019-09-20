import axios from '@/libs/api.request'
var md5 = require('md5')
var headers = {
  pp: md5('monitor_docker')
}

// 获取App列表
export const getAppList = () => {
  return axios.request({
    url: '/api/v1/app/detail/',
    method: 'get',
    headers: headers
  })
}

// 获取
export const getDockerAppGraph = (counter, ep, hours) => {
  return axios.request({
    url: `/api/v1/monitor/docker/graph/?counter=${counter}&hostname=${ep}&hours=${hours}`,
    method: 'get',
    headers: headers
  })
}
