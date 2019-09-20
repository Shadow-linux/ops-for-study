"""
第三方监控获取数据API
"""
import json
import datetime
import time
import hashlib
import requests
from django.conf import settings
from cmdb.cloud.aliyun.api import get_aliyun_resource
from cmdb.cloud.models import AliyunKeys, AliyunEcs
from .external_libs.ShowapiRequest import ShowapiRequest


# 获取阿里云所有的key
def __get_all_aliyun_keys():
    return AliyunKeys.objects.all()


def aliyun_ecs_api():
    return AliyunEcs.objects.filter(is_active=1)


def aliyun_rds_api():
    all_keys_obj_list = __get_all_aliyun_keys()
    ret_list = []
    for keys_obj in all_keys_obj_list:
        data_list = get_aliyun_resource(
            access_key=keys_obj.access_key,
            access_secret=keys_obj.access_secret,
            region_id=keys_obj.region_id,
            resource='rds',
            kwargs={
                'region_id': keys_obj.region_id
            }
        )
        ret_list.extend(data_list)
    return ret_list


def aliyun_nas_api():
    all_keys_obj_list = __get_all_aliyun_keys()
    ret_nas_list = []
    ret_nas_pkg_list = []
    for keys_obj in all_keys_obj_list:
        nas_list = get_aliyun_resource(
            access_key=keys_obj.access_key,
            access_secret=keys_obj.access_secret,
            region_id=keys_obj.region_id,
            resource='nas',
            kwargs={
                'region_id': keys_obj.region_id
            }
        )
        nas_package_list = get_aliyun_resource(
            access_key=keys_obj.access_key,
            access_secret=keys_obj.access_secret,
            region_id=keys_obj.region_id,
            resource='nas_package',
            kwargs={
                'region_id': keys_obj.region_id
            }
        )
        ret_nas_list.extend(nas_list)
        ret_nas_pkg_list.extend(nas_package_list)
    return ret_nas_list, ret_nas_pkg_list


def aliyun_vpn_api():
    all_keys_obj_list = __get_all_aliyun_keys()
    ret_list = []
    for keys_obj in all_keys_obj_list:
        vpn_list = get_aliyun_resource(
            access_key=keys_obj.access_key,
            access_secret=keys_obj.access_secret,
            region_id=keys_obj.region_id,
            resource='vpn',
            kwargs={
                'region_id': keys_obj.region_id
            }
        )
        ret_list.extend(vpn_list)

    return ret_list


def aliyun_domain_api():
    all_keys_obj_list = __get_all_aliyun_keys()
    ret_list = []
    for keys_obj in all_keys_obj_list:
        data_list = get_aliyun_resource(
            access_key=keys_obj.access_key,
            access_secret=keys_obj.access_secret,
            region_id=keys_obj.region_id,
            resource='domain',
            kwargs={
                'region_id': keys_obj.region_id
            }
        )
        ret_list.extend(data_list)

    return ret_list


def yuexin_sms_api() -> list:
    now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    ret_list = []
    for username, pwd in settings.DEPLOY_CONF['yueXin_sms_info'].items():
        # 处理pwd,这是阅信规则，加密密码
        pwd_date = f'{pwd}{now}'
        h5_pwd = hashlib.md5()
        h5_pwd.update(pwd_date.encode())
        res = requests.get(settings.DEPLOY_CONF.get('yueXin_sms_url', 'url'), params={
            'name': username,
            'pwd': h5_pwd.hexdigest(),
            'mttime': now
        })
        res_data = res.json()
        res_data['username'] = username
        ret_list.append(res_data)
    return ret_list


# 寻程二要素认证
def xuncheng_eryaosu_api():
    """
    {
        "error_code": 0,
        "reason": "查询成功",
        "result": [
            {
                "name": "身份证实名认证",
                "number": 43042
            }
        ]
    }
    :return:
    """
    data_list = []
    access_key = settings.DEPLOY_CONF.get('xunCheng_ak', 'access_key')
    url = settings.DEPLOY_CONF.get('xunCheng_url', 'url')
    for _, key in settings.DEPLOY_CONF['xunCheng_keys'].items():
        data_dict = {
            "ak": access_key,
            "key": key,
        }
        res = requests.get(url, params=data_dict)
        data = res.json()
        data['key'] = key
        data_list.append(data)
    return data_list


# 万维易源 银行卡身份证实名认证
def wanweiyiyuan_bank_identity_api():
    # 文档 https://www.showapi.com/api/view/631/3
    r = ShowapiRequest(f"{settings.DEPLOY_CONF.get('wanWeiYiYuan_url', 'url')}",
                       f"{settings.DEPLOY_CONF.get('wanWeiYiYuan_bankIdentity_info', 'app_id')}",
                       f"{settings.DEPLOY_CONF.get('wanWeiYiYuan_bankIdentity_info', 'app_secrete')}")
    # https://www.showapi.com/api/view/1072   1072 就是银行卡身份证实名认证 的api_code
    r.addBodyPara("api_code", f"{settings.DEPLOY_CONF.get('wanWeiYiYuan_bankIdentity_info', 'api_code')}")
    res = r.get()
    data_dict = res.json()
    if data_dict['showapi_res_code'] != 0 or data_dict['showapi_res_body']['ret_code'] != 0:
        raise Exception(res.text)
    return data_dict['showapi_res_body'].get('list', [])


# 腾讯市场 爱员工短信中心(应用)
def tencent_sms_api():
    timestamp = int(time.mktime(datetime.datetime.now().timetuple()))
    app_id = settings.DEPLOY_CONF.get('tencent_sms_info', 'app_id')
    app_key = settings.DEPLOY_CONF.get('tencent_sms_info', 'app_key')
    const_random = settings.DEPLOY_CONF.get('tencent_sms_info', 'random')
    url = f"{settings.DEPLOY_CONF.get('tencent_url', 'url')}?sdkappid={app_id}&random={const_random}"
    encrypt_content = f"appkey={app_key}&random={const_random}&time={timestamp}".encode()
    sig_obj = hashlib.sha256(encrypt_content)
    sig = sig_obj.hexdigest()
    post_data = {
        "offset": 0,
        "length": 100,
        "sig": "{}".format(sig),
        "time": timestamp
    }
    res = requests.post(url, data=json.dumps(post_data))
    data_list = res.json().get('data', [])
    package_id_list = settings.DEPLOY_CONF.get('tencent_sms_info', 'package_ids').split(',')
    res_list = []
    for pkg_id in package_id_list:
        for data in data_list:
            if int(data['package_id']) == int(pkg_id):
                res_list.append(data)
    return res_list
