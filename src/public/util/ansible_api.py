# coding: utf-8
"""
ansible Api
"""
import os
import tempfile
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase


class AnsibleHost:
    """
    ansible host 生成主机
    """
    def __init__(self, host, port=None, connection=None, ssh_user=None, ssh_pass=None):
        self.host = host
        self.port = port
        self.ansible_connection = connection
        self.ansible_ssh_user = ssh_user
        self.ansible_ssh_pass = ssh_pass

    def __str__(self):
        result = 'ansible_ssh_host=' + str(self.host)
        if self.port:
            result += ' ansible_ssh_port=' + str(self.port)
        if self.ansible_connection:
            result += ' ansible_connection=' + str(self.ansible_connection)
        if self.ansible_ssh_user:
            result += ' ansible_ssh_user=' + str(self.ansible_ssh_user)
        if self.ansible_ssh_pass:
            result += ' ansible_ssh_pass=' + str(self.ansible_ssh_pass)
        return result


class AnsibleTaskResultCallback(CallbackBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result


class AnsibleTask:
    def __init__(self, hosts=None, extra_vars=None):
        self.hosts = hosts
        self.__validate()
        self.hosts_file = None
        self.__generate_hosts_file()
        Options = namedtuple('Options', [
            'connection', 'module_path',
            'forks', 'become',
            'become_method', 'become_user',
            'check', 'diff',
            'host_key_checking', 'listhosts',
            'listtasks', 'listtags', 'syntax'
        ])
        self.options = Options(
            connection='ssh',
            module_path=None,
            forks=10,
            become=None,
            become_method=None,
            become_user=None,
            check=False,
            diff=False,
            host_key_checking=False,
            listhosts=None,
            listtasks=None,
            listtags=None,
            syntax=None
        )
        self.loader = DataLoader()
        self.passwords = dict(vault_pass='secret')
        self.inventory = InventoryManager(loader=self.loader, sources=[self.hosts_file])
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.results_callback = AnsibleTaskResultCallback()
        # 结果对象
        self.results_raw = {'success': {}, 'failed': {}, 'unreachable': {}}

        if extra_vars:
            self.variable_manager.extra_vars = extra_vars

    # 用于读取host 文件的，一般用不到
    def __generate_hosts_file(self):
        self.hosts_file = tempfile.mktemp()
        with open(self.hosts_file, 'w+', encoding='utf-8') as file:
            hosts = []
            for host in self.hosts:
                hosts.append(f'{host.host} {str(host)}')
            file.write('\n'.join(hosts))

    def __validate(self):
        assert self.hosts, 'hosts不能为空'
        assert isinstance(self.hosts, list), 'hosts 应为 list'
        for host in self.hosts:
            assert isinstance(host, AnsibleHost), 'host 类型必须为 AnsibleHost'

    def exec_run(self, module_name, module_args=None):
        play_source = dict(
            name="Ops Ansible Play",
            hosts='all',
            gather_facts='no',
            tasks=[dict(action=dict(module=module_name, args=module_args))] if module_args
            else [dict(action=dict(module=module_name))]
        )

        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        self.results_callback = AnsibleTaskResultCallback()
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
                stdout_callback=self.results_callback
            )
            tqm.run(play)
        except Exception as e:
            raise e
        finally:
            tqm.cleanup()
            self.loader.cleanup_all_tmp_files()

    def exec_playbook(self, playbooks):

        playbook = PlaybookExecutor(
            playbooks=playbooks,
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            options=self.options,
            passwords=self.passwords
        )
        setattr(getattr(playbook, '_tqm'), '_stdout_callback', self.results_callback)
        playbook.run()
        playbook._tqm.cleanup()

    @property
    def get_result(self):
        for host, result in self.results_callback.host_ok.items():
            self.results_raw['success'][host] = (
                result._result,
                {'code': 0}
            )

        for host, result in self.results_callback.host_failed.items():
            self.results_raw['failed'][host] = (
                result._result,
                {'code': 1}
            )

        for host, result in self.results_callback.host_unreachable.items():
            self.results_raw['unreachable'][host] = (
                result._result,
                {'code': 1}
            )

        return self.results_raw

    # __del__ 被称为析构方法，在程序执行完后，python垃圾回收器，会自动执行
    def __del__(self):
        if self.hosts_file:
            os.remove(self.hosts_file)


if __name__ == "__main__":
    import json
    import sys
    if len(sys.argv) != 4:
        print(len(sys.argv))
        print(f'''Usage: ./ansible_api.py setup '' '[["ip", port, "user"]]' ''')
        sys.exit(1)

    hosts_list = json.loads(sys.argv[3])
    task_list = [
        AnsibleHost(hosts[0], hosts[1], 'ssh', hosts[2], )
        for hosts in hosts_list
    ]
    task = AnsibleTask(task_list)
    task.exec_run(sys.argv[1], sys.argv[2])
    print(json.dumps(task.get_result))
