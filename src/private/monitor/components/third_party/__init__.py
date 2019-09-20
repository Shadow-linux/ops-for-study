"""
第三方监控的入口文件
"""
from public.util.libs import get_logger, datetime2timestamp
from .save_data import (
    aliyun_ecs_save,
    aliyun_rds_save,
    aliyun_nas_save,
    aliyun_vpn_save,
    aliyun_domain_save,
    yuexin_sms_save,
    wanweiyiyuan_bank_identity_save,
    xuncheng_eryaosu_save,
    tencent_message_save,
)
from monitor.models import MonitorThirdPartyStrategy, MonitorThirdPartyJitterStrategy, MonitorTPStrategyItemRel
from monitor.components.falcon_api import push_data_to_open_falcon
from .vars import (THIRD_PARTY_PREFIX, MONITOR_GRAPH_ITEMS, MONITOR_MODALS, THIRD_PARTY_GRAPH_PREFIX,
                   THIRD_PARTY_GRAPH_HG)
from .libs import GetMonitorItemStatus, push_third_party_notice, push_third_party_jitter_notice

logger = get_logger('monitor.third_party.__init__')
# 保存数据的方法
SAVE_DATA_FUNCS = (
    aliyun_ecs_save,
    aliyun_domain_save,
    aliyun_vpn_save,
    aliyun_rds_save,
    aliyun_nas_save,
    yuexin_sms_save,
    wanweiyiyuan_bank_identity_save,
    xuncheng_eryaosu_save,
    tencent_message_save,
)


# 更新第三方监控数据
def save_third_party_data():
    for save_func in SAVE_DATA_FUNCS:
        try:
            save_func()
        except Exception as e:
            logger.error(f'{save_func.__name__} 保存数据失败')
            logger.exception(e)


# push monitor jitter notice
def push_graph_jitter_notice():
    m_tp_jitter_strategy_obj_list = MonitorThirdPartyJitterStrategy.objects.filter(is_alarm=1)
    for strategy_obj in m_tp_jitter_strategy_obj_list:
        # 获取是否告警状态
        try:
            status_obj = GetMonitorItemStatus(strategy_obj.monitor_item, strategy_obj, True)
            status_dict = status_obj.get()
            logger.debug(f'monitor jitter notice: {status_dict}')
            monitor_modal = MONITOR_MODALS[strategy_obj.monitor_item]
            for item_id, jitter_number in status_dict.items():
                model_obj = monitor_modal.objects.get(id=item_id)
                if model_obj.is_monitor == 1:
                    push_third_party_jitter_notice(strategy_obj, model_obj, jitter_number)
        except Exception as e:
            logger.error('推送监控数据抖动告警出错')
            logger.exception(e)


# push monitor status and graph to falcon
def push_status_graph_notice(is_graph=True):
    monitor_tp_strategy_obj_list = MonitorThirdPartyStrategy.objects.all()
    for strategy_obj in monitor_tp_strategy_obj_list:
        if strategy_obj.is_alarm == 1:
            try:
                # 获取monitor item status
                status_obj = GetMonitorItemStatus(strategy_obj.monitor_item, strategy_obj)
                status_dict = status_obj.get()
                monitor_modal = MONITOR_MODALS[strategy_obj.monitor_item]
                logger.debug(f'第三方监控策略 item: [{monitor_modal.__name__}] result dict: {status_dict}')
                for item_id, status in status_dict.items():
                    try:
                        model_obj = monitor_modal.objects.get(id=item_id)
                        # 第三方告警策略与监控数据告警关系, 用于状态为problem 和 ok
                        strategy_alarm_rel_obj = MonitorTPStrategyItemRel.objects.get(
                            monitor_item=strategy_obj.monitor_item,
                            monitor_item_id=model_obj.id,
                            strategy_id=strategy_obj.id
                        )
                        # 判断当前是否处于告警状态，如果状态相同则不用发送消息
                        logger.debug(f'监控项目: itemId: {model_obj.id}, 状态: {strategy_alarm_rel_obj.current_alarm}')
                        if status != strategy_alarm_rel_obj.current_alarm and model_obj.is_monitor == 1:
                            # 推送通知信息
                            push_third_party_notice(strategy_obj, model_obj, status)
                            # 更新当前告警状态
                            strategy_alarm_rel_obj.current_alarm = status
                            strategy_alarm_rel_obj.save()
                    except Exception as e:
                        logger.error(
                            f'''
                                monitor_modal: {monitor_modal}, 
                                item_id: {item_id}, 
                                status: {status }, 
                                strategy_obj: {strategy_obj}
                            '''
                        )
                        logger.exception(e)
            except Exception as e:
                logger.error('第三方监控推送状态告警失败')
                logger.exception(e)

        if is_graph and strategy_obj.monitor_item in MONITOR_GRAPH_ITEMS:
            monitor_modal = MONITOR_MODALS[strategy_obj.monitor_item]
            for monitor_modal_obj in monitor_modal.objects.all():
                try:
                    commit_value = monitor_modal_obj.compare_num
                    # 推送图表数据到falcon
                    push_data_to_open_falcon(
                        endpoint=f"{THIRD_PARTY_GRAPH_PREFIX}_{monitor_modal_obj.work_order}",
                        metric='value',
                        value=commit_value,
                        timestamp=datetime2timestamp(),
                        step=3600,
                        tags=f'item={strategy_obj.monitor_item},item_id={monitor_modal_obj.id}'
                    )
                    logger.debug(f'''
                        推送图表数据到falcon,
                        endpoint="{THIRD_PARTY_GRAPH_PREFIX}_{monitor_modal_obj.work_order}",
                        metric='status',
                        value={commit_value},
                        timestamp={datetime2timestamp()},
                        step=3600,
                        tags='item={strategy_obj.monitor_item},item_id={monitor_modal_obj.id}'
                        ''')
                except Exception as e:
                    logger.error(f'''
                    `push_data_to_open_falcon(endpoint={THIRD_PARTY_GRAPH_PREFIX}_{strategy_obj.work_order},
                    tags='item={strategy_obj.monitor_item},item_id={monitor_modal_obj.id}'
                    **kwargs)`, 
                     推送图表数据到falcon失败''')
                    logger.exception(e)
