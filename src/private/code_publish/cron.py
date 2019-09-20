"""
cron
"""
import json
import datetime
from .models import CodePublishWebControl
from common.models import SettingConf
from code_publish.models import CodePublishLockEnv, CodePublishLockEnvApp


# 删除超出保留时间的数据
def delete_code_publish_record_cron():
    model_obj = SettingConf.objects.get(owner='global')
    delete_expire_days = json.loads(model_obj.code_publish_setting)['delete_expire_days']
    now_date = datetime.datetime.now()
    expired_date = now_date - datetime.timedelta(days=delete_expire_days)
    # 删除expired天前的数据
    CodePublishWebControl.objects.filter(updated__lt=expired_date).delete()


# 解锁超时的环境锁
def release_env_lock_cron():
    now_time = datetime.datetime.now()
    cple_model_obj_list = CodePublishLockEnv.objects.all()
    for model_obj in cple_model_obj_list:
        if now_time >= model_obj.expired:
            CodePublishLockEnvApp.objects.filter(lock_grp_id=model_obj.id).delete()
            model_obj.delete()
