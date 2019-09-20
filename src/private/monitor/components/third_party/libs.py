import json
from .algorithm import DateAlgorithm, NumberAlgorithm, NumberJitterAlgorithm
from monitor.components.falcon_api import (
    add_endpoint_to_falcon_grp,
    get_grp_hosts,
    del_endpoint_to_falcon_grp,
    del_endpoint_to_graph,
)
from .vars import (THIRD_PARTY_HG,
                   THIRD_PARTY_PREFIX,
                   MONITOR_DATE_ALGORITHM,
                   MONITOR_NUMBER_ALGORITHM,
                   MONITOR_NUMBER_JITTER_ALGORITHM)
from public.util.libs import get_logger
from message.send_message import sender
from .vars import NOTICE_DOC_FUNC

logger = get_logger('monitor.components.third_party.libs')


class GetMonitorItemStatus:
    """
    获取监控项需要上传的status
    :status: 0: 正常，1：异常， 2：失效
    """

    def __init__(self, monitor_item, strategy_obj, jitter=False):
        self.monitor_item = monitor_item
        self.strategy_obj = strategy_obj
        self.jitter = jitter

    def __get_algorithm(self):
        if self.monitor_item in MONITOR_NUMBER_JITTER_ALGORITHM and self.jitter:
            return NumberJitterAlgorithm(self.strategy_obj)

        if self.monitor_item in MONITOR_NUMBER_ALGORITHM and not self.jitter:
            return NumberAlgorithm(self.strategy_obj)

        if self.monitor_item in MONITOR_DATE_ALGORITHM and not self.jitter:
            return DateAlgorithm(self.strategy_obj)

        raise Exception(f'{self.monitor_item} not assigned.')

    def get_usual_item(self):
        algorithm_obj = self.__get_algorithm()
        algorithm_obj.core_calculate()
        return algorithm_obj.usual_item_id

    def get_unusual_item(self):
        algorithm_obj = self.__get_algorithm()
        algorithm_obj.core_calculate()
        return algorithm_obj.unusual_item_id

    def get(self):
        algorithm_obj = self.__get_algorithm()
        algorithm_obj.core_calculate()
        return algorithm_obj.result_set


def add_status_ep_to_falcon(work_order_list: list, prefix=THIRD_PARTY_PREFIX):
    try:
        hosts = get_grp_hosts(THIRD_PARTY_HG)
        for work_order in work_order_list:
            hosts.append(f'''{prefix}_{work_order}''')
        logger.debug(f'{hosts} bind to falcon host group `{THIRD_PARTY_HG}`')
        add_endpoint_to_falcon_grp(hosts, THIRD_PARTY_HG)
    except Exception as e:
        logger.error(f'`add_status_ep_to_falcon({work_order}, {prefix})` 添加endpoint 到falcon')
        raise e


def del_status_ep_to_falcon(work_order, prefix=THIRD_PARTY_PREFIX):
    try:
        del_endpoint_to_graph(f'{prefix}_{work_order}')
        del_endpoint_to_falcon_grp(f'{prefix}_{work_order}', THIRD_PARTY_HG)
    except Exception as e:
        logger.error(f'`del_ep_to_falcon({work_order}, {prefix})` 删除falcon 的ep 信息')
        raise e


def __push_notice(detail_obj, **kwargs):
    if 1 == detail_obj.is_mail:
        kwargs['send_type'] = 'mail'
        sender(**kwargs)

    if 1 == detail_obj.is_message:
        kwargs['send_type'] = 'message'
        sender(**kwargs)

    if 1 == detail_obj.is_wechat:
        kwargs['send_type'] = 'wechat'
        sender(**kwargs)


# push third party jitter strategy notice
def push_third_party_jitter_notice(strategy_obj, monitor_modal_obj, jitter_number):
    doc_func = NOTICE_DOC_FUNC[f"jitter_{strategy_obj.monitor_item}"]
    doc = doc_func(
        strategy_obj.monitor_item,
        strategy_obj.op,
        jitter_number,
        strategy_obj.alert_number,
        strategy_obj.note,
        strategy_obj.work_order,
        strategy_obj.hours_ago,
        monitor_modal_obj
    )
    send_kwargs = {
        'title': f'''[PROBLEM][Ops监控][第三方服务监控(数值抖动)]''',
        'content': doc,
        'receiver_user_id_list': json.loads(strategy_obj.send_user_id),
        'work_order': strategy_obj.work_order
    }
    logger.debug(f"`push_third_party_jitter_notice()` send_kwargs: {send_kwargs}")
    __push_notice(strategy_obj, **send_kwargs)



# push third party strategy notice
def push_third_party_notice(strategy_obj, monitor_modal_obj, status):
    """
    :param strategy_obj: strategy object
    :param monitor_modal_obj: monitor modal object
    :param status: alarm status
    """

    # 获取发送文案
    doc_func = NOTICE_DOC_FUNC[strategy_obj.monitor_item]
    doc = doc_func(strategy_obj.monitor_item,
                   strategy_obj.op,
                   monitor_modal_obj.compare_num,
                   strategy_obj.alert_number,
                   strategy_obj.note,
                   strategy_obj.work_order,
                   monitor_modal_obj)
    real_status = 'PROBLEM' if status == 1 else 'OK'
    send_kwargs = {
        'title': f'''[{real_status}][Ops监控][第三方服务监控]''',
        'content': doc,
        'receiver_user_id_list': json.loads(strategy_obj.send_user_id),
        'work_order': strategy_obj.work_order
    }
    logger.debug(f"`push_third_party_notice()` send_kwargs: {send_kwargs}")
    __push_notice(strategy_obj, **send_kwargs)
