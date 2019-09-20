# coding: utf-8

from email.header import Header
from email.mime.text import MIMEText
import smtplib

# mail list 收邮件地址


class SendMail:
    """
    :usage:
        send_mail = SendMail()
        send_mail.received_address = ['123@aiyuangong.com']
        send_mail.subject = 'reset password'
        send_mail.message = 'hello world'
        send_mail.start()
    """
    def __init__(self, mail_user, mail_password, smtp_host, smtp_port, ssl=False):

        # 文本内容路径
        self.email_address = mail_user
        self.password = mail_password
        # 地址列表
        self.received_address = None
        self.smtp_server = smtp_host
        self.smtp_port = smtp_port
        self.ssl = ssl
        self.subject = None
        self.message = None
        self.__build_smtp()

    def __check_received_address(self):
        if not isinstance(self.received_address, list) and not self.received_address:
            raise Exception('received_address not list instance')

    # 建立smtp连接
    def __build_smtp(self):
        try:
            if self.ssl:
                self.server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            else:
                self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.server.set_debuglevel(1)
            self.server.login(self.email_address, self.password)
        except Exception as e:
            raise e

    # 添加收件人发件人头部
    def __format_header(self):
        self.msg['From'] = self.email_address
        self.msg['To'] = ','.join(self.received_address)
        self.subject = self.subject if self.subject else ''
        self.msg['Subject'] = Header('{}'.format(self.subject), 'utf-8').encode()

    # 获取文本信息
    def __get_message(self):
        message = self.message if self.message else 'Hello everyone, this is ops mail test.'
        self.msg = MIMEText(message, 'HTML', 'utf-8')
        self.__format_header()

    def __send(self):
        self.server.sendmail(self.email_address, self.received_address, self.msg.as_string())

    def start(self):
        try:
            self.__get_message()
            self.__send()
        except Exception as e:
            raise e
