"""
nginx access alarm strategy doc
"""


def _average(alarm_name, latest_time, where_condition, cost, match_count, op, alarm_strategy, result_set):
    doc = f'''
    <p><b>监控名:</b> {alarm_name} </p> 
    <p><b>时间范围:</b> 最近 {latest_time} 分钟</p> 
    <p><b>监控接口:</b> {where_condition}</p>
    <p><b>策略:</b> 平均花费 {result_set['average'] / 1000}秒 {op} {cost / 1000}秒 </p>
    <p><b>匹配数量:</b> {match_count}</p>
    <p><b>RequestId(取样):</b> {result_set.get('request_id', [])}</p>
    <p style="color: #909399; font-size: 12px">PS: 请登录 https://log.aiyuangong.com/ 查询详情</p>
    '''
    return doc


def _max(alarm_name, latest_time, where_condition, cost, match_count, op, alarm_strategy, result_set):
    doc = f'''
    <p><b>监控名:</b> {alarm_name} </p> 
    <p><b>时间范围:</b> 最近 {latest_time} 分钟</p> 
    <p><b>监控接口:</b> {where_condition}</p>
    <p><b>策略:</b> 最大花费 {result_set.get('max', 0) / 1000}秒 {op} {cost / 1000}秒 </p>
    <p><b>匹配数量:</b> {match_count}</p>
    <p><b>RequestId(取样):</b> {result_set.get('request_id', [])}</p>
    <p style="color: #909399">PS: 请登录 https://log.aiyuangong.com/ 查询详情</p>
    '''
    return doc


def cost_percent(alarm_name, latest_time, where_condition, cost, match_count, op, alarm_strategy, result_set):
    doc = f'''
    <p><b>监控名:</b> {alarm_name} </p> 
    <p><b>时间范围:</b> 最近 {latest_time} 分钟</p> 
    <p><b>监控接口:</b> {where_condition}</p>
    <p><b>策略:</b> {op} 请求时间 {cost / 1000}秒 的请求数量占比
    {round(result_set.get('real_percent', 0), 2) * 100}%  {op} {alarm_strategy['percent'] * 100}% </p>
    <p><b>匹配数量:</b> {match_count}</p>
    <p><b>RequestId(取样):</b> {result_set.get('request_id', [])}</p>
    <p style="color: #909399">PS: 请登录 https://log.aiyuangong.com/ 查询详情</p>
    '''
    return doc
