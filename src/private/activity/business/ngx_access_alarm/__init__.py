# coding: utf-8
"""
access log 告警， 主要通过判断 request cost time
"""
import datetime
import requests
import numpy
import json
import asyncio
from django.conf import settings
from activity.business.models import AccessAlarmStrategy, AccessAlarmResult
from activity.business.vars import NGX_ACCESS_FALCON_PREFIX
from public.util.libs import local2utc, UTC_FORMAT_FULL, datetime2timestamp, get_logger
from monitor.components.falcon_api import push_data_to_open_falcon

logger = get_logger('activity.business.ngx_access_alarm.main')

# Falcon endpoint prefix
EP_PREFIX = NGX_ACCESS_FALCON_PREFIX
# ES access log index
ES_INDEX = 'plog-callchain*'
# 获取的使用sql插件es地址
SQL_ES_ADDRESS = settings.DEPLOY_CONF.get('business', 'sql_es_address')
# request header
HEADERS = {
    'Content-Type': 'application/json'
}


# 返回UTC 时间
def get_current_fmt_time(now_time_obj):
    now = local2utc(now_time_obj)
    return now.strftime(UTC_FORMAT_FULL)


# 返回UTC 时间
def get_ago_fmt_time(now_time_obj, minutes: int):
    now = local2utc(now_time_obj)
    minutes_ago_obj = now - datetime.timedelta(minutes=minutes)
    return minutes_ago_obj.strftime(UTC_FORMAT_FULL)


# 获取时间范围内的指定url的cost 时间
def filter_cost_to_time_range(start_time: str, end_time: str, where_condition: dict):
    """
    :param start_time: 起始时间
    :param end_time: 结束时间
    :param where_condition: 条件
    :return:
    """
    _where_content = []
    for key, value in where_condition.items():
        _where_content.append(f'''{key} = "{value}"''')
    where_content = " and ".join(_where_content)
    es_sql = ''
    res_data = {}
    # 第一次循环是确认次数，第二次是查询真实数据
    count = 1
    for _ in range(0, 2):
        es_sql = '''select cost from {ES_INDEX} where
                 @timestamp >= "{start_time}" 
                 and @timestamp <= "{end_time}" 
                 and  {where_content} limit {count}'''.format(
            ES_INDEX=ES_INDEX,
            start_time=start_time,
            end_time=end_time,
            where_content=where_content,
            count=count
        )
        res = requests.get(SQL_ES_ADDRESS, headers=HEADERS, params={'sql': es_sql}, verify=False)
        res_data = res.json()
        count = res_data['hits']['total']
    logger.debug(es_sql)
    return [float(dd.get('_source').get('cost', 0)) for dd in res_data['hits']['hits']]


# 查询request id
def filter_requestid_list(start_time: str, end_time: str, where_condition: dict, cost_condition: str):
    _where_content = []
    for key, value in where_condition.items():
        _where_content.append(f'''{key} = "{value}"''')
    where_content = " and ".join(_where_content)
    es_sql = '''select requestid from {ES_INDEX} where
                     @timestamp >= "{start_time}" and
                    @timestamp <= "{end_time}" and
                    {where_content} and {cost_condition} limit 3'''.format(
        ES_INDEX=ES_INDEX,
        start_time=start_time,
        end_time=end_time,
        where_content=where_content,
        cost_condition=cost_condition
    )
    logger.debug(es_sql)
    res = requests.get(SQL_ES_ADDRESS, headers=HEADERS, params={'sql': es_sql}, verify=False)
    res_data = res.json()
    return [(dd.get('_source').get('requestid', 'null')) for dd in res_data['hits']['hits']]


class NgxAlarmStrategy:
    """
    nginx access alarm strategy
    """

    def __init__(self, latest_time, cost, where_condition, op):
        """
        :param latest_time: 最近几分钟
        :param cost: 花费时间的告警指标
        """
        self.now = datetime.datetime.now()
        self.end_time = get_current_fmt_time(self.now)
        self.start_time = get_ago_fmt_time(self.now, latest_time)
        self.cost = cost
        self.op = op
        self.where_condition = where_condition
        self.cost_time_list = self.__get_cost_time_list()
        self.result_set = {}

    def __numpy_where(self, handle_list):
        if self.op == '>':
            return numpy.where(handle_list > self.cost)[0]

        if self.op == '==':
            return numpy.where(handle_list == self.cost)[0]

        if self.op == '<':
            return numpy.where(handle_list < self.cost)[0]

        if self.op == '>=':
            return numpy.where(handle_list >= self.cost)[0]

        if self.op == '<=':
            return numpy.where(handle_list <= self.cost)[0]

        if self.op == '!=':
            return numpy.where(handle_list <= self.cost)[0]

    def __get_cost_time_list(self):
        return filter_cost_to_time_range(self.start_time,
                                         self.end_time,
                                         where_condition=self.where_condition)

    # 平均消耗
    def average(self, **kwargs):
        if not self.cost_time_list:
            return 0
        avg_num = numpy.average(self.cost_time_list)
        handle_list = numpy.array(self.cost_time_list)
        res_list = self.__numpy_where(handle_list)
        match_count = len(res_list)
        request_ids = []
        if match_count > 0:
            request_ids = filter_requestid_list(self.start_time,
                                                self.end_time,
                                                self.where_condition,
                                                f'''cost = "{int(self.cost_time_list[res_list[0]])}"''')
        # 记录 avg_num
        self.result_set = {
            'average': avg_num,
            'request_id': request_ids
        }
        """numpy 示例
        >>> a = numpy.array([2,4,6,8,10])
        >>> arr = a[numpy.where(a>8)]
        >>> arr
        array([10])
        """
        # 当均值大于预先设定的值
        # if avg_num > self.cost:
        if eval(f'{avg_num} {self.op} {self.cost}'):
            return match_count
        # 如果没有匹配中规则 直接清空取样ID
        self.result_set['request_id'] = []
        return 0

    def max(self, **kwargs):
        if not self.cost_time_list:
            return 0
        max_num = numpy.max(self.cost_time_list)

        handle_list = numpy.array(self.cost_time_list)
        res_list = self.__numpy_where(handle_list)
        match_count = len(res_list)
        request_ids = []
        if match_count > 0:
            request_ids = filter_requestid_list(self.start_time,
                                                self.end_time,
                                                self.where_condition,
                                                f'''cost = "{int(self.cost_time_list[res_list[0]])}"''')
        # 记录max_num
        self.result_set = {
            'max': max_num,
            'request_id': request_ids
        }
        # 当最大值大于预先设定的值 # if max_num > self.cost:
        if eval(f'{max_num} {self.op} {self.cost}'):
            return match_count
        self.result_set['request_id'] = []
        return 0

    # 判断大于cost 的占比是否大于预设的占比值
    def cost_percent(self, **kwargs):
        if not self.cost_time_list:
            return 0
        percent = kwargs.get('percent', None)
        if not percent:
            return 0
        total_count = len(self.cost_time_list)
        handle_list = numpy.array(self.cost_time_list)
        logger.debug(f'{self.cost} {type(self.cost)}')
        # cal = f'{handle_list}{self.op}float({self.cost})'
        # logger.debug(cal)
        # res_list = numpy.where(cal)[0]
        res_list = self.__numpy_where(handle_list)
        match_count = len(res_list)
        request_ids = []
        if match_count > 0:
            request_ids = filter_requestid_list(
                self.start_time,
                self.end_time,
                self.where_condition,
                f'''cost = "{int(self.cost_time_list[res_list[0]])}"''')
        logger.debug(res_list)
        logger.debug(f'match count: {match_count}, total: {total_count}')
        real_percent = match_count / total_count
        # 记录 avg_num
        self.result_set = {
            'real_percent': round(real_percent, 2),
            'percent': round(percent, 2),
            'request_id': request_ids
        }
        # if real_percent > percent:
        if eval(f'{real_percent} {self.op} {percent}'):
            return match_count
        # 如果没有匹配中规则 直接清空取样ID
        self.result_set['request_id'] = []
        return 0


# nginx access alarm 启动
def ngx_access_launch():
    def __save_result(m_obj, mc, latest_time, _result_set):
        try:
            _obj = AccessAlarmResult.objects.get(work_order=m_obj.work_order)
        except Exception:
            _obj = AccessAlarmResult()
            _obj.work_order = m_obj.work_order

        _obj.alarm_strategy = m_obj.alarm_strategy
        _obj.where_condition = m_obj.where_condition
        _obj.match_count = mc
        _obj.cost = m_obj.cost
        _obj.latest_time = latest_time
        _obj.result_set = json.dumps(_result_set)
        _obj.save()

    async def __launch_handle(_model_obj):
        alarm_strategy = json.loads(_model_obj.alarm_strategy)
        op = _model_obj.op
        cost = _model_obj.cost
        where_condition = json.loads(_model_obj.where_condition)
        strategy = alarm_strategy['strategy']
        alarm_strategy_obj = NgxAlarmStrategy(_model_obj.latest_time, cost, where_condition, op)
        logger.debug(f'''cost_time_list: {alarm_strategy_obj.cost_time_list}''')
        # 根据条件执行方法
        match_count = getattr(alarm_strategy_obj, strategy)(**alarm_strategy, op=op)
        result_set = alarm_strategy_obj.result_set
        # 保存结果集
        __save_result(_model_obj, match_count, _model_obj.latest_time, result_set)
        logger.debug(f'''
                    work_order: {_model_obj.work_order}
                    alarm_strategy: {alarm_strategy} ;
                    where_condition: {where_condition};
                    result_set: {result_set};
                    cost: {cost};
                    match_count: {match_count}''')
        commit_value = 1 if match_count > 0 else 0
        try:
            push_data_to_open_falcon(
                endpoint=f"{EP_PREFIX}_{_model_obj.work_order}",
                metric="status",
                value=commit_value,
                timestamp=datetime2timestamp(),
                tags='type=ngx_access'
            )
        except Exception as e:
            logger.error(f'策略ID: {_model_obj.work_order} 推送open-falcon 错误')
            logger.exception(e)

    queryset = AccessAlarmStrategy.objects.all()
    tasks = []
    for model_obj in queryset:
        # __launch_handle(model_obj)
        tasks.append(__launch_handle(model_obj))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
