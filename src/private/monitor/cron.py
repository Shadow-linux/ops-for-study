from .components.third_party import save_third_party_data, push_status_graph_notice, push_graph_jitter_notice
from public.util.libs import get_logger

logger = get_logger('monitor.cron')


def monitor_third_party_cron():
    # 当更新信息失败后
    logger.info('[cron] 更新第三方监控信 started')
    try:
        save_third_party_data()
        push_status_graph_notice()
        push_graph_jitter_notice()
    except Exception as e:
        logger.error('[cron] 更新第三方监控信 出错')
        logger.exception(e)
