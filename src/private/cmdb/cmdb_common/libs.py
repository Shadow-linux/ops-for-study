import json
from public.util.call_ansible import call_console_ansible_setup
from .serializers import AnisbleUpdateAliyunEcsSerializer, AnsibleUpdateNativeHostSerializer
from .models import TagsAliyunEcsRel, TagsNativeHostRel
from .models import Tags

CMDB_MAPS = {
    'aliyun': TagsAliyunEcsRel,
    'native': TagsNativeHostRel,
}


# 获取 host 对应的 tag
def get_host_tags(host_id, cmdb):
    tag_rel_modal = CMDB_MAPS[cmdb]
    tag_rel_modal_obj_list = tag_rel_modal.objects.filter(target_id=host_id)
    tags_obj_list = Tags.objects.filter(id__in=[ tr_modal_obj.tag_id for tr_modal_obj in  tag_rel_modal_obj_list])
    return [
        {
            'key': tag_obj.tag_key,
            'value': tag_obj.tag_value
        }
        for tag_obj in tags_obj_list
    ]


""" ansible 数据格式
['success']['192.168.1.158'][1]['ansible_facts']
['ansible_processor_vcpus']
['ansible_memory_mb']['real']['total']
['ansible_devices']['disk']['partitions']
['ansible_product_serial']
['ansible_fqdn']
['ansible_swaptotal_mb']
['ansible_lsb']['id'] + ['ansible_lsb']['release']
['ansible_system']
"""

# 基础函数，公共调用
def __base_ansible_update_host(host_list):
    setup_info = call_console_ansible_setup(host_list)
    setup_dict = json.loads(setup_info)
    assert not setup_dict.get('failed'), f'{host_list} ansible setup failed'
    assert not setup_dict.get('unreachable'), f'{host_list} ansible setup unreachable'
    setup_host_info = setup_dict['success']
    return setup_host_info


# aliyun ecs
def ansible_update_aliyun_ecs(host_list, model_obj):
    # 是用ansible setup 模块
    setup_host_info = __base_ansible_update_host(host_list)
    for host, info in setup_host_info.items():
        ansible_facts = info[0]['ansible_facts']
        data = {'hostname': ansible_facts['ansible_fqdn']}
        serializer = AnisbleUpdateAliyunEcsSerializer(model_obj, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()


# native host
def ansible_update_native_host(host_list, model_obj):
    setup_host_info = __base_ansible_update_host(host_list)

    # 提取disk 信息
    def __handle_disk(_ansible_facts: dict) -> dict:
        ret_dict = {}
        for dev, _info in _ansible_facts['ansible_devices'].items():
            if _info['partitions']:
                # GB 前的空号不要删除是故意写的，格式就是这样
                ret_dict[f'/dev/{dev}'] = _info['size'].replace(' GB', '')
        return ret_dict

    for host, info in setup_host_info.items():
        ansible_facts = info[0]['ansible_facts']
        data = {
            'hostname': ansible_facts['ansible_fqdn'],
            'memory': ansible_facts['ansible_memory_mb']['real']['total'],
            'disk': json.dumps(__handle_disk(ansible_facts)),
            'cpu': ansible_facts['ansible_processor_vcpus'],
            'serial_number': ansible_facts['ansible_product_serial'],
            'swap': ansible_facts['ansible_swaptotal_mb'],
            'os_name': f''' {ansible_facts['ansible_distribution']} {ansible_facts['ansible_distribution_version']}''',
            'os_type': ansible_facts['ansible_system'].lower(),
        }
        serializer = AnsibleUpdateNativeHostSerializer(model_obj, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
