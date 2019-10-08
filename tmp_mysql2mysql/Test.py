# -*- coding: utf-8 -*-
__ProductName__ = "PyCharm"
__Author__ = "J.H.Wei"
__CreatedTime__ = "2019/9/29 15:15"
__FileName__ = "Test.py"

from master.CreateJson import CreateJson


def main():
    cj = CreateJson()
    writer_col_list = cj.get_col_list()

    return writer_col_list


if __name__ == '__main__':
    print main()
