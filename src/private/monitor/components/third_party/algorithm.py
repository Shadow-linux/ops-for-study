"""
第三方监控，监控算法
"""
import datetime
from abc import ABCMeta, abstractmethod
from .vars import MONITOR_ITEMS, MONITOR_MODALS, THIRD_PARTY_GRAPH_PREFIX
from public.util.libs import get_logger
from monitor.components.falcon_api import get_graph_data


logger = get_logger('monitor.components.third_party.algorithm')


class BaseAlgorithm(metaclass=ABCMeta):
    # 指定的监控项
    monitor_items = MONITOR_ITEMS
    monitor_models = MONITOR_MODALS

    def __init__(self, strategy_obj):
        self.strategy_obj = strategy_obj
        self.result_set = {}
        # 异常结果的item id
        self.unusual_item_id = []
        # 异常结果的item id
        self.usual_item_id = []

    def op_result(self, op: str, compare_val, standard_val) -> int:
        # 1 是触发告警， 0 是正常
        logger.debug(f'''{compare_val} {op} {standard_val}''')
        result = 1 if eval(f'''{compare_val} {op} {standard_val}''') else 0
        print(result)
        return result

    def unusual_item(self, item_id: int, result: int):
        if result == 1:
            self.unusual_item_id.append(item_id)
            return
        self.usual_item_id.append(item_id)

    # 核心算法
    @abstractmethod
    def core_calculate(self):
        raise NotImplementedError('`core_calculate()` must be implemented.')


class DateAlgorithm(BaseAlgorithm):
    """
    日期算法
    """
    def core_calculate(self):
        # alert number
        alert_number = self.strategy_obj.alert_number
        monitor_model = self.monitor_models[self.strategy_obj.monitor_item]
        monitor_model_obj_list = monitor_model.objects.all()
        for monitor_model_obj in monitor_model_obj_list:
            result = self.op_result(self.strategy_obj.op, monitor_model_obj.compare_num, alert_number)
            self.result_set[monitor_model_obj.id] = result
            # 添加异常项
            self.unusual_item(monitor_model_obj.id, result)


class NumberAlgorithm(BaseAlgorithm):
    """
    数字算法
    """
    def core_calculate(self):
        # compare_number
        # alert number
        alert_number = self.strategy_obj.alert_number
        monitor_model = self.monitor_models[self.strategy_obj.monitor_item]
        monitor_model_obj_list = monitor_model.objects.all()
        for monitor_model_obj in monitor_model_obj_list:
            result = self.op_result(self.strategy_obj.op, monitor_model_obj.compare_num, alert_number)
            self.result_set[monitor_model_obj.id] = result
            # 添加异常项
            self.unusual_item(monitor_model_obj.id, result)


class NumberJitterAlgorithm(BaseAlgorithm):
    """
    数字抖动算法
    """
    def core_calculate(self):
        alert_number = self.strategy_obj.alert_number
        monitor_model = self.monitor_models[self.strategy_obj.monitor_item]
        monitor_model_obj_list = monitor_model.objects.all()
        for monitor_model_obj in monitor_model_obj_list:
            end_time = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
            start_time = end_time - datetime.timedelta(hours=self.strategy_obj.hours_ago)
            ep = f"{THIRD_PARTY_GRAPH_PREFIX}_{monitor_model_obj.work_order}"
            counter = f"value/item={self.strategy_obj.monitor_item},item_id={monitor_model_obj.id}"
            logger.debug(f'ep: {ep}, counter: {counter}')
            graph_datas = get_graph_data(start_time, end_time, [ep], [counter], 3600)[0]['Values']
            logger.debug(f'graph_data: {graph_datas}')
            # 第几个小时前的数据
            graph_number = int(graph_datas[0]['value']) if graph_datas[0]['value'] else 0
            # old - new
            jitter_number = graph_number - monitor_model_obj.compare_num
            logger.debug(f"策略 {self.strategy_obj.work_order}, {self.strategy_obj.note}")
            result = self.op_result(self.strategy_obj.op, jitter_number, alert_number)
            # 添加 result_set
            if result == 1:
                self.result_set[monitor_model_obj.id] = jitter_number
            # 添加异常项
            self.unusual_item(monitor_model_obj.id, result)
