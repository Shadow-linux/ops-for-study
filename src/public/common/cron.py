"""
Crontab
"""
import requests
import json
import datetime
from .models import AppALiveBrief, AppAliveStatistics
from public.util.libs import get_logger
from public.util import call_mysql
from apps.models import AppDetail
from monitor.components.app_alive import AppAliveGraph

logger = get_logger('common.cron')


# 收集app每天的错误信息点, 只针对release 环境，用于展示在dashboard
def collect_app_alive_failed_point_cron():
    with call_mysql.OpsMysqlClient() as cursor:
        sql = '''select `url`, `ops_cp_app_id` from urlooker.strategy where environment = 'release';'''
        cursor.execute(sql)
        result_set = cursor.fetchall()
    for app_obj in result_set:
        try:
            app_d_obj = AppDetail.objects.get(id=app_obj['ops_cp_app_id'])
            app_alive_graph_obj = AppAliveGraph(
                environment='release',
                app_id=app_obj['ops_cp_app_id'],
                check_api=app_obj['url'],
                hours=24
            )
            monitor_info_list = app_alive_graph_obj.monitor_info()
            failed_point_count = 0
            for mf in monitor_info_list[0]['values']:
                if isinstance(mf['value'], float):
                    if mf['value'] != 0:
                        logger.debug(f'app alive 连接失败点数据: {app_d_obj.app_name} {mf}')
                        failed_point_count += 1
            AppAliveStatistics.objects.create(
                app_name=app_d_obj.app_name,
                failed_point_amount=failed_point_count
            )
        except Exception as e:
            logger.warning('收集app alive 统计数据出错, 未找到配置...')
            # logger.exception(e)


# 分类处1day 30day 90day 365 day
def category_app_alive_brief_cron():
    # 1day
    now_date = datetime.datetime.now()
    app_statistics_list = AppAliveStatistics.objects.values('app_name').distinct()

    def brief_1_day():
        logger.info(f'[计划任务]: 分类app alive 1 day')
        days = 1
        # 1440 * 1 / 5 (间隔5分钟一个点)
        all_amount = 288
        one_day_ago = now_date - datetime.timedelta(days=days)
        for app_dic in app_statistics_list:
            app_alive_obj_list = AppAliveStatistics.objects.filter(app_name=app_dic['app_name'],
                                                                   created__gt=one_day_ago,
                                                                   created__lt=now_date)
            failed_amount = 0
            for app_alive_obj in app_alive_obj_list:
                failed_amount = app_alive_obj.failed_point_amount + failed_amount
            success_rate = round(1.0 - (failed_amount / all_amount), 3) * 100
            try:
                model_obj = AppALiveBrief.objects.get(app_name=app_dic['app_name'], days=days)
            except Exception:
                model_obj = AppALiveBrief()
                model_obj.app_name = app_dic['app_name']
                model_obj.days = 1
            model_obj.success_rate = success_rate
            model_obj.save()

    def brief_30_day():
        logger.info(f'[计划任务]: 分类app alive 30 day')
        days = 30
        # 1440 * 30 / 5
        all_amount = 8640
        one_day_ago = now_date - datetime.timedelta(days=days)
        for app_dic in app_statistics_list:
            app_alive_obj_list = AppAliveStatistics.objects.filter(app_name=app_dic['app_name'],
                                                                   created__gt=one_day_ago,
                                                                   created__lt=now_date)
            failed_amount = 0
            for app_alive_obj in app_alive_obj_list:
                failed_amount = app_alive_obj.failed_point_amount + failed_amount
            success_rate = round(1.0 - (failed_amount / all_amount), 3) * 100
            try:
                model_obj = AppALiveBrief.objects.get(app_name=app_dic['app_name'], days=days)
            except Exception:
                model_obj = AppALiveBrief()
                model_obj.app_name = app_dic['app_name']
                model_obj.days = days
            model_obj.success_rate = success_rate
            model_obj.save()

    def brief_90_day():
        logger.info(f'[计划任务]: 分类app alive 90 day')
        days = 90
        # 1440 * 90 / 5
        all_amount = 25920
        one_day_ago = now_date - datetime.timedelta(days=days)
        for app_dic in app_statistics_list:
            app_alive_obj_list = AppAliveStatistics.objects.filter(app_name=app_dic['app_name'],
                                                                   created__gt=one_day_ago,
                                                                   created__lt=now_date)
            failed_amount = 0
            for app_alive_obj in app_alive_obj_list:
                failed_amount = app_alive_obj.failed_point_amount + failed_amount
            success_rate = round(1.0 - (failed_amount / all_amount), 3) * 100
            try:
                model_obj = AppALiveBrief.objects.get(app_name=app_dic['app_name'], days=days)
            except Exception:
                model_obj = AppALiveBrief()
                model_obj.app_name = app_dic['app_name']
                model_obj.days = days
            model_obj.success_rate = success_rate
            model_obj.save()

    brief_1_day()
    brief_30_day()
    brief_90_day()




