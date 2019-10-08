# -*- coding: utf-8 -*-
__ProductName__ = "PyCharm"
__Author__ = "J.H.Wei"
__CreatedTime__ = "2019/9/20 10:29"
__FileName__ = "utils.py"

import pymssql
import MySQLdb
import datetime


# 秒转时间
def seconds2time(sec):
    """
    :param sec: 多少秒
    :return: 字符串，格式：xxx天xxx小时xxx秒
    """
    if sec >= 24 * 60 * 60:
        d = sec // (24 * 60 * 60)
        h = (sec - d * 24 * 60 * 60) // (60 * 60)
        m = (sec - d * 24 * 60 * 60 - h * 60 * 60) // 60
        s = sec - d * 24 * 60 * 60 - h * 60 * 60 - m * 60
        return "{}天{}小时{}分钟{}秒".format(int(d), int(h), int(m), s)
    elif sec >= 60 * 60:
        h = sec // (60 * 60)
        m = (sec - h * 60 * 60) // 60
        s = sec - h * 60 * 60 - m * 60
        return "{}小时{}分钟{}秒".format(int(h), int(m), s)
    elif sec >= 60:
        m = sec // 60
        s = sec - m * 60
        return "{}分钟{}秒".format(int(m), s)
    else:
        return "{}秒".format(sec)


def count_time(func):
    """
    统计某个函数的运行时间
    :param func: 函数
    :return: 函数运行时长
    """

    def int_time(*args, **kwargs):
        start_time = datetime.datetime.now()  # 程序开始时间
        func()
        over_time = datetime.datetime.now()  # 程序结束时间
        total_time = (over_time - start_time).total_seconds()
        print "此次任务总计用时：%s" % seconds2time(total_time)

    return int_time


def getSQLResult(dbtype, sql, sql_host, sql_username, sql_password, sql_db, sql_port):
    if (dbtype == 'sqlserver'):
        conn = pymssql.connect(
            host=sql_host,
            user=sql_username,
            password=sql_password,
            database=sql_db,
            port=sql_port,
            charset='utf8')
    elif (dbtype == 'mysql'):
        conn = MySQLdb.connect(
            host=sql_host,
            user=sql_username,
            passwd=sql_password,
            db=sql_db,
            port=sql_port,
            charset='utf8')

    cursor = conn.cursor()
    cursor.execute(sql)
    rs = cursor.fetchall()
    cursor.close()
    conn.close()
    return rs


# 判断数据表是否有数据
def ishaverecord(dbtype, sql_table, sql_host, sql_username, sql_password, sql_db):
    sql_tmp = """select * FROM `{tablename}` limit 1""".format(tablename=sql_table)
    rs = getSQLResult(dbtype, sql_tmp, sql_host, sql_username, sql_password, sql_db)
    return len(rs) > 0
