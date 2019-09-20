import axios from '@/libs/api.request'
var md5 = require('md5')
var headers = {
  pp: md5('code_publish_config')
}

// 获取 env 列表
export const getEnvs = () => {
  return axios.request({
    url: `/api/v1/code-publish/web/env/`,
    method: 'get',
    headers: headers
  })
}

export const createEnv = (data) => {
  return axios.request({
    url: `/api/v1/code-publish/web/env/`,
    method: 'post',
    data: data,
    headers: headers
  })
}

export const updateEnv = (id, data) => {
  return axios.request({
    url: `/api/v1/code-publish/web/env/${id}/`,
    method: 'put',
    data: data,
    headers: headers
  })
}

export const deleteEnv = (id) => {
  return axios.request({
    url: `/api/v1/code-publish/web/env/${id}/`,
    method: 'delete',
    headers: headers
  })
}

export const getMainConfs = () => {
  return axios.request({
    url: `/api/v1/code-publish/get/main-conf/`,
    method: 'get',
    headers: headers
  })
}

export const deleteMainConf = (id) => {
  return axios.request({
    url: `/api/v1/code-publish/web/main-conf/${id}/`,
    method: 'delete',
    headers: headers
  })
}

export const createWebMainConf = (data) => {
  return axios.request({
    url: `/api/v1/code-publish/web/main-conf/`,
    method: 'post',
    headers: headers,
    data: data
  })
}

export const updateWebMainConf = (id, data) => {
  return axios.request({
    url: `/api/v1/code-publish/web/main-conf/${id}/`,
    method: 'put',
    headers: headers,
    data: data
  })
}

export const getSingleMainConf = (appName, env) => {
  return axios.request({
    url: `/api/v1/code-publish/get/main-conf/?app_name=${appName}&env=${env}`,
    method: 'get',
    headers: headers
  })
}

export const replaceIp = (data) => {
  return axios.request({
    url: `/api/v1/code-publish/web/replace-ip/`,
    method: 'post',
    data: data,
    headers: headers
  })
}

export const copyConfig = (id, data) => {
  return axios.request({
    url: `/api/v1/code-publish/web/copy-conf/${id}/`,
    method: 'put',
    data: data,
    headers: headers
  })
}

export const batchCopyConfig = (data) => {
  return axios.request({
    url: `/api/v1/code-publish/web/batch/copy-config/`,
    method: 'post',
    data: data,
    headers: headers
  })
}

// get steps
export const getSteps = () => {
  return axios.request({
    url: `/api/v1/code-publish/web/steps/`,
    method: 'get',
    headers: headers
  })
}

// get mvn opts
export const getMvnOpts = () => {
  return axios.request({
    url: `/api/v1/code-publish/web/mvn-opts/`,
    method: 'get',
    headers: headers
  })
}

// get mvn opts
export const getGradleOpts = () => {
  return axios.request({
    url: `/api/v1/code-publish/web/gradle-opts/`,
    method: 'get',
    headers: headers
  })
}

// get java opts
export const getJavaOpts = () => {
  return axios.request({
    url: `/api/v1/code-publish/web/java-opts/`,
    method: 'get',
    headers: headers
  })
}

// get jar opts
export const getJarOpts = () => {
  return axios.request({
    url: `/api/v1/code-publish/web/jar-opts/`,
    method: 'get',
    headers: headers
  })
}

// get docker opts
export const getDockerOpts = () => {
  return axios.request({
    url: `/api/v1/code-publish/web/docker-opts/`,
    method: 'get',
    headers: headers
  })
}

// get dockerfile
export const getDockefile = () => {
  return axios.request({
    url: `/api/v1/code-publish/web/dockerfile/`,
    method: 'get',
    headers: headers
  })
}

// get app detail
export const getAppDetail = () => {
  return axios.request({
    url: `/api/v1/code-publish/web/control/app-detail/`,
    method: 'get',
    headers: headers
  })
}

// get code publish setting
export const getCodePublish = () => {
  return axios.request({
    url: `/api/v1/common/setting/code-publish/`,
    method: 'get',
    headers: headers
  })
}
