# -*- coding: utf-8 -*-
__ProductName__ = "PyCharm"
__Author__ = "J.H.Wei"
__CreatedTime__ = "2019/9/20 9:56"
__FileName__ = "ReadConfig.py"

import ConfigParser
import os
import sys


class ReadConfig(object):
    """
    定义一个读取配置文件的类
    """

    def __init__(self, filepath=None):
        if filepath:
            configpath = filepath
        else:
            root_dir = os.path.dirname(os.path.dirname(__file__))
            configpath = os.path.join(root_dir, "conf/config.ini")
        self.cf = ConfigParser.SafeConfigParser()
        self.cf.read(configpath)

    def get_db(self, param):
        value = self.cf.get("db", param)
        return value

    def get_other(self, param):
        value = self.cf.get("other", param)
        return value


if __name__ == '__main__':
    test = ReadConfig()
    reader = test.get_db("reader")
    writer = test.get_db("writer")
    schema_r = test.get_db("schema_r")

    print len(schema_r)
    print reader
    print writer
