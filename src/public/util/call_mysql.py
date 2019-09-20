"""
连接数据库方法
"""
# coding: utf-8
import pymysql
from .libs import local_mysql_conf

class OpsMysqlClient(object):

    def __init__(self,
                 host: str=local_mysql_conf['host'],
                 username: str=local_mysql_conf['username'],
                 password: str=local_mysql_conf['password'],
                 schema: str=local_mysql_conf['schema'],
                 port: int=int(local_mysql_conf['port'])):
        self.host = host
        self.username = username
        self.password = password
        self.schema = schema
        self.port = port
        self.cursor = object

    def __enter__(self):
        self.connection = pymysql.connect(
            host=self.host,
            user=self.username,
            passwd=self.password,
            db=self.schema,
            charset='utf8mb4',
            port=int(self.port),
        )
        self.cursor = self.connection.cursor(cursor=pymysql.cursors.DictCursor)
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
