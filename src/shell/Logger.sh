#!/usr/bin/env bash

# 工具方法, 日志工具
# author : YD
# created: 2018-08-14

# Usage:
#   source ./lib/logger.sh
#   loggerSetPath './test.log';        // 设置日志文件路径，如果不设置日志路径，仅打印在终端
#   logger 'info' 'test hello world';  // 只是打印日志并记录文件
#   loggerRc $? "成功显示 /root"        // 如返回码为0 打印info日志 ，如果不为0 打印error日志并且退出程序

CURRENT_TIME=$(date +"%F %T");

# 配置日志
function loggerSetPath(){
    local set_path="${1}";
    if [ ${#set_path} -ne 0 ];then
        export log_path="${set_path}";
        touch -f .aaaa/test.log > /dev/null 2>&1
        test -f ${log_path}
        if [[  $? -ne 0 ]];then
            echo "[ ${CURRENT_TIME} ${0}:${LINENO} ERROR ]: 日志路径不存在或不是文件 ${log_path} "
            exit 1
        fi

    fi
}

# 记录日志
function _recordLog(){
    local format_message=${1};
    if [[ ! -z ${log_path} ]];then
        echo -e "${format_message}" |tee -a ${log_path};
        return
    fi
    echo  -e "${format_message}"
}

# 纯日志函数
function logger(){

    local level="${1:-WARNING}";
    local content="${2:-None}";

    case ${level} in
    'info'|'INFO')
        _recordLog  "[ ${CURRENT_TIME} ${0}:${LINENO}  INFO ]: ${content}";
        ;;
    'warning'|'warn'|'WARN'|'WARNING')
        _recordLog  "[ ${CURRENT_TIME} ${0}:${LINENO}  WARNING ]: ${content}";
        ;;
    'error'|'ERROR')
        _recordLog "[ ${CURRENT_TIME} ${0}:${LINENO}  ERROR ]: ${content}";
        ;;
    esac
}

# 判断返回值的日志函数,返回值不为0时程序结束
function loggerRc(){
    local ret_code="${1}";
    local content="${2:-OccurError}";
    local info_message="[ ${CURRENT_TIME} ${0}:${LINENO}  INFO ]: ${content}";
    local error_message="[ ${CURRENT_TIME} ${0}:${LINENO}  ERROR ]: ${content} 错误 \n 程序退出";

    case ${ret_code} in
    0|'0')
        _recordLog  "${info_message}";
        ;;
    *)
        _recordLog  "${error_message}";
        exit 1
        ;;
    esac
}


