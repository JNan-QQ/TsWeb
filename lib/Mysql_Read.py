# -*- coding:utf-8 -*-
# @FileName  :Mysql_Read.py
# @Time      :2021/7/20 9:53
# @Author    :姜楠
# @Tool      :PyCharm
import MySQLdb
from config.config import LibConfig


def mysql_read_alpha(sql):
    conf = LibConfig.mysqlAlpha
    # 创建一个 Connection 对象，代表了一个数据库连接
    connection = MySQLdb.connect(

        host=conf[0],  # 数据库IP地址
        user=conf[1],  # mysql用户名
        passwd=conf[2],  # mysql用户登录密码
        db="tswaiyutong_beta",  # 数据库名
        # 如果数据库里面的文本是utf8编码的，
        # charset指定是utf8
        charset="utf8"
    )

    # 返回一个 Cursor对象
    c_mysql = connection.cursor()
    c_mysql.execute(sql)
    # rowcount属性记录了最近一次 execute 方法获取的数据行数
    # numrows = c_mysql.rowcount
    # print(numrows)

    row = c_mysql.fetchone()

    c_mysql.close()
    connection.close()

    return row


def mysql_read_beta(sql):
    conf = LibConfig.mysqlBeta
    # 创建一个 Connection 对象，代表了一个数据库连接
    connection = MySQLdb.connect(

        host=conf[0],  # 数据库IP地址
        port=3307,
        user=conf[1],  # mysql用户名
        passwd=conf[2],  # mysql用户登录密码
        db="tswaiyutong",  # 数据库名
        # 如果数据库里面的文本是utf8编码的，
        # charset指定是utf8
        charset="utf8"
    )

    # 返回一个 Cursor对象
    c_mysql = connection.cursor()
    c_mysql.execute(sql)
    # rowcount属性记录了最近一次 execute 方法获取的数据行数
    numrows = c_mysql.rowcount
    # print(numrows)

    row = c_mysql.fetchone()

    c_mysql.close()
    connection.close()

    return row


def paper_to_test(sql):
    conf = LibConfig.mysqlBeta
    # 创建一个 Connection 对象，代表了一个数据库连接
    connection = MySQLdb.connect(

        host=conf[0],  # 数据库IP地址
        port=3307,
        user=conf[1],  # mysql用户名
        passwd=conf[2],  # mysql用户登录密码
        db="tswaiyutong",  # 数据库名
        # 如果数据库里面的文本是utf8编码的，
        # charset指定是utf8
        charset="utf8"
    )

    # 返回一个 Cursor对象
    c_mysql = connection.cursor()
    c_mysql.execute(sql)
    # rowcount属性记录了最近一次 execute 方法获取的数据行数
    # numrows = c_mysql.rowcount
    # print(numrows)

    row = c_mysql.fetchall()

    c_mysql.close()
    connection.close()

    return row


if __name__ == "__main__":
    print(mysql_read_beta(r'.csj$*`fe/\\'))
