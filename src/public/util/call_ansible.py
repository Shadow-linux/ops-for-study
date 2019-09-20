# coding: utf-8
import os
import json
from subprocess import Popen, PIPE
from django.conf import settings
from .libs import get_logger
from .ansible_api import AnsibleHost, AnsibleTask

logger = get_logger('public.util.call_ansible')
PYTHON = settings.DEPLOY_CONF.get('python', 'python')


# (致开发者or维护者) 在终端上通过传值直接调用， 其实api接口已经写好了，正常其实可以在程序中调用的。
# 那为什么没直接调用，却费劲的在终端上调用呢？ 原因是那个运维哥，搞个vpn ，搞了n个月都没动手，机器的出口IP一值在变动。
# 每变动一次IP内部的ansible api 工作就不正常了，守营者真可怕。
# 注：在linux上使用不知道为什么会报错， 报 no attribute 'isatty'
# (问题找到了是因为gunicorn 使用了gevent 异步模式，用回同步应该就解决了)
# 注: 最终并未能通过console调用解决问题，只要是通过ssh_proxy 访问的，当出口IP变化时就变成unreachable, 可能是ops依赖于终端导致的
def call_console_ansible_setup(host_list: list):
    ansible_api_file = os.path.join(settings.BASE_DIR, 'public/util/ansible_api.py')
    console_cmd = f'''{PYTHON} {ansible_api_file} setup '' '{json.dumps(host_list)}' '''
    logger.info(console_cmd)
    # console_cmd = 'ls ./'
    p = Popen(console_cmd, shell=True, stdout=PIPE, stderr=PIPE)
    p.wait()
    out, err = p.communicate()
    logger.debug(out.decode())
    if err:
        raise Exception(err)
    return out.decode()


def call_console_ansible_shell(host_list: list, cmd: str):
    ansible_api_file = os.path.join(settings.BASE_DIR, 'public/util/ansible_api.py')
    console_cmd = f'''{PYTHON} {ansible_api_file} shell '{cmd}' '{json.dumps(host_list)}' '''
    logger.info(console_cmd)
    # console_cmd = 'ls ./'
    p = Popen(console_cmd, shell=True, stdout=PIPE, stderr=PIPE)
    # p.wait()
    out, err = p.communicate()
    if err:
        raise Exception(err)
    return out.decode()


# 直接调用ansible
def call_ansible_setup(hosts_list: list):
    task_list = [
        AnsibleHost(hosts[0], hosts[1], 'ssh', hosts[2])
        for hosts in hosts_list
    ]
    task = AnsibleTask(task_list)
    task.exec_run('setup')
    return json.dumps(task.get_result)
