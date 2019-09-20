"""
falcon 回调路由
"""
import json
from abc import ABCMeta, abstractmethod
from message.busniess import ngx_access_doc
from activity.business.models import AccessAlarmResult, AccessAlarmStrategy
from message.send_message import sender
from public.util.libs import get_logger

logger = get_logger('openapi.falcon.libs')


class FalconBaseImplement(metaclass=ABCMeta):

    # 处理接收falcon值（用于处理自定义监控值的规范）
    #  0: 正常状态
    #  1: 异常状态
    #  2: 数据失效
    def falcon_receive_value(self, value):
        falcon_status = {
            0: 'ok',
            1: 'problem',
            2: 'expire'
        }
        return falcon_status.get(int(value), 'none')

    def send(self, detail_obj, **kwargs):
        if 1 == detail_obj.is_mail:
            kwargs['send_type'] = 'mail'
            sender(**kwargs)

        if 1 == detail_obj.is_message:
            kwargs['send_type'] = 'message'
            sender(**kwargs)

        if 1 == detail_obj.is_wechat:
            kwargs['send_type'] = 'wechat'
            sender(**kwargs)

    # 解析出 tags
    def parse_tags(self, tags: str):
        ret_dict = {}
        for tag in tags.split(','):
            key, value = tag.split(':')
            ret_dict[key] = value
        return ret_dict

    # 灵活传入各种值, 获取相应的文档
    @abstractmethod
    def get_doc(self, *args, **kwargs):
        # left_value = self.falcon_receive_value(value)
        raise NotImplementedError('`get_doc()` must be implemented.')

    @abstractmethod
    def launch(self):
        # doc = self.get_doc(*args, **kwargs)
        # self.send(**send_kwargs)
        raise NotImplementedError('`launch()` must be implemented.')


class NgxAccess(FalconBaseImplement):

    def __init__(self, query_params):
        self.query_params = query_params
        self.doc_maps = {
            'average': ngx_access_doc._average,
            'max': ngx_access_doc._max,
            'cost_percent': ngx_access_doc.cost_percent
        }

    def get_doc(self, alarm_name, value, alarm_strategy, cost, op, result_obj):
        """
        :param alarm_strategy: 策略
        :param op: 操作符
        :param alarm_name: 告警名称
        :param value: falcon 值
        :param cost: 花费时间
        :param result_obj: 结果对象
        :return:
        """

        def ok():
            return doc_func(
                alarm_name,
                result_obj.latest_time,
                result_obj.where_condition,
                cost,
                result_obj.match_count,
                op,
                alarm_strategy,
                json.loads(result_obj.result_set)
            )

        def problem():
            return ok()

        def expire():
            return f'''
            <p><b>监控名:</b> {alarm_name} </p> 
            <p><b>监控接口:</b> {result_obj.where_condition} </p>
            <p><b>Note:</b> 数据失效，监控数据未提交。</p>'''

        def none():
            return f'''
            <p><b>监控名:</b> {alarm_name} </p> 
            <p><b>监控接口:</b> {result_obj.where_condition} </p>
            <p><b>Note:</b> Unknown error.</p>
            '''

        left_value = self.falcon_receive_value(value)
        doc_func = self.doc_maps[alarm_strategy['strategy']]
        doc = eval(f'{left_value}')()
        return doc

    def launch(self):
        work_order = self.query_params['endpoint'].split('ngx_access_')[1]
        result_obj = AccessAlarmResult.objects.get(work_order=work_order)
        detail_obj = AccessAlarmStrategy.objects.get(work_order=work_order)
        # 判断是否开启了告警
        if detail_obj.is_alarm == 1:
            doc = self.get_doc(
                detail_obj.alarm_name,
                self.query_params['left_value'],
                json.loads(result_obj.alarm_strategy),
                detail_obj.cost,
                detail_obj.op,
                result_obj
            )
            send_kwargs = {
                'title': f'''[{self.query_params['status']}][Ops监控][API接口 质量告警]''',
                'content': doc,
                'receiver_user_id_list': json.loads(detail_obj.send_user_id),
                'work_order': work_order
            }
            logger.debug(send_kwargs)
            self.send(detail_obj, **send_kwargs)


class ThirdPartyGraph(FalconBaseImplement):
    def __init__(self, query_params):
        self.query_params = query_params

    def get_doc(self, *args, **kwargs):
        pass

    def launch(self):
        pass


class Urlooker(FalconBaseImplement):
    def __init__(self, query_params):
        self.query_params = query_params

    def get_doc(self, *args, **kwargs):
        pass

    def launch(self):
        pass


class Default(FalconBaseImplement):
    def __init__(self, query_params):
        self.query_params = query_params

    def get_doc(self, *args, **kwargs):
        pass

    def launch(self):
        pass


def analyze_endpoint(endpoint: str):
    """
    分析出对应关系
    :return 执行方法
    """
    db_maps = {
        'urlooker': Urlooker,
        'ngx_access': NgxAccess,
        'default': Default,
        'third_party_graph': ThirdPartyGraph
    }
    # 现在需要在ops 告警的前缀
    filter_list = ['urlooker', 'ngx_access', 'third_party_graph']
    for con in filter_list:
        if endpoint.startswith(con):
            return db_maps[con]
    return db_maps['default']
