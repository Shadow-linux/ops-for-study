from .ngx_access_alarm import ngx_access_launch
from public.util.libs import get_logger

logger = get_logger('activity.business.cron')

def ngx_access_cron():
    logger.info('[cron] ngx_access_cron started.')
    try:
        ngx_access_launch()
    except Exception as e:
        logger.exception(e)