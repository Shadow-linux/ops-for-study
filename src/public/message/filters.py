# from django_filters import  rest_framework as filters
#
#
# class InnerMessageFB(filters.DjangoFilterBackend):
#     def get_filterset_class(self, view, queryset=None):
#         if view.action == 'update':
#             return InnerMessageFilter
#
#
# class InnerMessageFilter(filters.filters):
#     WHAT_CHOICES = [
#         ('unread_count', '未读消息数量'),
#         ('content', '消息内容')
#     ]
#     what = filters.CharFilter(method='get_what', help_text='', choices=WHAT_CHOICES)
