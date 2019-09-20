"""
sql 语句
"""
# coding: utf-8


# 在 urlooker 创建一条app alive 记录
def create_urlooker_app_alive(url=None, ip=None, note=None, app_id=None,
                              environment=None, idc=None, is_monitor=0) -> str:
    sql = f'''INSERT INTO strategy (`url`, `timeout`, `creator`, `ip`, `expect_code`, `note`, `max_step`,
 `times`, `teams`, `ops_cp_app_id`, `environment`, `idc`) 
 VALUES ('{url}', '60000', 'ops-admin', '{ip}', '200', '{note}', {is_monitor},
  5, '1', {app_id}, '{environment}', '{idc}');'''
    return sql


# 在 urlooker 删除一条 app alive 记录
def delete_urlooker_app_alive(app_id=None):
    sql_0 = f'''delete from rel_sid_ip 
where sid in (select id from strategy where ops_cp_app_id = {app_id});'''
    sql_1 = f'''delete from strategy where ops_cp_app_id = {app_id};'''
    return sql_0, sql_1


# 在 urlooker 更新一条 app alive 记录
def update_urlooker_app_alive(app_id=None, environment=None, check_api=None, update_kwargs=None):
    """
    param update_kwargs: aa=11, bb=22
    """
    sql = f'''update strategy set {update_kwargs} where ops_cp_app_id = {app_id} and environment = '{environment}' and 
    url = '{check_api}'; '''
    return sql


# 查询 urlooker 的记录
def select_urlooker_app_alive(app_id=None, environment=None, check_api=None, select_args=None):
    """
    param select_args: 如 id, max_step
    """
    if check_api:
        sql = f'''select {select_args} from strategy where ops_cp_app_id = {app_id} and environment = '{environment}'
        and url = '{check_api}' ; '''
        return sql
    sql = f'''select {select_args} from strategy where ops_cp_app_id = {app_id} and environment = '{environment}'; '''
    return sql


# 查询 urlooker 的记录
def select_urlooker(app_id=None, select_args=None):
    """
    param select_args: 如 id, max_step
    """
    sql = f'''select {select_args} from strategy where ops_cp_app_id = {app_id}; '''
    return sql
