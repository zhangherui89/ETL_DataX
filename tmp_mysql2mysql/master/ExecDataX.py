# -*- coding: utf-8 -*-
__ProductName__ = "PyCharm"
__Author__ = "J.H.Wei"
__CreatedTime__ = "2019/9/20 17:40"
__FileName__ = "ExecDataX.py"

import os
from CreateJson import CreateJson


class ExecDataX(object):
    """
    执行DataX任务
    """
    def __init__(self):
        self.__cj = CreateJson()
        self.sql_table = self.__cj.sql_table
        self.datax_home = self.__cj.datax_home
        self.json_path = self.__cj.output_json_path

    def run(self):
        os.system("python %sdatax.py %s" % (self.datax_home, self.json_path))

        print "表%s初始化完毕..." % self.sql_table


if __name__ == '__main__':
    test = ExecDataX()
    print test.sql_table
