#!/usr/bin/env bash

source ./shell/Logger.sh

GUNICORN='/opt/ops_py36/bin/gunicorn'
WORK_DIR='/home/app/ops'
PROJECT='ops'

function start() {
    cd ${WORK_DIR}/${PROJECT}/src
    nohup ${GUNICORN} --bind=0.0.0.0:8001 \
    --pid ./${PROJECT}.pid \
    --workers=15 ops.wsgi:application  \
    --threads 2 \
    --backlog 1024 \
    --timeout 300 \
    --access-logfile ./log/access.log \
    --error-logfile ./log/error.log &
    loggerRc $? "启动 ${PROJECT}"
}

function stop() {
    cd ${WORK_DIR}/${PROJECT}/src
    local process_id=$(ps aux|grep '/opt/ops_py36/bin/gunicorn' |grep -v grep|awk '{print $2}')
    kill -9 ${process_id}
    logger 'info' "关闭 ${PROJECT}"
}

function restart() {
    stop
    start
}

function status() {
    cd ${WORK_DIR}/${PROJECT}/src
    local process_id=$(cat ${PROJECT}.pid)
    local exists=$(ps aux|grep ${process_id} |grep -v grep |grep ops |wc -l)
    if [[ ${exists} != 0 ]]; then
        logger 'info' "Ops is up."; exit 0
    fi
    logger 'info' "Ops is down."; exit 0
}

function main() {
    local action=${1}
    case ${action} in
        'start')
        start ;;
        'stop')
        stop ;;
        'restart')
        restart ;;
        'status')
        status ;;
    esac
}

ACTION=${1}
ACTION_ARRAY=('start' 'stop' 'restart' 'status')
for item in ${ACTION_ARRAY[@]}; do
    if [[ ${item} == ${ACTION} ]]; then
        main ${ACTION}
        break
    fi
done
