"""
用于调度 Jenkins Api
"""
import jenkins
from urllib.parse import urljoin
from django.conf import settings

USERNAME = settings.DEPLOY_CONF.get('jenkins', 'username')
PASSWORD = settings.DEPLOY_CONF.get('jenkins', 'password')
HOST = settings.DEPLOY_CONF.get('jenkins', 'host')


class OpsJenkinsController:

    def __init__(self):
        self.server = jenkins.Jenkins(HOST, username=USERNAME, password=PASSWORD)

    # 构建Job
    def build_job(self, job, params):
        """
        :param job:
        :param params: 构建参数
        :return: console url
        """
        job_info = self.get_job_info(job)
        next_bn = job_info['nextBuildNumber']
        job_url = job_info['url']

        if job_info.get('activeConfigurations'):
            label = job_info.get('activeConfigurations')[0]['name']
            url = urljoin(job_url, f'{label}/{next_bn}/console')
        else:
            url = urljoin(job_url, f'{next_bn}/console')
        self.server.build_job(job, params)
        return url, next_bn

    # Check Job Exists
    def is_job_exists(self, job):
        return self.server.job_exists(job)

    def get_build_info(self, job, number):
        return self.server.get_build_info(job, number)

    def get_job_info(self, job, depth=0):
        return self.server.get_job_info(job, depth=0)

    # 获取正在执行的队列
    def get_running_builds(self):
        return self.server.get_running_builds()

    # 获取准备执行的队列
    def get_queue_info(self):
        return self.server.get_queue_info()

    # 终止正在执行的job
    def stop_build(self, job, number):
        return self.server.stop_build(job, number)

    # 获取某个job 某个id 任务的状态
    def get_job_id_status(self, job, number):
        """
        :param job:
        :param number:
        :return: 0: null， 1: success， 2：failure， 3：building, 4: aborted
        """
        # 先查看build_info
        try:
            # print(job, number)
            build_info = self.get_build_info(job, number)
            # print(build_info)
        except Exception as e:
            return 0
        if build_info['building']:
            return 3

        if not build_info['building']:
            result = build_info['result']
            if result == 'SUCCESS':
                return 1
            if result == 'FAILURE':
                return 2
            if result == 'ABORTED':
                return 4
