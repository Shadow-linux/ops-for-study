from django.db import models

# Create your models here.


class PermissionAll(models.Model):
    group_id = models.IntegerField(help_text='组名ID', null=True)
    # page_permission 数据结构: {'home': 0 } , 0 无权限， 1 只读权限，2 读写权限
    page_permission = models.CharField(max_length=1024, help_text='页面权限', null=True)

    class Meta:
        db_table = 'permissions_all'

    def __str__(self):
        return self.group_id
