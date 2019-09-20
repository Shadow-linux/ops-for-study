"""
app alive 信息
"""
import datetime
import requests
import json
from urllib.parse import urlparse
from django.conf import settings
from monitor.components.falcon_api import get_open_falcon_login_token
from public.util import call_mysql
from public.util.libs import local_mysql_conf, get_logger

logger = get_logger('monitor.components.app_alive')


class AppAliveGraph:
    """
    获取 app alive 监控信息流程:
        env -> urlooker(获取strategy id) --> open-falcon(urlooker_id)
    """
    def __init__(self, environment=None, app_id=None, check_api=None, hours=12):
        self.env = environment
        self.app_id = app_id
        self.check_api = check_api
        self.hours = hours
        # 这里只能从配置文件获取，无法从urlooker 直接获取
        self.__parse_agent = {
            'default': settings.DEPLOY_CONF.get('urlooker_agent', 'default'),
            'internal.ayg.gz': settings.DEPLOY_CONF.get('urlooker_agent', 'internal_ayg_gz')
        }

    def __get_urlooker_id(self):
        result = []
        sql = f'''select id, ip, idc, url from strategy
where environment = '{self.env}' and ops_cp_app_id = {self.app_id} and url = '{self.check_api}';'''
        with call_mysql.OpsMysqlClient(username=local_mysql_conf['username'],
                                       password=local_mysql_conf['password'],
                                       host=local_mysql_conf['host'],
                                       port=local_mysql_conf['port'],
                                       schema='urlooker') as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
        ret_result = {}
        for strategy_obj in result:
            ret_result[strategy_obj['id']] = {
                'ip': strategy_obj['ip'],
                'idc': strategy_obj['idc'],
                'url': strategy_obj['url']
            }

        return ret_result

    def __get_falcon_monitor(self, urlooker_id=None, ip=None, src=None, domain=None):
        try:
            headers = {
                "Apitoken": get_open_falcon_login_token(),
                "content-Type": "application/json",
            }
        except Exception as e:
            logger.exception(e)
            raise e
        now_time = datetime.datetime.now()
        start_time = now_time - datetime.timedelta(hours=self.hours)
        post_data = {
            "step": 600,
            "start_time": int(start_time.timestamp()),
            "hostnames": [urlooker_id],
            "end_time": int(now_time.timestamp()),
            "counters": [
                f'url_status/creator=ops-admin,domain={domain},from={src},ip={ip}'
            ],
            "consol_fun": "AVERAGE"
        }
        post_url = f'''{settings.DEPLOY_CONF.get('falcon', 'api_address')}/graph/history'''
        res_data = requests.post(post_url, data=json.dumps(post_data), headers=headers)
        res_data_list = res_data.json()
        return res_data_list[0]['Values']

    def monitor_info(self):
        ret_list = []
        ret_result_dict = self.__get_urlooker_id()
        for urlooker_id, result_info in ret_result_dict.items():
            # 不需要端口，只需要domain
            domain = urlparse(result_info['url']).netloc.split(':')[0]
            values = self.__get_falcon_monitor(
                urlooker_id=f'urlooker_{urlooker_id}',
                ip=result_info['ip'],
                src=self.__parse_agent[result_info['idc']],
                domain=domain)
            ret_list.append({
                'id': self.app_id,
                'values': values
            })
        return ret_list
