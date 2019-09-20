from django.db import models

# Create your models here.


class OperationGlobalLog(models.Model):
    """
    日志记录操作
    """
    IS_SUCCEED_CHOICE = [
        (0, '失败'),
        (1, '成功')
    ]
    user = models.CharField(max_length=150, help_text='用户名')
    uri = models.CharField(max_length=100, help_text='操作的uri')
    method = models.CharField(max_length=10, help_text='http方法')
    data = models.TextField(help_text='操作的数据')
    description = models.CharField(max_length=200, help_text='操作描述')
    time = models.DateTimeField(auto_now_add=True, help_text='操作时间')
    is_succeed = models.BooleanField(default=1, help_text='是否成功，0 失败，1 成功', choices=IS_SUCCEED_CHOICE)

    def __str__(self):
        return self.uri

    class Meta:
        db_table = 'operation_global_log'
