#!/usr/bin/env bash


#action [deploy|rollback|deploy-sync]
#app_name [deposit|…]
#env [test92|…]
#publish_ip 0.0.0.0
#server_mode [docker|tomcat|jar|tc2docker]
#branch
#version
#task_id
#flag


source ./ops_control.sh


ACTION=${1}
# TIER
APP_NAME=${2}
ENV=${3}
PUBLISH_IP=${4}
SERVER_MODE=${5}
BRANCH=${6}
VERSION=${7}
TASK_ID=${8}c


# 配置初始化
function InitConfig() {
    :
}



function DockerModule () {
    local app_name=${APP_NAME}
    local env=${ENV}
    local version=${VERSION}
    echo "docker module"
}


function TomcatModule () {
    local app_name=${APP_NAME}
    local env=${ENV}
    local version=${VERSION}
    echo "tomcat module"
}


function JarModule () {
    local app_name=${APP_NAME}
    local env=${ENV}
    local version=${VERSION}
    echo "jar module"

}


function Tc2dockerModule() {
    local app_name=${APP_NAME}
    local env=${ENV}
    local version=${VERSION}
    echo "tc2docker module"
}


function GitClone() {
    :
}

function UtilMaven() {
    :
}

function UtilGradle() {
    :
}

function UtilDockerBuild() {
    :
}

function UtilDockerPush() {
    :
}

function UtilUploadPkg() {
    # DownFormRepo
    # tar zcvf  ${version}.tar.gz
    :
}

UtilUploadPkg src target &
pid=$!


function UtilDownloadPkg() {
    # tar zxvf /*  ${version}.tar.gz
    # UploadToRepo
    :
}

function UtilPushTargetServer() {
    :
}

# 路由分发
function MainRouter () {
    local app_name=${APP_NAME}
    local env=${ENV}
    local server_mode=${SERVER_MODE}
    # if
    # case
}


# Action 分发
function ActionRouter () {
    local action=${ACTION}
    case ${action} in
    'deploy')
        GitClone
        echo 'Do action'
        ;;
    'rollback')
        UtilDownloadPkg
        echo 'Do action'
        ;;
    'deploy-sync')
        UtilDownloadPkg
        echo 'Do action'
        ;;
    *)
        echo 'No action to do.'
        exit 1
    esac
}


# Server Mode 分发
function ServerModeRouter () {
    local server_mode=${SERVER_MODE}
    case ${server_mode} in
    'docker')
        DockerModule
        ;;
    'tomcat')
        TomcatModule
        ;;
    'deploy-sync')
        JarModule
        ;;
    'tc2docker')
        Tc2dockerModule
        ;;
    *)
        echo 'No action to do.'
        exit 1
    esac
}



function Main() {
    InitConfig
    MainRouter
    ActionRouter
    ServerModeRouter
}

Main
wait $pid


ops -> jenkins -> script
script <- ops