"""
监控数据入库
"""
import datetime
from .monitor_api import (
    aliyun_ecs_api,
    aliyun_rds_api,
    aliyun_nas_api,
    aliyun_domain_api,
    aliyun_vpn_api,
    yuexin_sms_api,
    wanweiyiyuan_bank_identity_api,
    tencent_sms_api,
    xuncheng_eryaosu_api,
)
from monitor.models import (
    MonitorECS,
    MonitorRDS,
    MonitorNAS,
    MonitorDomain,
    MonitorVPN,
    MonitorYueXinSms,
    MonitorWanWeiYiYuanBankIdentity,
    MonitorTencentSms,
    MonitorXunChengEryaosu
)
from public.util.libs import utc2local, UTC_FORMAT_FULL, get_work_order
from public.util.libs import get_logger

logger = get_logger('monitor.components.third_party.save_data')


def __compare_date(expire_time, now_time=None):
    if not now_time:
        now_time = datetime.datetime.now()
    time_obj = expire_time - now_time
    return time_obj.days


def aliyun_ecs_save():
    try:
        ecs_obj_list = aliyun_ecs_api()
        logger.debug(f"`aliyun_ecs_api()`: {ecs_obj_list}")
        for ecs_obj in ecs_obj_list:
            try:
                monitor_ecs_obj = MonitorECS.objects.get(server_id=ecs_obj.instance_id)
                if monitor_ecs_obj.is_monitor != 1:
                    continue
            except Exception:
                monitor_ecs_obj = MonitorECS()
                monitor_ecs_obj.server_id = ecs_obj.instance_id
                # 添加endpoint 到 falcon grp

            monitor_ecs_obj.hostname = ecs_obj.hostname
            monitor_ecs_obj.status = ecs_obj.status
            monitor_ecs_obj.create_time = ecs_obj.created
            monitor_ecs_obj.expire_time = ecs_obj.expired_time
            monitor_ecs_obj.compare_num = __compare_date(monitor_ecs_obj.expire_time)
            monitor_ecs_obj.save()

    except Exception as e:
        logger.error(f'`aliyun_ecs_save()` error')
        raise e


def aliyun_rds_save():
    try:
        rds_list = aliyun_rds_api()
        logger.debug(f"`aliyun_rds_api()`: {rds_list}")
        for rds in rds_list:
            # 跳过不是预付费的 rds 统计
            if rds['PayType'] != 'Prepaid':
                continue
            try:
                monitor_rds_obj = MonitorRDS.objects.get(instance_id=rds['DBInstanceId'])
                if monitor_rds_obj.is_monitor != 1:
                    continue
            except Exception:
                monitor_rds_obj = MonitorRDS()
                monitor_rds_obj.instance_id = rds['DBInstanceId']

            monitor_rds_obj.instance_desc = rds['DBInstanceDescription']
            monitor_rds_obj.status = rds['DBInstanceStatus']
            monitor_rds_obj.create_time = utc2local(datetime.datetime.strptime(rds['CreateTime'], UTC_FORMAT_FULL))
            monitor_rds_obj.expire_time = utc2local(datetime.datetime.strptime(rds['ExpireTime'], UTC_FORMAT_FULL))
            monitor_rds_obj.compare_num = __compare_date(monitor_rds_obj.expire_time)
            monitor_rds_obj.save()

    except Exception as e:
        logger.error(f'`aliyun_rds_save()` error')
        raise e


def aliyun_nas_save():
    try:
        data_list = aliyun_nas_api()
        logger.debug(f"`aliyun_nas_api()`: {data_list}")
        nas_list, nas_pkg_list = data_list
        for nas in nas_list:
            pkg_ids = [pkg_dict['PackageId'] for pkg_dict in nas['Packages']['Package']]
            for pkg_id in pkg_ids:
                try:
                    monitor_nas_obj = MonitorNAS.objects.get(system_id=nas['FileSystemId'], package_id=pkg_id)
                    if monitor_nas_obj.is_monitor != 1:
                        continue
                except Exception:
                    monitor_nas_obj = MonitorNAS()
                    monitor_nas_obj.system_id = nas['FileSystemId']
                    monitor_nas_obj.package_id = pkg_id

                monitor_nas_obj.desc = nas['Destription']
                # pkg id 信息
                for nas_pkg in nas_pkg_list:
                    if nas_pkg['packageId'] == pkg_id:
                        monitor_nas_obj.create_time = datetime.datetime.fromtimestamp(nas_pkg['startTime'])
                        monitor_nas_obj.expire_time = datetime.datetime.fromtimestamp(nas_pkg['endTime'])
                        monitor_nas_obj.compare_num = __compare_date(monitor_nas_obj.expire_time)
                        monitor_nas_obj.save()
                        break
    except Exception as e:
        logger.error(f'`aliyun_nas_save()` error')
        raise e


def aliyun_domain_save():
    try:
        data_list = aliyun_domain_api()
        logger.debug(f"`aliyun_domain_api()`: {data_list}")
        for data in data_list:
            try:
                model_obj = MonitorDomain.objects.get(domain=data['DomainName'])
                if model_obj.is_monitor != 1:
                    continue
            except Exception:
                model_obj = MonitorDomain()
                model_obj.domain = data['DomainName']

            model_obj.status = data['DomainAuditStatus']
            model_obj.create_time = datetime.datetime.fromtimestamp(int(str(data['RegistrationDateLong'])[:10]))
            model_obj.expire_time = datetime.datetime.fromtimestamp(int(str(data['ExpirationDateLong'])[:10]))
            model_obj.compare_num = __compare_date(model_obj.expire_time)
            model_obj.save()

    except Exception as e:
        logger.error(f'`aliyun_domain_save()` error')
        raise e


def aliyun_vpn_save():
    try:
        data_list = aliyun_vpn_api()
        logger.debug(f"`aliyun_vpn_api()`: {data_list}")
        for data in data_list:
            try:
                model_obj = MonitorVPN.objects.get(vpc_id=data['VpcId'], vpn_id=data['VpnGatewayId'])
                if model_obj.is_monitor != 1:
                    continue
            except Exception:
                model_obj = MonitorVPN()
                model_obj.vpc_id = data['VpcId']
                model_obj.vpn_id = data['VpnGatewayId']

            model_obj.desc = data['Description']
            model_obj.status = data['Status']
            model_obj.create_time = datetime.datetime.fromtimestamp(int(str(data['CreateTime'])[:10]))
            model_obj.expire_time = datetime.datetime.fromtimestamp(int(str(data['EndTime'])[:10]))
            model_obj.compare_num = __compare_date(model_obj.expire_time)
            model_obj.save()

    except Exception as e:
        logger.error(f'`aliyun_vpn_save()` error')
        raise e


def yuexin_sms_save():
    try:
        data_list = yuexin_sms_api()
        logger.debug(f"`yuexin_sms_api()`: {data_list}")
        work_order_list = []
        for data in data_list:
            try:
                model_obj = MonitorYueXinSms.objects.get(username=data['username'])
                if model_obj.is_monitor != 1:
                    continue
            except Exception:
                model_obj = MonitorYueXinSms()
                model_obj.username = data['username']
                model_obj.work_order = get_work_order(work_type='third_party')
                work_order_list.append(model_obj.work_order)

            model_obj.req_code = data['ReqCode']
            model_obj.req_message = data['ReqMsg']
            model_obj.balance = data['Balance']
            model_obj.compare_num = data['Balance']
            model_obj.save()

    except Exception as e:
        logger.error(f'`yuexin_message_save()` error')
        raise e


def xuncheng_eryaosu_save():
    try:
        data_list = xuncheng_eryaosu_api()
        logger.debug(f"`xuncheng_eryaosu_api()`: {data_list}")
        for data in data_list:
            try:
                model_obj = MonitorXunChengEryaosu.objects.get(key=data['key'])
                if model_obj.is_monitor != 1:
                    continue
            except Exception:
                model_obj = MonitorXunChengEryaosu()
                model_obj.work_order = get_work_order(work_type='third_party')
                model_obj.key = data['key']
            model_obj.reason = data['reason']
            model_obj.name_desc = data['result'][0]['name']
            model_obj.number = int(data['result'][0]['number'])
            model_obj.compare_num = int(data['result'][0]['number'])
            model_obj.error_code = data['error_code']
            model_obj.save()
    except Exception as e:
        logger.error(f'`xuncheng_eryaosu_save()` error')
        raise e


def wanweiyiyuan_bank_identity_save():
    try:
        data_list = wanweiyiyuan_bank_identity_api()
        logger.debug(f"`wanweiyiyuan_bank_identity_api()`: {data_list}")
        for data in data_list:
            try:
                model_obj = MonitorWanWeiYiYuanBankIdentity.objects.get(api_name=data['apiName'])
                if model_obj.is_monitor != 1:
                    continue
            except Exception:
                model_obj = MonitorWanWeiYiYuanBankIdentity()
                model_obj.work_order = get_work_order(work_type='third_party')
                model_obj.api_name = data['apiName']

            model_obj.compare_num = int(data['remainUnit'])
            model_obj.remain_unit = int(data['remainUnit'])
            model_obj.total_unit = int(data['totalUnit'])
            model_obj.save()
    except Exception as e:
        logger.error(f'`wanweiyiyuan_bank_identity_save()` error')
        raise e


def tencent_message_save():
    try:
        data_list = tencent_sms_api()
        logger.debug(f"`tencent_sms_api()`: {data_list}")
        for data in data_list:
            try:
                model_obj = MonitorTencentSms.objects.get(package_id=data['package_id'])
                if model_obj.is_monitor != 1:
                    continue
            except Exception:
                model_obj = MonitorTencentSms()
                model_obj.work_order = get_work_order(work_type='third_party')
                model_obj.package_id = data['package_id']

            model_obj.compare_num = int(data['amount']) - int(data['used'])
            model_obj.amount = data['amount']
            model_obj.used = data['used']
            model_obj.save()
    except Exception as e:
        logger.error(f'`tencent_message_save()` error')
        raise e
