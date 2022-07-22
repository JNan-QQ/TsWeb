# -*- coding:utf-8 -*-
# @FileName  :Mysql_Read.py
# @Time      :2021/7/20 9:53
# @Author    :姜楠
# @Tool      :PyCharm
import os
import sqlite3

import MySQLdb


# 整数与ip地址相互转发你
def int2ip(num):
    if not num:
        return ''
    iplist = []
    for n in range(4):
        num, mod = divmod(num, 256)
        iplist.insert(0, str(mod))
    return '.'.join(iplist)


def ip2int(ip):
    if not ip:
        return ''
    ip_list = ip.strip().split('.')
    SUM = 0
    for i in range(len(ip_list)):
        SUM += int(ip_list[i]) * 256 ** (3 - i)
    return SUM


def mysql_read(sql):
    from config.config import getCaseConfigData
    conf = getCaseConfigData.MysqlLinkInfo
    # 创建一个 Connection 对象，代表了一个数据库连接
    connection = MySQLdb.connect(

        host=int2ip(conf[0]),  # 数据库IP地址
        port=conf[1],
        user=conf[2],  # mysql用户名
        passwd=conf[3],  # mysql用户登录密码
        db=conf[4],  # 数据库名
        # 如果数据库里面的文本是utf8编码的，
        # charset指定是utf8
        charset="utf8"
    )

    # 返回一个 Cursor对象
    c_mysql = connection.cursor()
    c_mysql.execute(sql)
    row = c_mysql.fetchone()

    c_mysql.close()
    connection.close()

    return row


class Sqlit3Link:
    def __init__(self):
        self.connect = sqlite3.connect(
            os.path.join(os.path.abspath(__file__ + os.path.sep + ".." + os.path.sep + ".."), 'config', 'config.db')
        )
        self.cursor = self.connect.cursor()

    # 插入数据
    def insert_table(self, table_name, *values):
        """
        :param table_name: 表名称(字段1，字段2)
        :param values: 写入字段的值  例：(1,'name',6)
        :return: None
        """
        if len(values) == 1:
            self.cursor.execute(
                "insert into {} values ({})".format(table_name, ','.join(list('?' * len(values[0])))), values[0])
        else:
            self.cursor.executemany(
                "insert into {} values ({})".format(table_name, ','.join(list('?' * len(values[0])))), values)
        self.connect.commit()

    # 查询数据
    def select_table(self, table_name, where_filter=None, *field):
        """
        :param table_name: 表名称
        :param where_filter: 过滤规则   例：'id=1'
        :param field: 查询字段名称    例：'name','age'
        :return: SET
        """
        if where_filter:
            sql = f"select {'*' if not field else ','.join(field)} from {table_name} where {where_filter} ORDER BY -id"
        else:
            sql = f"select {'*' if not field else ','.join(field)} from {table_name}  ORDER BY -id"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # 修改数据
    def modify_table(self, table_name, where_filter, **field):
        """
        :param table_name: 表名称
        :param where_filter: 过滤规则   例：'id=1'
        :param field: 修改字段名称=修改值    例：name='tome',age=16
        :return: None
        """
        sql = f"""
                update {table_name} set {','.join("{}='{}'".format(k, v) for k, v in field.items())} where {where_filter}
            """
        self.cursor.execute(sql)
        self.connect.commit()

    # 删除数据
    def delete_table(self, table_name, where_filter):
        """
        :param table_name: 表名称
        :param where_filter: 过滤规则   例：'id=1'
        :return:
        """
        self.cursor.execute(f"delete from {table_name} where {where_filter}")
        self.connect.commit()

    def close(self):
        self.cursor.close()
        self.connect.close()


sqlite3Link = Sqlit3Link()
