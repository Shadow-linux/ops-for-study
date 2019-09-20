import axios from '@/libs/api.request'
var md5 = require('md5')
var headers = {
  pp: md5('code_publish_issue')
}

// 获取 task 列表
export const getTasksList = () => {
  return axios.request({
    url: `/api/v1/code-publish/web/control/main/`,
    method: 'get',
    headers: headers
  })
}

// 获取 env 列表
export const getEnvs = () => {
  return axios.request({
    url: `/api/v1/code-publish/web/env/`,
    method: 'get',
    headers: headers
  })
}

// get app detail
export const getAppDetail = (appName, env) => {
  return axios.request({
    url: `/api/v1/code-publish/web/control/main-conf/?app_name=${appName}&env=${env}`,
    method: 'get',
    headers: headers
  })
}

// get has been published list
export const getHasBeenPublished = (appName, env, action) => {
  return axios.request({
    url: `/api/v1/code-publish/web/has-been-published/?app_name=${appName}&env=${env}&action=${action}`,
    method: 'get',
    headers: headers
  })
}

// get branch
export const getAppNameBranch = (appName, env) => {
  return axios.request({
    url: `/api/v1/code-publish/web/get-branch/?app_name=${appName}&env=${env}`,
    method: 'get',
    headers: headers
  })
}

// create publish task
export const createPublishTask = (data) => {
  return axios.request({
    url: `/api/v1/code-publish/web/control/main/`,
    method: 'post',
    headers: headers,
    data: data
  })
}

// 删除 publish task
export const destroyPublishTask = (id) => {
  return axios.request({
    url: `/api/v1/code-publish/web/control/main/${id}/`,
    method: 'delete',
    headers: headers
  })
}

// update publish task status
export const updateTaskStatus = () => {
  return axios.request({
    url: `/api/v1/code-publish/web/control/task-status/`,
    method: 'get',
    headers: headers
  })
}

// 实时更新发布步骤
export const getRealTimeSteps = (id) => {
  return axios.request({
    url: `/api/v1/code-publish/web/real-time/steps/${id}/`,
    method: 'get',
    headers: headers
  })
}

// stop jenkins build
export const stopJenkinsBuild = (id) => {
  return axios.request({
    url: `/api/v1/code-publish/web/stop-building/${id}/`,
    method: 'delete',
    headers: headers
  })
}

// real time task status
export const getRealTimeTaskStatus = () => {
  return axios.request({
    url: `/api/v1/code-publish/web/real-time/task-status/`,
    method: 'get',
    headers: headers
  })
}

// get has already been publish version
export const getAlreadyPublishVer = (appName, env) => {
  return axios.request({
    url: `/api/v1/code-publish/web/already-version/?app_name=${appName}&env=${env}`,
    method: 'get',
    headers: headers
  })
}

export const getAppNameEndpoint = (endpoint, env) => {
  return axios.request({
    url: `/api/v1/code-publish/web/app-name/endpoint/?web_tag=${endpoint}&env=${env}`,
    method: 'get',
    headers: headers
  })
}

export const unlockPublishIp = (data) => {
  return axios.request({
    url: `/api/v1/code-publish/web/unlock/publish-ip/`,
    method: 'post',
    headers: headers,
    data: data
  })
}

export const envLockList = () => {
  return axios.request({
    url: `/api/v1/code-publish/web/lock-env/`,
    method: 'get',
    headers: headers
  })
}

export const getUsersList = () => {
  return axios.request({
    url: `/api/v1/users/open/`,
    method: 'get',
    headers: headers
  })
}

export const getLockEnvAppList = (env) => {
  return axios.request({
    url: `/api/v1/code-publish/web/lock-env-app/?env=${env}`,
    method: 'get',
    headers: headers
  })
}

export const getBindLockEnvAppList = (id) => {
  return axios.request({
    url: `/api/v1/code-publish/web/lock-env-app/${id}/`,
    method: 'get',
    headers: headers
  })
}

export const createEnvLock = (data) => {
  return axios.request({
    url: `/api/v1/code-publish/web/lock-env/`,
    method: 'post',
    headers: headers,
    data: data
  })
}

export const updateEnvLock = (id, data) => {
  return axios.request({
    url: `/api/v1/code-publish/web/lock-env/${id}/`,
    method: 'put',
    headers: headers,
    data: data
  })
}

export const unlockEnv = (id) => {
  return axios.request({
    url: `/api/v1/code-publish/web/unlock-env/${id}/`,
    method: 'delete',
    headers: headers
  })
}
