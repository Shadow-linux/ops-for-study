"""
新增的监控项变量都需要定义在这里
"""
from monitor.models import (
    MonitorECS,
    MonitorVPN,
    MonitorDomain,
    MonitorNAS,
    MonitorRDS,
    MonitorYueXinSms,
    MonitorXunChengEryaosu,
    MonitorWanWeiYiYuanBankIdentity,
    MonitorTencentSms
)
from message.ops_monitor import third_party_doc


# 指定的监控项
MONITOR_ITEMS = ('ecs', 'rds', 'nas', 'domain', 'vpn',
                 'yuexin_sms', 'xuncheng_eryaosu', 'wanweiyiyuan_bankid', 'tencent_sms')
# 需要图表的监控项
MONITOR_GRAPH_ITEMS = ('yuexin_sms', 'xuncheng_eryaosu', 'wanweiyiyuan_bankid', 'tencent_sms')
# 使用DateAlgorithm
MONITOR_DATE_ALGORITHM = ('ecs', 'rds', 'nas', 'domain', 'vpn')
# 使用NumberAlgorithm
MONITOR_NUMBER_ALGORITHM = ('yuexin_sms', 'xuncheng_eryaosu', 'wanweiyiyuan_bankid', 'tencent_sms')
# 使用NumberJitterAlgorithm
MONITOR_NUMBER_JITTER_ALGORITHM = ('yuexin_sms', 'xuncheng_eryaosu', 'wanweiyiyuan_bankid', 'tencent_sms')

# 指定的表
MONITOR_MODALS = {
    'ecs': MonitorECS,
    'vpn': MonitorVPN,
    'domain': MonitorDomain,
    'nas': MonitorNAS,
    'rds': MonitorRDS,
    'yuexin_sms': MonitorYueXinSms,
    'xuncheng_eryaosu': MonitorXunChengEryaosu,
    'wanweiyiyuan_bankid': MonitorWanWeiYiYuanBankIdentity,
    'tencent_sms': MonitorTencentSms
}
# 告警通知文案
NOTICE_DOC_FUNC = {
    'ecs': third_party_doc.ecs,
    'rds': third_party_doc.rds,
    'nas': third_party_doc.nas,
    'domain': third_party_doc.domain,
    'vpn': third_party_doc.vpn,
    'yuexin_sms': third_party_doc.yuexin_sms,
    'xuncheng_eryaosu': third_party_doc.xuncheng_eryaosu,
    'wanweiyiyuan_bankid': third_party_doc.wanweiyiyuan_bankid,
    'tencent_sms': third_party_doc.tencent_sms,
    'jitter_yuexin_sms': third_party_doc.jitter_yuexin_sms,
    'jitter_xuncheng_eryaosu': third_party_doc.jitter_xuncheng_eryaosu,
    'jitter_wanweiyiyuan_bankid': third_party_doc.jitter_wanweiyiyuan_bankid,
    'jitter_tencent_sms': third_party_doc.jitter_tencent_sms,
}

# Falcon 内的组
THIRD_PARTY_HG = 'third.party.hg'
THIRD_PARTY_GRAPH_HG = 'third.party.graph.hg'
# Falcon endpoint prefix
THIRD_PARTY_PREFIX = 'third_party'
THIRD_PARTY_GRAPH_PREFIX = 'third_party_graph'
