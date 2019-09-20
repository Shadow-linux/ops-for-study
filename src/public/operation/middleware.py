"""
所有自定义的middleware
"""
import json
import threading
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest, HttpResponse
from .models import OperationGlobalLog
from public.util.libs import get_logger


LOGGER = get_logger('operation.middleware')


class RequestExceptionMiddleware(MiddlewareMixin):
    """
    处理错误记录到日志
    """
    def process_exception(self, request, exception):
        user = str(request.user)
        uri = request.path_info
        method = request.method
        data = request.body.decode()
        message = f'''
[Process Exception]
用户: {user}
URI: {uri}
Method: {method}
Data: {data}
Exception: {exception}
        '''
        LOGGER.error(message)
        return None


class GlobalOperatingLogMiddleware(MiddlewareMixin):
    """
    记录操作日志
    """
    methods_2_actions = {
        'POST': 'create',
        'PUT': 'update',
        'PATCH': 'partial_update',
        'DELETE': 'destroy',
    }
    view_op_actions = ('create', 'update', 'partial_update', 'destroy', 'post', 'put', 'delete', 'patch')
    record_methods = ('POST', 'PUT', 'PATCH', 'DELETE')

    def process_view(self, request: HttpRequest, view_func, view_args, view_kwargs):
        """
        建立数据操作记录
        """
        if request.method in self.record_methods and self.__post_to_get(request):
            descriptions_dict = self.handle_view_doc(view_func.__doc__)
            # 用于获取ViewSet 方法注释
            desc = descriptions_dict.get(self.methods_2_actions[request.method], None)
            # 用于获取ApiView 方法的注释
            if not desc:
                desc = descriptions_dict.get(request.method.lower(), None)

            op_global_log_obj = OperationGlobalLog.objects.create(
                uri=request.path_info,
                method=request.method,
                data=request.body.decode(),
                description=desc if desc else f'{view_func.__name__} 该方法没有描述，请添加描述',
            )
            request.__dict__['op_global_log_obj'] = op_global_log_obj

    def process_response(self, request, response: HttpResponse):
        """
        修改操作记录的状态是否成功
        """
        if request.method in self.record_methods and self.__post_to_get(request):
            request.op_global_log_obj.user = str(request.user)
            if not str(response.status_code).startswith('2'):
                request.op_global_log_obj.is_succeed = 0
            threading.Thread(target=self.save, args=(request.op_global_log_obj,)).start()
        return response

    def save(self, modal_obj: OperationGlobalLog):
        modal_obj.save()

    def __post_to_get(self, request) -> bool:
        # 为了某些过长的GET 请求转而使用 POST来拉取数据时，就不对其进行记录
        if request.method == 'POST':
            if json.loads(request.body.decode()).get('http_method', None) == 'GET':
                return False
        return True

    def handle_view_doc(self, doc_data: str) -> dict:
        doc_data_list = doc_data.split('\n')
        description_map = []
        need_next = False
        idx = 0

        for line_data in doc_data_list:
            if need_next:
                description_map[idx][1] = line_data.strip()
                idx += 1
                need_next = False
            for action in self.view_op_actions:
                if line_data.lower().strip().startswith(action):
                    description_map.append([action, None])
                    need_next = True

        return dict(description_map)
