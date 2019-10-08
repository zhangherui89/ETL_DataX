# -*- coding: utf-8 -*-
__ProductName__ = "PyCharm"
__Author__ = "J.H.Wei"
__CreatedTime__ = "2019/9/20 10:47"
__FileName__ = "main.py.py"

from master.CreateJson import CreateJson
from common.utils import count_time
from master.ExecDataX import ExecDataX


@count_time
def exectask():
    cj = CreateJson()
    cj.run()  # 生成DataX所需的Json文件

    print "开始初始化表：%s..." % cj.sql_table
    print "\n" * 2

    ed = ExecDataX()
    ed.run()  # 执行DataX抽取数据


if __name__ == '__main__':
    exectask()
