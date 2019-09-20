"""
第三方监控告警文案
"""


def __base(monitor_item, op, compare_num, alert_num, note, work_order):
    return f"""
    <p><b>监控项：</b>{monitor_item}</p>
    <p><b>注解(Note): </b>{note}</p>
    <p><b>策略: </b>{compare_num} {op} {alert_num}</p>
    <p><b>OpsId: </b>{work_order}</p>
    <p><b>详细信息:</b></p>
    """

def __jitter_base(monitor_item, op, compare_num, alert_num, note, work_order, hours_ago):
    return f"""
    <p><b>监控项：</b>{monitor_item}</p>
    <p><b>注解(Note): </b>{note}</p>
    <p><b>策略: </b>{compare_num} {op} {alert_num}</p>
    <p><b>OpsId: </b>{work_order}</p>
    <p><b>时间范围: </b>前 {hours_ago} 小时</p>
    <p><b>详细信息:</b></p>
    """


def ecs(monitor_item, op, compare_num, alert_num, note, work_order, model_obj):
    base_doc = __base(monitor_item, op, compare_num, alert_num, note, work_order)
    doc = f"""
    <p>[主机名]: {model_obj.hostname}</p>
    <p>[ServerId]: {model_obj.server_id}</p>
    <p>[过期时间]: {model_obj.expire_time}</p>
    """
    return base_doc + doc


def rds(monitor_item, op, compare_num, alert_num, note, work_order, model_obj):
    base_doc = __base(monitor_item, op, compare_num, alert_num, note, work_order)
    doc = f"""
    <p>[描述]: {model_obj.instance_desc}</p>
    <p>[ServerId]: {model_obj.instance_id}</p>
    <p>[过期时间]: {model_obj.expire_time}</p>
    """
    return base_doc + doc


def nas(monitor_item, op, compare_num, alert_num, note, work_order, model_obj):
    base_doc = __base(monitor_item, op, compare_num, alert_num, note, work_order)
    doc = f"""
    <p>[描述]: {model_obj.desc}</p>
    <p>[ServerId]: {model_obj.system_id}</p>
    <p>[PkgId]: {model_obj.package_id}</p>
    <p>[过期时间]: {model_obj.expire_time}</p>
    """
    return base_doc + doc


def domain(monitor_item, op, compare_num, alert_num, note, work_order, model_obj):
    base_doc = __base(monitor_item, op, compare_num, alert_num, note, work_order)
    doc = f"""
    <p>[Domain]: {model_obj.domain}</p>
    <p>[过期时间]: {model_obj.expire_time}</p>
    """
    return base_doc + doc


def vpn(monitor_item, op, compare_num, alert_num, note, work_order, model_obj):
    base_doc = __base(monitor_item, op, compare_num, alert_num, note, work_order)
    doc = f"""
    <p>[描述]: {model_obj.desc}</p>
    <p>[VpcId]: {model_obj.vpc_id}</p>
    <p>[VPnId]: {model_obj.vpn_id}</p>
    <p>[过期时间]: {model_obj.expire_time}</p>
    """
    return base_doc + doc


# 阅信短信
def yuexin_sms(monitor_item, op, compare_num, alert_num, note, work_order, model_obj):
    base_doc = __base(monitor_item, op, compare_num, alert_num, note, work_order)
    doc = f"""
    <p>[username]: {model_obj.username}</p>
    <p>[balance]: {model_obj.balance}</p>
    """
    return base_doc + doc


def jitter_yuexin_sms(monitor_item, op, jitter_num, alert_num, note, work_order, hours_ago, model_obj):
    base_doc = __jitter_base(monitor_item, op, jitter_num, alert_num, note, work_order, hours_ago)
    doc = f"""
    <p>[username]: {model_obj.username}</p>
    <p>[balance]: {model_obj.balance}</p>
    """
    return base_doc + doc


# 寻程 二要素
def xuncheng_eryaosu(monitor_item, op, compare_num, alert_num, note, work_order, model_obj):
    base_doc = __base(monitor_item, op, compare_num, alert_num, note, work_order)
    doc = f"""
    <p>[name_desc]: {model_obj.name_desc}</p>
    <p>[balance]: {model_obj.number}</p>
    """
    return base_doc + doc


def jitter_xuncheng_eryaosu(monitor_item, op, jitter_num, alert_num, note, work_order, hours_ago, model_obj):
    base_doc = __jitter_base(monitor_item, op, jitter_num, alert_num, note, work_order, hours_ago)
    doc = f"""
    <p>[name_desc]: {model_obj.name_desc}</p>
    <p>[balance]: {model_obj.number}</p>
    """
    return base_doc + doc


# 万维易源 银行身份证验证
def wanweiyiyuan_bankid(monitor_item, op, compare_num, alert_num, note, work_order, model_obj):
    base_doc = __base(monitor_item, op, compare_num, alert_num, note, work_order)
    doc = f"""
    <p>[api_name]: {model_obj.api_name}</p>
    <p>[balance]: {model_obj.compare_num}</p>
    """
    return base_doc + doc


def jitter_wanweiyiyuan_bankid(monitor_item, op, jitter_num, alert_num, note, work_order, hours_ago, model_obj):
    base_doc = __jitter_base(monitor_item, op, jitter_num, alert_num, note, work_order, hours_ago)
    doc = f"""
    <p>[api_name]: {model_obj.api_name}</p>
    <p>[balance]: {model_obj.compare_num}</p>
    """
    return base_doc + doc


def tencent_sms(monitor_item, op, compare_num, alert_num, note, work_order, model_obj):
    base_doc = __base(monitor_item, op, compare_num, alert_num, note, work_order)
    doc = f"""
    <p>[package_id]: {model_obj.package_id}</p>
    <p>[balance]: {model_obj.compare_num}</p>
    """
    return base_doc + doc


def jitter_tencent_sms(monitor_item, op, jitter_number, alert_num, note, work_order, hours_ago, model_obj):
    base_doc = __jitter_base(monitor_item, op, jitter_number, alert_num, note, work_order, hours_ago)
    doc = f"""
    <p>[package_id]: {model_obj.package_id}</p>
    <p>[balance]: {model_obj.compare_num}</p>
    """
    return base_doc + doc


def expire(monitor_item, op, compare_num, alert_num, note, work_order, model_obj):
    base_doc = __base(monitor_item, op, compare_num, alert_num, note, work_order)
    doc = f"""
    <p>[描述]: 数据失效, 监控数据未上传。</p>
    """
    return base_doc + doc
