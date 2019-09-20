"""
用于调度 Jenkins Api
"""
import time
import json
import jenkins


server = jenkins.Jenkins('http://jenkins.aiyuangong.com', username="shadow.liang", password="htL*SXJ8")
print(server.server)
print(server.jobs_count())
print(server.get_jobs(view_name='Ops'))
print(server.job_exists('ops-deposit'))
print(json.dumps(server.get_job_info('ops', depth=0)))
next_bn = server.get_job_info('ops')['nextBuildNumber']
print(next_bn)
print(server.get_running_builds())
# print(server.get_build_console_output('ops', 10))

# # print(json.dumps(server.get_node_info(name='docker-test')))
params = {}
# server.build_job('ops', parameters=params)
# time.sleep(3)
# print(json.dumps(server.get_queue_info()))
print(server.get_running_builds())
print(json.dumps(server.get_build_info('pipeline_test', 10)))
# ABORTED
# FAILURE
