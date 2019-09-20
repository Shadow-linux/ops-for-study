"""
libs
"""
import json
from .models import (CodePublishLockEnvApp, CodePublishLockEnv)


def get_lock_info_collections(user_id, creator=False):
    """
    :param user_id: 用户id
    :param creator: 默认是False，用于区分是否是建立者来请求
    :return: 用户所在组列表， 所在组锁定的app， 所在组未锁定的app
    """
    # user所在的组
    if creator:
        lock_grp_id = [
            cple_obj.id
            for cple_obj in CodePublishLockEnv.objects.all() if user_id == cple_obj.creator
        ]
    else:
        lock_grp_id = [
            cple_obj.id
            for cple_obj in CodePublishLockEnv.objects.all() if user_id == cple_obj.creator or
                                                                user_id in json.loads(cple_obj.user_ids)
        ]
    # print(lock_grp_id)
    # 属于这些组的  app
    owner_cplea_id_list = [obj.app_name_id for obj in
                           CodePublishLockEnvApp.objects.filter(lock_grp_id__in=lock_grp_id)]
    # print(owner_cplea_id_list)
    # 被其他组锁定的 app
    lock_cplea_id_list = [
        obj.app_name_id for obj in
        CodePublishLockEnvApp.objects.exclude(lock_grp_id__in=lock_grp_id)
    ]
    # print(lock_cplea_id_list)
    return lock_grp_id, owner_cplea_id_list, lock_cplea_id_list
