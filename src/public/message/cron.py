"""
crontab
"""
import datetime
from message.models import  MessageMail


def remain_7_days_log_cron():
    days_7_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    MessageMail.objects.filter(time__lt=days_7_ago).delete()