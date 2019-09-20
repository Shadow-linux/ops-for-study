#!/usr/bin/env bash

_PYTHON='/Users/liangyedong/Desktop/ayg/code_publish/venv/bin/python3.6'
OPS_CONTROL='/Users/liangyedong/Desktop/ayg/code_publish/old_code_publish/ops_contorl/control.py'



# 更新必须参数app配置
function GetAppConfig () {
    local cmd="${_PYTHON} ${OPS_CONTROL} --update-conf"
    echo ${cmd}
    eval ${cmd}
}


# 获取各种配置参数 [mvn_opts|java_opts|jar_opts|docker_opts|pkg_name|docker_file]
function GetDifferentArgs() {
    local app_name=${1}
    local env=${2}
    local opt_type=${3}
    ${_PYTHON} ${OPS_CONTROL} config --app-name ${app_name} --env ${env} --opt-type ${opt_type}
}


# 推送steps code_build
function CommitPublishStatus() {
    local task_id=${1}
    local step=${2}
    ${_PYTHON} ${OPS_CONTROL} status --update --task-id ${task_id} --step ${step}
}


# upload pkg
function UploadToRepo() {
    # remote_file 格式: test92/deposit/deposit_20190101010101_1/deposit.jar
    local remote_file${1}
    local local_file=${2}
    ${_PYTHON} ${OPS_CONTROL} repo --upload --remote-file ${remote_file} --local-file ${local_file}
}


function DownloadFromRepo() {
    local remote_file=${1}
    local local_file=${2}
    ${_PYTHON} ${OPS_CONTROL} repo --download --remote-file ${remote_file} --local-file ${local_file}
}

