"""
cmdb 需要做的定时任务都在这里
"""
import datetime
import json
from cmdb.cloud.models import AliyunKeys, AliyunEcs, AliyunRDS
from cmdb.cloud.aliyun.libs import generate_aliyun_ecs, get_aliyun_resource
from cmdb.cloud.serializers import AliyunEcsUpdateSerializer
from cmdb.native.models import NativeHost
from public.util.libs import get_logger, utc2local, UTC_FORMAT_FULL
from public.util.call_ansible import call_console_ansible_shell

logger = get_logger('cmdb.cmdb_common.cron')


# 通过 aliyun key 更新rds
def aliyun_rds_update_cron():
    logger.info('[cron] aliyun_rds_update_cron started')
    try:
        for keys_obj in AliyunKeys.objects.all():
            rds_list = get_aliyun_resource(
                access_key=keys_obj.access_key,
                access_secret=keys_obj.access_secret,
                region_id=keys_obj.region_id,
                resource='rds',
                kwargs={
                    'region_id': keys_obj.region_id
                }
            )
            logger.debug(f"`aliyun_rds_api()`: {rds_list}")
            for rds in rds_list:
                try:
                    try:
                        rds_obj = AliyunRDS.objects.get(instance_id=rds['DBInstanceId'])
                    except Exception:
                        rds_obj = AliyunRDS()
                        rds_obj.ac_key_id = keys_obj.id
                        rds_obj.instance_id = rds['DBInstanceId']

                    rds_obj.instance_desc = rds['DBInstanceDescription']
                    rds_obj.status = rds['DBInstanceStatus']
                    # 2019-03-12T07:02:09Z
                    if rds.get('CreateTime') != '':
                        rds_obj.create_time = utc2local(datetime.datetime.strptime(rds.get('CreateTime'),
                                                                                   UTC_FORMAT_FULL))
                    if rds.get('ExpireTime') != '':
                        rds_obj.expire_time = utc2local(datetime.datetime.strptime(rds.get('ExpireTime'),
                                                                                   UTC_FORMAT_FULL))
                    rds_obj.save()
                except Exception as e:
                    logger.debug(rds)
                    logger.exception(e)
    except Exception as e:
        logger.error(f'`aliyun_rds_update_cron()` error')
        logger.exception(e)


# 通过aliyun key 更新阿里云信息
def aliyun_ecs_update_cron():
    logger.info('[cron] aliyun_ecs_update started')
    aliyun_key_obj_list = AliyunKeys.objects.all()
    for aliyun_key_obj in aliyun_key_obj_list:
        ecs_list = generate_aliyun_ecs(
            aliyun_key_obj.id,
            aliyun_key_obj.access_key,
            aliyun_key_obj.access_secret,
            aliyun_key_obj.region_id
        )
        for data in ecs_list:
            try:
                try:
                    ecs_obj = AliyunEcs.objects.get(instance_id=data['instance_id'])
                    update_serializer = AliyunEcsUpdateSerializer(ecs_obj, data=data)
                except Exception:
                    update_serializer = AliyunEcsUpdateSerializer(data=data)
                update_serializer.is_valid(raise_exception=True)
                update_serializer.save()
            except Exception as e:
                logger.error(f'''阿里云更新 {data['instance_id']} 失败''')
                logger.exception(e)


# 需要通过ansible 检测的列表
def ansible_host_update_status_cron():
    logger.info('[cron] ansible_host_update_status_cron started')
    cmdb_map = {
        'aliyun': AliyunEcs,
        'native': NativeHost
    }

    # 检测列表
    model_list = ('native',)
    for _model in model_list:
        cmdb = cmdb_map[_model]
        hosts_obj_list = cmdb.objects.filter(is_ansible=1)
        host_list = []
        for host_obj in hosts_obj_list:
            host_list.append([host_obj.ssh_ip, host_obj.ssh_port, 'root'])

        try:
            out = call_console_ansible_shell(host_list, 'w > /dev/null')
            result_set = json.loads(out)
            success_list = result_set['success'].keys()
            failed_list = result_set['failed'].keys()
            unreachable_list = result_set['unreachable'].keys()
            # 成功列表
            for ssh_ip in success_list:
                try:
                    model_obj = cmdb.objects.get(ssh_ip=ssh_ip)
                    model_obj.status = 'Running'
                    model_obj.save()
                except Exception as e:
                    logger.exception(e)
            # 失败列表
            for result_list in (failed_list, unreachable_list):
                for ssh_ip in result_list:
                    try:
                        model_obj = cmdb.objects.get(ssh_ip=ssh_ip)
                        model_obj.status = 'Stopped'
                        model_obj.save()
                    except Exception as e:
                        logger.exception(e)
        except Exception as e:
            logger.exception(e)
