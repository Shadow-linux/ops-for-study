from django.db import models

# Create your models here.

IS_SUCCEED_CHOICE = [
    (0, '失败'),
    (1, '成功')
]


class MessageMail(models.Model):
    """
    邮件信息
    """
    work_order = models.CharField(max_length=100, default=None, help_text='int; 工单号')
    user_id = models.IntegerField(help_text='int; 用户id')
    receiver = models.TextField(help_text='st;: 目标邮箱')
    title = models.CharField(max_length=200, help_text='str; 邮件标题')
    content = models.TextField(help_text='str; 邮件内容')
    is_succeed = models.BooleanField(default=False, choices=IS_SUCCEED_CHOICE, help_text='str; 是否发送成功')
    created = models.DateTimeField(auto_now_add=True, help_text='str; 创建时间')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'message_mail'
        verbose_name = '邮件信息'


class MessageInner(models.Model):
    """
    站内信息
    """
    STATUS_CHOICES = [
        (0, 'trash'),
        (1, 'unread'),
        (2, 'read')
    ]
    work_order = models.CharField(max_length=100, default=None, help_text='int; 工单号')
    user_id = models.TextField(help_text='int; 接收用户的id')
    title = models.CharField(max_length=200, help_text='str; 标题')
    content = models.TextField(help_text='str; 内容')
    is_succeed = models.BooleanField(default=False, choices=IS_SUCCEED_CHOICE, help_text='str; 是否发送成功')
    created = models.DateTimeField(auto_now_add=True, help_text='str; 创建时间')
    status = models.SmallIntegerField(default=1,
                                      choices=STATUS_CHOICES,
                                      help_text='int; 状态: 0 trash, 1 unread, 2 read')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'message_inner'
        verbose_name = '站内信息'


class MessagePush(models.Model):
    """
    消息推送
    """
    work_order = models.CharField(max_length=100, default=None, help_text='int; 工单号')
    title = models.CharField(max_length=100, help_text='str; 标题')
    content = models.TextField(help_text='str; 消息内容')
    user_id_list = models.CharField(max_length=500, help_text='str; 用户ID')
    send_type_list = models.CharField(max_length=500, help_text='str; 发送消息类型')
    created = models.DateTimeField(auto_now_add=True, help_text='str; 创建时间')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'message_push'
        verbose_name = '消息推送'