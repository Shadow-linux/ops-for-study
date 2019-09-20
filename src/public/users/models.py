from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UsersAccount(AbstractUser):
    """
        用户
    """
    CA_CHOICE = [
        (0, '不允许'),
        (1, '只读'),
        (2, '读写')
    ]

    real_name = models.CharField(max_length=100, help_text='str: 真实姓名')
    mobile = models.CharField(max_length=15, help_text='str: 手机号', null=True, blank=True)
    email = models.CharField(max_length=100, help_text='str: 邮箱')
    position = models.CharField(max_length=100, help_text='str: 职位')
    department = models.CharField(max_length=100, help_text='str: 部门')
    login_position = models.CharField(max_length=200, help_text='str: 登录位置', null=True, blank=True)

    class Meta:
        verbose_name = '用户'
        db_table = 'users_account'

    def __str__(self):
        return self.username
