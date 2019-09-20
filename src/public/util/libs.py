"""
各种小工具类
"""
import os
import sys
import logging
import jinja2
import datetime
import time
import random
from django.conf import settings
from subprocess import PIPE, Popen

# local mysql conf
local_mysql_conf = {
    'username': settings.DEPLOY_CONF.get('mysql', 'username'),
    'password': settings.DEPLOY_CONF.get('mysql', 'password'),
    'host': settings.DEPLOY_CONF.get('mysql', 'host'),
    'port': settings.DEPLOY_CONF.get('mysql', 'port'),
    'schema': settings.DEPLOY_CONF.get('mysql', 'schema')
}


def get_logger(name: str = None):
    """
    获取logger
    :param name: 能准确描述该方法作用，命名方式：a_b_c
    :return:
    """
    return logging.getLogger('ops.{}'.format(name))


def template_render2data(context, src_file):
    """
    模版渲染 返回data
    :param context: 传入渲染的context
    :param src_file: 源模版
    :return:
    """
    try:
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(src_file)))
        template = env.get_template(os.path.basename(src_file))
        data = template.render(context)
        return data
    except Exception as e:
        raise e


def template_render2file(context, src_file, det_file):
    """
    模版渲染成输出文件
    :param context: 内容
    :param src_file: 源文件
    :param det_file: 目标文件
    :return:
    """

    try:
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(src_file)))
        template = env.get_template(os.path.basename(src_file))
        data = template.render(context)
        with open(det_file, 'w') as f:
            f.write(data)
    except Exception as e:
        raise e


# 获取工单号
def get_work_order(work_type='message'):
    work_order_type = {
        'message': '100',
        'ngx_access': '200',
        'third_party': '300'
    }
    rand_number = random.randrange(1000, 9999)
    return f'''{work_order_type[work_type]}{str(datetime.datetime.now().strftime('%Y%m%d%H%M%S%f'))}{rand_number}'''


class ExecuteCmd:
    logger = get_logger('ExecuteCmd')

    # The command be executed, but no wait to response
    @classmethod
    def run(cls, cmd=None, exception=False):
        cls.logger.info(f'[执行shell命令]: {cmd}')
        p_obj = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        return cls.__handle_p_obj(p_obj, exception)

    # The command be executed and wait to response
    @classmethod
    def run_wait(cls, cmd=None, exception=False):
        cls.logger.info(f'[执行shell命令]: {cmd}')
        p_obj = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        p_obj.wait()
        return cls.__handle_p_obj(p_obj, exception)

    # The command be executed and rolling output to device
    # :timeout: param prevent function exit. The "sys.stdout" need some time to output info.
    @classmethod
    def run_rolling(cls, cmd=None, exception=False):
        cls.logger.info(f'[执行shell命令]: {cmd}')
        p_obj = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        for line in iter(p_obj.stdout.readline, ''):
            sys.stdout.write(line.decode())
            if line == b'' and p_obj.poll() == 0:
                break

        return cls.__handle_p_obj(p_obj, exception)

    @classmethod
    def __handle_p_obj(cls, p_obj, exception=False):
        out, err = p_obj.communicate()
        code = p_obj.returncode
        result = {
            'stdout': out.decode(encoding='utf-8'),
            'stderr': err.decode(encoding='utf-8'),
            'code': code
        }
        if exception:
            if int(result.get('code', 2)) != 0:
                raise Exception(f"[Shell 执行命令出错，错误内容]: {result.get('stderr')}")
        return result


# utc 与 local 时间转换
UTC_FORMAT_FULL = "%Y-%m-%dT%H:%M:%SZ"
UTC_FORMAT_NO_SEC = "%Y-%m-%dT%H:%MZ"
LOCAL_FORMAT = "%Y-%m-%d %H:%M:%S"
E_CHARTS_FORMAT = "%y/%m/%d %H:%M"


def utc2local(utc_obj):
    """UTC时间转本地时间(+8:00)"""
    try:
        now_stamp = time.time()
        local_time = datetime.datetime.fromtimestamp(now_stamp)
        utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
        offset = local_time - utc_time
        local_st = utc_obj + offset
        return local_st
    except Exception as e:
        raise e


def local2utc(local_obj):
    """本地时间转UTC时间（-8:00)"""
    try:
        time_struct = time.mktime(local_obj.timetuple())
        utc_st = datetime.datetime.utcfromtimestamp(time_struct)
        return utc_st
    except Exception as e:
        raise e


# timestamp -> 指定格式的string
def timestamp2format_time(timestamp: int, fmt: str) -> object:
    try:
        date_obj = datetime.datetime.fromtimestamp(timestamp)
        return date_obj.strftime(fmt)
    except Exception as e:
        raise e


# datetime -> timestamp
def datetime2timestamp(now=None):
    if now == None:
        now = datetime.datetime.now()
    return int(time.mktime(now.timetuple()))
