"""
发送消息接口
支持：
    1. 站内
    2. 邮箱
"""
import os
import json
import threading
from abc import ABCMeta, abstractmethod
from django.conf import settings
from users.models import UsersAccount
from .models import MessageInner, MessageMail
from common.models import SettingConf
from util import libs, send_mail

logger = libs.get_logger('sender')


class BaseSenderImplement(metaclass=ABCMeta):
    """
    sender 的基本类
    """
    def __init__(self, title, content, receiver_user_id_list, work_order, **kwargs):
        self.title = title
        self.content = content
        self.receiver_user_id_list = receiver_user_id_list
        self.kwargs = kwargs
        self.work_order = work_order

    @abstractmethod
    def format_message(self) -> str:
        """
        格式化发送的信息，必须复写
        """
        raise NotImplementedError('`format_message()` must be implemented.')

    @abstractmethod
    def save_message(self, content: str):
        """
        持久化信息数据， 必须复写
        """
        raise NotImplementedError('`save_message()` must be implemented.')

    def already(self) -> str:
        """
        数据已准备好，在每次调用start之前必须执行already， 无需复写
        """
        format_content = self.format_message()
        self.save_message(format_content)
        return format_content

    @abstractmethod
    def start(self):
        """
        启动发送消息功能，必须复写
        """
        self.already()
        raise NotImplementedError('`start()` must be implemented.')


class InnerSender(BaseSenderImplement):
    """
    站内信息发送
    """
    def format_message(self):
        return f'''<p style="indent: 10px">{self.content}</p>'''

    def save_message(self, content):
        for user_id in self.receiver_user_id_list:
            MessageInner.objects.create(
                user_id=user_id,
                title=self.title,
                content=content,
                is_succeed=1,
                work_order=self.work_order
            )

    def start(self):
        self.already()


class MailSender(BaseSenderImplement):
    """
    邮件信息发送
    """
    def __init__(self, title, content, receiver_user_id_list, work_order, **kwargs):
        super().__init__(title, content, receiver_user_id_list, work_order, **kwargs)
        self.receiver_list = []
        self.mail_message_id = []

    def format_message(self):
        context = {
            'title': self.title,
            'content': self.content
        }
        data = libs.template_render2data(context,
                                         os.path.join(settings.STATICFILES_DIRS[0], 'message_template/mail.html'))
        return data

    def save_message(self, content):
        for user_id in self.receiver_user_id_list:
            try:
                receiver = UsersAccount.objects.get(id=user_id).email
                message_mail_obj = MessageMail.objects.create(
                    user_id=user_id,
                    receiver=receiver,
                    title=self.title,
                    content=content,
                    is_succeed=1,
                    work_order=self.work_order
                )
                self.mail_message_id.append(message_mail_obj.id)
                for item in receiver.split(','):
                    if item != '':
                        self.receiver_list.append(item)
            except Exception as e:
                pass

    def start(self):
        try:
            format_content = self.already()
            setting_global_obj = SettingConf.objects.get(owner='global')
            message_conf = json.loads(setting_global_obj.message_setting)
            send_mail_obj = send_mail.SendMail(
                message_conf['mail']['mail_user'],
                message_conf['mail']['mail_password'],
                message_conf['mail']['smtp_host'],
                message_conf['mail']['smtp_port'],
                message_conf['mail']['smtp_ssl']
            )
            send_mail_obj.received_address = self.receiver_list
            send_mail_obj.subject = self.title
            send_mail_obj.message = format_content
            send_mail_obj.start()
        except Exception as e:
            for mail_id in self.mail_message_id:
                mail_obj = MessageMail.objects.get(id=mail_id)
                mail_obj.is_succeed = 0
                mail_obj.save()
            raise e


class MessageSender(BaseSenderImplement):
    def format_message(self) -> str:
        pass

    def save_message(self, content: str):
        pass

    def start(self):
        pass


class WeChatSender(BaseSenderImplement):
    def format_message(self) -> str:
        pass

    def save_message(self, content: str):
        pass

    def start(self):
        pass


SENDER_DICT = {
    'inner': InnerSender,
    'mail': MailSender,
    'message': MessageSender,
    'wechat': WeChatSender
}


def sender(title: str, content: str, receiver_user_id_list: list, send_type: str='inner', work_order=None, **kwargs):
    try:
        logger.info(f"发送 {title} 信息，发送类型: {send_type}")
        if not work_order:
            work_order = libs.get_work_order('message')
        setting_global_obj = SettingConf.objects.get(owner='global')
        if eval(f"setting_global_obj.is_{send_type.lower()}"):
            sender_obj = SENDER_DICT[send_type]
            sd = sender_obj(title, content, receiver_user_id_list, work_order, **kwargs)
            t = threading.Thread(target=sd.start).start()
    except Exception as e:
        logger.error(f"发送 {title} 信息失败，发送类型: {send_type}, 接收用户id: {receiver_user_id_list}")
        logger.exception(e)


# 这是独立使用的send mail
def send_mail2target(title: str, content: str, receiver_list: list):
    setting_global_obj = SettingConf.objects.get(owner='global')
    message_conf = json.loads(setting_global_obj.message_setting)
    print(message_conf['mail']['smtp_ssl'])
    send_mail_obj = send_mail.SendMail(
        message_conf['mail']['mail_user'],
        message_conf['mail']['mail_password'],
        message_conf['mail']['smtp_host'],
        message_conf['mail']['smtp_port'],
        message_conf['mail']['smtp_ssl']
    )
    send_mail_obj.received_address = receiver_list
    send_mail_obj.subject = title
    send_mail_obj.message = content
    send_mail_obj.start()
