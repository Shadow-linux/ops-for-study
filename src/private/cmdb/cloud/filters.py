from django_filters import rest_framework as filters
from .models import AliyunKeys, AliyunEcs, AliyunRDS

# --------------------------------------- 阿里云 ---------------------------------------


class AliyunGraphFilter(filters.FilterSet):
    ACTION_CHOICES = [
        ('ecs_graph', 'Ecs 图表数据'),
        ('disk_graph', 'Disk 图表数据')
    ]
    action = filters.CharFilter(method='return_query_set',
                                help_text='''str; 选择图表数据类型, [ecs|ecs_graph|disk|rds]''',
                                required=True)
    kwargs = filters.CharFilter(method='return_query_set', help_text='''str; 数据格式
    {
        "metric": "cpu_idle",
        "region_id": "cn-shenzhen",
        "days": 7,
        "dimensions": "[{\\"instanceId\\": \\"i-wz9exmnpyufi62y6dnbc\\"}]"
    }''', required=True)

    def return_query_set(self, queryset, name, value):
        return queryset

    class Meta:
        model = AliyunKeys
        fields = ['action', 'kwargs']


class AliyunKey2ECsFilter(filters.FilterSet):
    ac_key_id = filters.CharFilter(help_text='int; access key id', required=True)

    class Meta:
        model = AliyunEcs
        fields = ['ac_key_id']


class AliyunKey2RdsFilter(filters.FilterSet):
    ac_key_id = filters.CharFilter(help_text='int; access key id', required=True)

    class Meta:
        model = AliyunRDS
        fields = ['ac_key_id']


class AliyunRdsGraphFilter(filters.FilterSet):
    metric_name = filters.CharFilter(help_text='str; metric name', required=True, method='return_query_set')
    start_time = filters.CharFilter(help_text='str; start time', required=True, method='return_query_set')
    end_time = filters.CharFilter(help_text='str; start time', required=True, method='return_query_set')

    def return_query_set(self, queryset, name, value):
        return queryset

    class Meta:
        model = AliyunRDS
        fields = ['metric_name', 'start_time', 'end_time']
