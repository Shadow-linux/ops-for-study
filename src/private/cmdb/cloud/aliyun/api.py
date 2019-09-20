"""
获取阿里云数据方法
"""
import json
import datetime
import asyncio
from types import FunctionType
from django.conf import settings
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from util.libs import LOCAL_FORMAT, get_logger


logger = get_logger('aliyun.api')


# 获取ECS 列表
def __get_ecs(client: AcsClient, kwargs) -> list:
    instances_request = CommonRequest(domain=settings.DEPLOY_CONF.get('aliyun_api_address', 'ecs'),
                                      version='2014-05-26',
                                      action_name='DescribeInstances')
    instances_request.add_query_param('PageSize', 100)
    return_instances = []
    response = client.do_action_with_exception(instances_request)
    res_instance_list = json.loads(response.decode())['Instances']['Instance']
    return_instances.extend(res_instance_list)
    page_number = 1
    while True:
        page_number += 1
        instances_request.add_query_param('PageNumber', page_number)
        response = client.do_action_with_exception(instances_request)
        res_instance_list = json.loads(response.decode())['Instances']['Instance']
        if not res_instance_list:
            break
        return_instances.extend(res_instance_list)

    return return_instances


# 获取Disk 信息
def __get_disk(client: AcsClient, kwargs) -> list:
    disk_request = CommonRequest(domain=settings.DEPLOY_CONF.get('aliyun_api_address', 'ecs'),
                                 version='2014-05-26',
                                 action_name='DescribeDisks')
    disk_request.add_query_param('RegionId', kwargs['region_id'])
    disk_request.add_query_param('InstanceId', kwargs['instance_id'])
    response = client.do_action_with_exception(disk_request)
    res_dict = json.loads(response.decode())
    return res_dict['Disks']['Disk']


# 获取RDS 信息
def __get_rds(client: AcsClient, kwargs) -> list:
    instances_request = CommonRequest(domain=settings.DEPLOY_CONF.get('aliyun_api_address', 'rds'),
                                      version='2014-08-15',
                                      action_name='DescribeDBInstances')
    instances_request.add_query_param('RegionId', kwargs['region_id'])
    instances_request.add_query_param('PageSize', 100)
    response = client.do_action_with_exception(instances_request)
    res_dict = json.loads(response.decode())
    return res_dict['Items']['DBInstance']


# 获取nas 信息
def __get_nas(client: AcsClient, kwargs) -> list:
    instances_request = CommonRequest(domain=settings.DEPLOY_CONF.get('aliyun_api_address', 'nas'),
                                      version='2017-06-26',
                                      action_name='DescribeFileSystems')
    instances_request.add_query_param('RegionId', kwargs['region_id'])
    instances_request.add_query_param('PageSize', 100)
    response = client.do_action_with_exception(instances_request)
    res_dict = json.loads(response.decode())
    return res_dict['FileSystems']['FileSystem']


# 获取nas package 信息
def __get_nas_package(client: AcsClient, kwargs) -> list:
    instances_request = CommonRequest(domain=settings.DEPLOY_CONF.get('aliyun_api_address', 'nas'),
                                      version='2016-02-29',
                                      action_name='DescribeVolumeStoragePackages')
    instances_request.add_query_param('RegionId', kwargs['region_id'])
    instances_request.add_query_param('PageSize', 100)
    response = client.do_action_with_exception(instances_request)
    res_dict = json.loads(response.decode())
    return res_dict['Packages']


# 获取vpc 信息
def __get_vpn(client: AcsClient, kwargs) -> list:
    instances_request = CommonRequest(domain=settings.DEPLOY_CONF.get('aliyun_api_address', 'vpc'),
                                      version='2016-04-28',
                                      action_name='DescribeVpnGateways')
    instances_request.add_query_param('RegionId', kwargs['region_id'])
    response = client.do_action_with_exception(instances_request)
    res_dict = json.loads(response.decode())
    return res_dict['VpnGateways']['VpnGateway']


# 获取domain 信息
def __get_domain(client: AcsClient, kwargs) -> list:
    instances_request = CommonRequest(domain=settings.DEPLOY_CONF.get('aliyun_api_address', 'domain'),
                                      version='2018-01-29',
                                      action_name='QueryDomainList')
    instances_request.add_query_param('RegionId', kwargs['region_id'])
    instances_request.add_query_param('PageSize', 100)
    instances_request.add_query_param('PageNum', 1)
    response = client.do_action_with_exception(instances_request)
    res_dict = json.loads(response.decode())
    return res_dict['Data']['Domain']


# 由于阿里云图表数据限制请求数，所以使用时间切割出多次请求的时间
class GraphTimeSplit(object):

    @staticmethod
    def __base_time_handler(start_time, end_time, count, split_num, time_attr='hours'):
        time_attr_maps = {
            'hours': datetime.timedelta(hours=split_num),
            'days': datetime.timedelta(days=split_num)
        }
        time_list = []
        start = start_time
        for _ in range(0, count):
            end = start + time_attr_maps[time_attr]
            time_list.append([start, end])
            start = end
        return time_list

    @staticmethod
    def day_0(start_time, end_time):
        return GraphTimeSplit.__base_time_handler(start_time, end_time, 1, 1)

    @staticmethod
    def day_1(start_time, end_time):
        return GraphTimeSplit.__base_time_handler(start_time, end_time, 2, 12)

    @staticmethod
    def day_3(start_time, end_time):
        return GraphTimeSplit.__base_time_handler(start_time, end_time, 6, 12)

    @staticmethod
    def day_7(start_time, end_time):
        return GraphTimeSplit.__base_time_handler(start_time, end_time, 5, 36)

    @staticmethod
    def day_30(start_time, end_time):
        return GraphTimeSplit.__base_time_handler(start_time, end_time, 3, 10, time_attr='days')


# 获取ecs监控图表信息
def __get_graph(client: AcsClient, kwargs) -> list:
    # 这里是使用了协程的玩意来提取数据，不用线程的原因是使用线程可能会更慢（全局锁你懂得）
    #
    # 1 天 period: 60
    # 3 天 period: 60
    # 7 天 period: 300
    # 30 天 period: 900
    def __period_base(period, s_time, e_time):
        try:
            request.add_query_param('Period', period)
            request.add_query_param('StartTime', s_time)
            request.add_query_param('EndTime', e_time)
            response = client.do_action_with_exception(request)
            data_list = json.loads(json.loads(response.decode())['Datapoints'])
            graph_list.extend(data_list)
        except Exception as e:
            logger.error('__period_base has error.')
            logger.exception(e)

    async def __period_0(s_time, e_time):
        return __period_base(60, s_time, e_time)

    async def __period_60(s_time, e_time):
        return __period_base(60, s_time, e_time)

    async def __period_300(s_time, e_time):
        return __period_base(300, s_time, e_time)

    async def __period_900(s_time, e_time):
        return __period_base(900, s_time, e_time)

    period_maps = {
        0: __period_0,
        1: __period_60,
        3: __period_60,
        7: __period_300,
        30: __period_900,
    }
    """接收数据格式
    {
        "metric": "cpu_idle",
        "region_id": "cn-shenzhen",
        "days": 7,
        "dimensions": "[{"instanceId": "i-wz9exmnpyufi62y6dnbc"}]"
    }
    """
    metric_name = kwargs['metric']
    dimensions = kwargs['dimensions']
    region_id = kwargs['region_id']
    days = kwargs['days']
    namespace = kwargs['namespace']
    end_time = datetime.datetime.now()
    # 0 值为1个小时的数据
    if days == 0:
        start_time = end_time + datetime.timedelta(hours=-1)
    else:
        start_time = end_time + datetime.timedelta(days=-days)
    tmp_address = domain = settings.DEPLOY_CONF.get('aliyun_api_address', 'monitor').split('.')
    tmp_address.insert(1, region_id)
    # 最后的地址如: 	metrics.cn-shenzhen.aliyuncs.com
    request_address = ".".join(tmp_address)
    request = CommonRequest(domain=request_address,
                            version='2019-01-01',
                            action_name='DescribeMetricList')
    request.add_query_param('Namespace', namespace)
    request.add_query_param('Dimensions', dimensions)
    # 来自阿里云 https://help.aliyun.com/document_detail/28619.html?spm=a2c4g.11186623.2.12.5e65659d39LRGT
    metric_numerate = [
        'cpu_total',  # Host.cpu.total，当前消耗的总CPU百分比
        'cpu_idle',  # Host.cpu.idle，当前空闲CPU百分比
        'memory_usedutilization',  # Host.mem.usedutilization，内存使用率
        'load_1m',  # Host.load1，过去1分钟的系统平均负载，Windows操作系统没有此指标
        'load_5m',  # Host.load5， 过去5分钟的系统平均负载，Windows操作系统没有此指标
        'load_15m',  # Host.load15，过去15分钟的系统平均负载，Windows操作系统没有此指标
        'DiskReadBPS',  # 系统磁盘总读BPS
        'DiskWriteBPS',  # 系统磁盘总写BPS
        'DiskReadIOPS',  # 系统磁盘读IOPS
        'DiskWriteIOPS',  # 系统磁盘写IOPS
        'diskusage_utilization',  # Host.disk.utilization，磁盘使用率
        'disk_readbytes',  # Host.disk.readbytes，磁盘每秒读取的字节数
        'disk_writebytes',  # Host.disk.writebytes，磁盘每秒写入的字节数
        'disk_readiops',  # Host.disk.readiops，磁盘每秒的读请求数量
        'disk_writeiops',  # Host.disk.writeiops，磁盘每秒的写请求数量
        'InternetInRate',  # 公网流入带宽
        'InternetOutRate',  # 公网流出带宽
        'IntranetInRate',  # 私网流入带宽
        'IntranetOutRate',  # 私网流出带宽
    ]
    if metric_name not in metric_numerate:
        raise Exception(f'{metric_name} 不在 metric_numerate 里面，请核对。')
    request.add_query_param('MetricName', metric_name)
    time_list = eval(f"GraphTimeSplit.day_{days}")(start_time, end_time)
    graph_list = []
    tasks = []
    for i_time in time_list:
        logger.debug(f'''图表时间范围 {i_time[0].strftime(LOCAL_FORMAT)} - {i_time[1].strftime(LOCAL_FORMAT)}''')
        tasks.append(period_maps[days](
            i_time[0].strftime(LOCAL_FORMAT),
            i_time[1].strftime(LOCAL_FORMAT),
        ))
    # print(tasks)
    # 所以如果你asyncio.get_event_loop在主线程中调用一次，
    # 它将自动创建一个循环对象并将其设置为默认值，
    # 但是如果你在一个子线程中再次调用它，你会得到这个错误AssertionError: There is no current event loop in thread ‘Thread-1’.
    # 所以您需要在线程启动时显式创建/设置事件循环
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    return graph_list


# 获取ecs监控图表信息
def __get_ecs_graph(client: AcsClient, kwargs) -> list:
    # 这是aliyun  云监控 规定的namespace
    kwargs['namespace'] = 'acs_ecs_dashboard'
    return __get_graph(client, kwargs)


# 获取aliyun slb 信息
def __get_slb(client: AcsClient, kwargs) -> list:
    instances_request = CommonRequest(domain=settings.DEPLOY_CONF.get('aliyun_api_address', 'slb'),
                                      version='2014-05-15',
                                      action_name='DescribeLoadBalancers')
    instances_request.set_accept_format('json')
    instances_request.add_query_param('PageSize', 100)
    response = client.do_action_with_exception(instances_request)
    res_instance_list = json.loads(response.decode())
    return res_instance_list.get('LoadBalancers', {}).get('LoadBalancer', [])


def __get_adjust_slb(client: AcsClient, kwargs):
    app_name = kwargs.get('app_name')
    server_id = kwargs.get('server_id')
    weight = kwargs.get('weight')
    lb_id = None
    res_data_dict = None
    slb_list = __get_slb(client, kwargs)
    for slb in slb_list:
        if slb['LoadBalancerName'] == app_name:
            lb_id = slb['LoadBalancerId']  
    
    if lb_id:
        instances_request = CommonRequest(domain=settings.DEPLOY_CONF.get('aliyun_api_address', 'slb'),
                                          version='2014-05-15',
                                          action_name='SetBackendServers')
        instances_request.add_query_param('LoadBalancerId', f'{lb_id}')
        instances_request.add_query_param('BackendServers', f'[{{"ServerId":"{server_id}","Weight":"{weight}"}}]')
        response = client.do_action_with_exception(instances_request)
        res_data_dict = json.loads(response.decode())
    return res_data_dict


def __get_rds_graph(client: AcsClient, kwargs):
    metric_numerate = [
        'MySQL_NetworkTraffic',  # MySQL实例平均每秒钟的输入流量，MySQL实例平均每秒钟的输出流量。单位为KB。
        'MySQL_QPSTPS',  # 平均每秒SQL语句执行次数，平均每秒事务数。
        'MySQL_Sessions',  # 当前活跃连接数，当前总连接数。
        'MySQL_InnoDBBufferRatio',  # InnoDB缓冲池的读命中率，InnoDB缓冲池的利用率，InnoDB缓冲池脏块的百分率。
        'MySQL_InnoDBDataReadWriten',  # InnoDB平均每秒钟读取的数据量，InnoDB平均每秒钟写入的数据量。单位为KB。
        'MySQL_InnoDBLogRequests',  # 平均每秒向InnoDB缓冲池的读次数，平均每秒向InnoDB缓冲池的写次数。
        'MySQL_InnoDBLogWrites',  # 平均每秒日志写请求数，平均每秒向日志文件的物理写次数，平均每秒向日志文件完成的fsync()写数量。
        'MySQL_TempDiskTableCreates',  # MySQL执行语句时在硬盘上自动创建的临时表的数量。
        'MySQL_MyISAMKeyBufferRatio',  # MyISAM平均每秒Key Buffer利用率，MyISAM平均每秒Key Buffer读命中率，
        # MyISAM平均每秒Key Buffer写命中率。
        'MySQL_MyISAMKeyReadWrites',  # MyISAM平均每秒钟从缓冲池中的读取次数，MyISAM平均每秒钟从缓冲池中的写入次数，
        # MyISAM平均每秒钟从硬盘上读取的次数，MyISAM平均每秒钟从硬盘上写入的次数。
        'MySQL_COMDML',  # 平均每秒Delete语句执行次数，平均每秒Insert语句执行次数， 平均每秒Insert_Select语句执行次数，
        # 平均每秒Replace语句执行次数，平均每秒Replace_Select语句执行次数，平均每秒Select语句执行次数，平均每秒Update语句执行次数。
        'MySQL_RowDML',  # 平均每秒从InnoDB表读取的行数，平均每秒从InnoDB表更新的行数，平均每秒从InnoDB表删除的行数，
        # 平均每秒从InnoDB表插入的行数，平均每秒向日志文件的物理写次数
        'MySQL_MemCpuUsage',  # MySQL实例CPU使用率(占操作系统总数)，MySQL实例内存使用率(占操作系统总数)。
        'MySQL_IOPS',  # MySQL实例的IOPS（每秒IO请求次数）。
        'MySQL_DetailedSpaceUsage',  # MySQL实例空间占用详情：ins_size实例总空间使用量;data_size数据空间;
        # log_size日志空间;tmp_size临时空间;other_size系统空间。
        'MySQL_CPS',  # MySQL实例每秒连接数。
    ]
    metric_name = kwargs.get('metric_name')
    if kwargs.get('metric_name') not in metric_numerate:
        raise Exception(f'{metric_name} 不在 metric_numerate 里面，请核对。')
    instances_request = CommonRequest(domain=settings.DEPLOY_CONF.get('aliyun_api_address', 'rds'),
                                      version='2014-08-15',
                                      action_name='DescribeDBInstancePerformance')
    instances_request.add_query_param('DBInstanceId', kwargs.get('db_instance_id'))
    instances_request.add_query_param('Key', metric_name)
    instances_request.add_query_param('StartTime', kwargs.get('start_time'))
    instances_request.add_query_param('EndTime', kwargs.get('end_time'))
    response = client.do_action_with_exception(instances_request)
    res_instance_dict = json.loads(response.decode())
    return res_instance_dict.get('PerformanceKeys').get('PerformanceKey')[0].get('Values').get('PerformanceValue')


def __get_rds_process_list(client: AcsClient, kwargs):
    instances_request = CommonRequest(domain=settings.DEPLOY_CONF.get('aliyun_api_address', 'rds'),
                                      version='2014-08-15',
                                      action_name="DescribeCloudDBAService")
    instances_request.add_query_param('ServiceRequestType', 'ShowProcessList')
    instances_request.add_query_param('ServiceRequestParam', "{\"Language\":\"zh\",\"Command\":\"Not Sleep\"}")
    instances_request.add_query_param('DBInstanceId', kwargs.get('db_instance_id'))
    response = client.do_action_with_exception(instances_request)
    res_instance_dict = json.loads(response.decode())
    return json.loads(res_instance_dict.get('AttrData')).get('ProcessList')


# 调用入口
def get_aliyun_resource(access_key: str, access_secret: str, region_id: str, resource: str='ecs', kwargs=None) -> list:
    if not kwargs:
        kwargs = {}
    client = AcsClient(access_key, access_secret, region_id)
    assert isinstance(eval(f'__get_{resource}'), FunctionType), f'aliyun_api 不存在 {resource} 资源'
    return eval(f'__get_{resource}')(client, kwargs)
