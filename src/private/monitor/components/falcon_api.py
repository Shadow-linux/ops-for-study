"""
falcon 的相关方法
api参考地址: http://api.open-falcon.com
"""
import datetime
import json
import requests
from django.conf import settings
from public.util.libs import get_logger

logger = get_logger('monitor.components.third_party.falcon_api')

HEADER = {
    "token": "default-token-used-in-server-side",
    "content-Type": "application/json"
}


# 获取open-falcon 登录信息
def get_open_falcon_login_token():
    data = {
        "name": settings.DEPLOY_CONF.get('falcon', 'name'),
        "password": settings.DEPLOY_CONF.get('falcon', 'password')
    }
    req_url = f"{settings.DEPLOY_CONF.get('falcon', 'api_address')}/user/login"
    r_data = requests.post(req_url, data=json.dumps(data), headers=HEADER, verify=False)
    logger.debug(f"`get_open_falcon_login_token()` res: {r_data}")
    r_data_dict = r_data.json()
    if r_data_dict.get("error"):
        raise Exception(r_data_dict)
    r_data_dict.pop("admin")
    return json.dumps(r_data_dict)


# 临时解决办法
def API_HEADER():
    try:
        api_header = {
            "Apitoken": get_open_falcon_login_token(),
            # "Apitoken": "",
            "content-Type": "application/json",
        }
    except Exception as e:
        api_header = {
            "Apitoken": '',
            # "Apitoken": "",
            "content-Type": "application/json",
        }
        logger.warning('登陆open-falcon失败，获取 open-falcon api_header失败')
        logger.exception(e)
    return api_header


# get graph data
def get_graph_data(start_time: datetime, end_time: datetime, ep: list, counters: list, step: int):
    post_data = {
        "step": step,
        "start_time": int(start_time.timestamp()),
        "hostnames": ep,
        "end_time": int(end_time.timestamp()),
        "counters": counters,
        # 没写错 consol falcon 是这样写的
        "consol_fun": "AVERAGE"
    }
    post_url = f'''{settings.DEPLOY_CONF.get('falcon', 'api_address')}/graph/history'''
    res_data = requests.post(post_url, data=json.dumps(post_data), headers=API_HEADER())
    logger.debug(f"`get_graph_data()` res: {res_data}")
    res_data_list = res_data.json()
    return res_data_list


# push monitor info to open-falcon
def push_data_to_open_falcon(endpoint=None, metric=None,
                             timestamp=None, step=60,
                             value=None, counter_type='GAUGE', tags=""):
    """
    curl -X POST -d
    '[{"metric": "qps",
     "endpoint": "open-falcon-graph01.bj",
      "timestamp": 1431347802,
       "step": 60,
       "value": 9,
       "counterType": "GAUGE",
       "tags": "project=falcon,module=graph"}]' http://127.0.0.1:1988/v1/push
    """
    data = [{
        'metric': metric,
        'endpoint': endpoint,
        'timestamp': timestamp,
        'step': step,
        'value': value,
        'counterType': counter_type,
        'tags': tags
    }]
    push_url = settings.DEPLOY_CONF.get('falcon', 'agent')
    res = requests.post(push_url, data=json.dumps(data), headers=HEADER, verify=False)
    logger.debug(f"`push_data_to_open_falcon()` res: {res}")
    assert res.content.decode() == 'success', f'''`push_data_to_open_falcon() response {res.content.decode()}`'''


def get_falcon_hg():
    req_url = f"{settings.DEPLOY_CONF.get('falcon', 'api_address')}/hostgroup"
    grp_data = requests.get(req_url, headers=API_HEADER(), verify=False)
    logger.debug(f"`get_falcon_hg()` res: {grp_data}")
    """grp_data_list 数据格式
    [
      {
        "id": 3,
        "grp_name": "docker-A",
        "create_user": "user-A"
      },
      ...
    ]
    """
    grp_data_list = grp_data.json()
    return grp_data_list


# 获取host 的id
def get_host_id(hg_id, endpoint):
    req_url = f"{settings.DEPLOY_CONF.get('falcon', 'api_address')}/hostgroup/{hg_id}"
    grp_data = requests.get(req_url, headers=API_HEADER(), verify=False)
    logger.debug(f"`get_host_id()` res: {grp_data}")
    grp_data_list = grp_data.json()
    hosts_data_list = grp_data_list['hosts']
    for host_data in hosts_data_list:
        if host_data['hostname'] == endpoint:
            return host_data['id']


# 获取falcon groups 对应的hosts
def get_grp_hosts(hg: str) -> list:
    grp_data_list = get_falcon_hg()
    hg_id = None
    for grp in grp_data_list:
        if grp['grp_name'] == hg.strip():
            hg_id = grp['id']
            break
    # 如果是空的则直接返回
    if not hg_id:
        return []
    url = f"{settings.DEPLOY_CONF.get('falcon', 'api_address')}/hostgroup/{hg_id}"
    res = requests.get(url, headers=API_HEADER(), verify=False)
    logger.debug(f"`get_grp_hosts()` res: {res}")
    assert res.status_code == 200, f'''`get_grp_hosts() status code {res.status_code}`'''
    data = res.json()
    return [hh['hostname'] for hh in data['hosts']]


# 添加endpoint 到 falcon host_group
def add_endpoint_to_falcon_grp(endpoint: list, hg):
    grp_data_list = get_falcon_hg()
    # grp_id 可以为0 ，但不能为none
    grp_id = None
    for grp in grp_data_list:
        if grp['grp_name'] == hg:
            grp_id = grp['id']
            break
    if grp_id is not None:
        add_host_url = f"{settings.DEPLOY_CONF.get('falcon', 'api_address')}/hostgroup/host"
        post_data = {
            'hosts': endpoint,
            'hostgroup_id': grp_id
        }
        res = requests.post(add_host_url, data=json.dumps(post_data), headers=API_HEADER(), verify=False)
        logger.debug(f"`add_endpoint_to_falcon_grp()` res: {res}")
        assert res.status_code == 200, f'''`add_endpoint_to_falcon_grp() status code {res.status_code}`'''


# 删除graph 即首页的数据
def del_endpoint_to_graph(endpoint):
    if isinstance(endpoint, list):
        data = endpoint
    else:
        data = [endpoint]
    del_url = f"{settings.DEPLOY_CONF.get('falcon', 'api_address')}/graph/endpoint"
    res = requests.delete(del_url, data=json.dumps(data), headers=API_HEADER(), verify=False)
    logger.debug(f"`del_endpoint_to_graph()` res: {res}")
    assert res.status_code == 200, f'''`del_endpoint_to_graph() status code {res.status_code}`'''


# 删除 unbind a host on hostgroup
def del_endpoint_to_falcon_grp(endpoint, hg):
    grp_data_list = get_falcon_hg()
    # grp_id 可以为0 ，但不能为none
    grp_id = None
    for grp in grp_data_list:
        if grp['grp_name'] == hg:
            grp_id = grp['id']
            break
    if grp_id is not None:
        add_host_url = f"{settings.DEPLOY_CONF.get('falcon', 'api_address')}/hostgroup/host"
        host_id = get_host_id(grp_id, endpoint)
        if not host_id:
            return
        data = {
            'hostgroup_id': grp_id,
            'host_id': host_id
        }
        res = requests.put(add_host_url, data=json.dumps(data), headers=API_HEADER(), verify=False)
        logger.debug(f"`del_endpoint_to_falcon_grp()` res: {res}")


# 删除 falcon endpoint counter
def del_endpoint_counter(endpoints: list, counters: list):
    data = {
        "endpoints": endpoints,
        "counters": counters,
    }
    url = f"{settings.DEPLOY_CONF.get('falcon', 'api_address')}/graph/counter"
    res = requests.delete(url=url, data=json.dumps(data), headers=API_HEADER(), verify=False)
    logger.debug(f"`del_endpoint_counter()` res: {res}")
    assert res.status_code == 200, f'''`del_endpoint_counter() status code {res.status_code}`'''


# 获取 endpoint id
def get_endpoint_id(ep):
    url = f"{settings.DEPLOY_CONF.get('falcon', 'api_address')}/graph/endpoint/?q={ep}"
    logger.debug(url)
    res = requests.get(url=url, headers=API_HEADER(), verify=False)
    logger.debug(f"`get_endpoint_id()` res: {res.text}")
    assert res.status_code == 200, f'''`get_endpoint_id() status code {res.status_code}`'''
    return res.json()


# 查询 endpoint 中有哪些 counter
def get_endpoint_counter(endpoint, counter):
    """
    :param endpoint:  string
    :param counter:  使用 regex 查询字符option 参数 , 如 ^net.if.out.bytes
    :return: []
    """
    ep_id = 0
    endpoint_id_list = get_endpoint_id(endpoint)
    for endpoint_id in endpoint_id_list:
        if endpoint == endpoint_id['endpoint']:
            ep_id = endpoint_id['id']
            break
    if ep_id:
        url = f'''{settings.DEPLOY_CONF.get('falcon', 'api_address')}/graph/endpoint_counter'''
        logger.debug(url)
        res = requests.get(url=url, headers=API_HEADER(), verify=False, params={
            'eid': ep_id,
            'metricQuery': f'^{counter}'
        })
        logger.debug(f"`get_endpoint_counter()` res: {res.text}")
        assert res.status_code == 200, f'''`get_endpoint_counter() status code {res.status_code}`'''
        return res.json()
    return []
