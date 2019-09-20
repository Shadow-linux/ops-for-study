"""
crontab
"""
import datetime
from .models import  OperationGlobalLog


def remain_7_days_log_cron():
    days_7_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    OperationGlobalLog.objects.filter(time__lt=days_7_ago).delete()