import json
import os
from django.conf import settings
from public.util.libs import template_render2file


# render ssh config 用于跳到跳板机后执行命令，ansible 需要该方法
def render_ssh_config(host_obj_list):
    context = {'host_obj_list': [
        {
            'host': json.loads(host_obj.private_ip)[0],
            'port': host_obj.ssh_port,
            'ssh_proxy': settings.DEPLOY_CONF.get('ssh_proxy', 'ssh_ip')
        }
        for host_obj in host_obj_list
    ]}
    base_dir = settings.BASE_DIR
    src_file = os.path.join(base_dir, 'private/cmdb/cmdb_common/template/config.templet')
    det_file = settings.DEPLOY_CONF.get('ssh_proxy', 'ssh_config')
    template_render2file(context, src_file, det_file)
