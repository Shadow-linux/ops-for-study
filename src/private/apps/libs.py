# coding: utf-8
from cmdb.cloud.models import AliyunEcs
from cmdb.native.models import NativeHost
from .models import AppHostRel


# 获取与app有关联的host
def get_app_rel_host(app_id):
    # aliyun ecs
    aliyun_obj_list = AliyunEcs.objects.filter(id__in=[
        model_obj.host_id for model_obj in AppHostRel.objects.filter(app_id=app_id, owner='aliyun')
    ])
    # native host
    native_obj_list = NativeHost.objects.filter(id__in=[
        model_obj.host_id for model_obj in AppHostRel.objects.filter(app_id=app_id, owner='native')
    ])

    return {
        'aliyun': aliyun_obj_list,
        'native': native_obj_list
    }


# 获取与app 按环境查找 关联host
def get_app_rel_host_with_env(app_id, env) -> list:
    ret_list = []
    # 提升append 速度, 参考cookbook 加速程序运行
    # 每一次使用点(.)操作符来访问属性的时候会带来额外的开销。
    # 它会触发特定的方法，比如 __getattribute__() 和 __getattr__() ，这些方法会进行字典操作操作
    ret_list_append = ret_list.append
    # aliyun
    aliyun_obj_list = AliyunEcs.objects.filter(id__in=[
        model_obj.host_id for model_obj in AppHostRel.objects.filter(app_id=app_id, owner='aliyun')
    ], environment=env)
    # native host
    native_obj_list = NativeHost.objects.filter(id__in=[
        model_obj.host_id for model_obj in AppHostRel.objects.filter(app_id=app_id, owner='native')
    ], environment=env)

    # 整合列表
    handle_hosts =(aliyun_obj_list, native_obj_list)
    for host_obj_list in handle_hosts:
        for host_obj in host_obj_list:
            ret_list_append(host_obj)

    return ret_list
