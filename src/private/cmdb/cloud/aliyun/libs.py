"""
aliyun 相关方法
"""
import json
from .api import get_aliyun_resource
from types import GeneratorType


# 解析磁盘信息
def __parse_aliyun_disk(disk_list: list) -> dict:
    ret_dict = {}
    for disk in disk_list:
        if disk['Status'] == 'In_use':
            ret_dict[disk['Device']] = disk['Size']
    return ret_dict


# 获取磁盘ID
def __get_aliyun_disk_id(disk_list: list) -> dict:
    ret_dict = {}
    for disk in disk_list:
        if disk['Status'] == 'In_use':
            ret_dict[disk['Device']] = disk['DiskId']
    return ret_dict


# 解析阿里云ecs信息
def generate_aliyun_ecs(ac_key_id: int, access_key: str, access_secret: str, region_id: str) -> list:
    ecs_list = get_aliyun_resource(access_key, access_secret, region_id)
    ret_list = []
    for ecs in ecs_list:
        private_ip = ecs['InnerIpAddress']['IpAddress'] + ecs['VpcAttributes']['PrivateIpAddress']['IpAddress']
        item = {
            'ac_key_id': ac_key_id,
            'hostname': ecs['HostName'],
            'serial_number': ecs['SerialNumber'],
            'zone_id': ecs['ZoneId'],
            'region_id': ecs['RegionId'],
            'cpu': ecs['Cpu'],
            'memory': ecs['Memory'],
            'os_type': ecs['OSType'],
            'os_name': ecs['OSName'],
            'expired_time': ecs['ExpiredTime'],
            'instance_type': ecs['InstanceType'],
            'instance_name': ecs['InstanceName'],
            'instance_id': ecs['InstanceId'],
            'created': ecs['CreationTime'],
            'status': ecs['Status'],
            'instance_charge_type': ecs['InstanceChargeType'],
            'public_ip': json.dumps(ecs['PublicIpAddress']['IpAddress']),
            'private_ip': json.dumps(private_ip),
            'ssh_ip': private_ip[0]
        }
        disk_list = get_aliyun_resource(
            access_key,
            access_secret,
            region_id,
            resource='disk',
            kwargs={
            'region_id': item['region_id'],
            'instance_id': item['instance_id'],
        })
        item['disk'] = json.dumps(__parse_aliyun_disk(disk_list))
        item['disk_id'] = json.dumps(__get_aliyun_disk_id(disk_list))
        ret_list.append(item)
    return ret_list