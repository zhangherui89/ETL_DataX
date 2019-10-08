# -*- coding: utf-8 -*-
__ProductName__ = "PyCharm"
__Author__ = "J.H.Wei"
__CreatedTime__ = "2019/9/20 10:46"
__FileName__ = "CreateJson.py"

import os
import sys

dirname = os.path.dirname(os.path.dirname(__file__))  # 获取上上级目录
sys.path.append(dirname)  # 系统加入上上级目录

import json
from common.json import json_dict
from common.ReadConfig import *
from common.utils import *
from common.MetaSQL import metasql_dict


class CreateJson(object):
    def __init__(self):
        self.dirname = dirname  # 表所在目录
        self.sql_table = os.path.basename(dirname)  # 获取上上级目录的当前文件夹名，即writer部分表名

        # 读取参数
        self.__dbconfig = ReadConfig()
        self.reader = self.__dbconfig.get_db("reader")
        self.writer = self.__dbconfig.get_db("writer")

        # reader数据库相关参数
        self.host_r = self.__dbconfig.get_db("host_r")
        self.user_r = self.__dbconfig.get_db("user_r")
        self.password_r = self.__dbconfig.get_db("password_r")
        self.database_r = self.__dbconfig.get_db("database_r")
        self.port_r = self.__dbconfig.get_db("port_r")
        self.schema_r = self.__dbconfig.get_db("schema_r")

        # writer数据库相关参数
        self.host_w = self.__dbconfig.get_db("host_w")
        self.user_w = self.__dbconfig.get_db("user_w")
        self.password_w = self.__dbconfig.get_db("password_w")
        self.database_w = self.__dbconfig.get_db("database_w")
        self.port_w = self.__dbconfig.get_db("port_w")
        self.schema_w = self.__dbconfig.get_db("schema_w")

        # DataX目录
        self.datax_home = self.__dbconfig.get_other("datax_home")

        # json文件保存目录
        self.output_json_path = os.path.join(self.dirname, "output_json/%s.json" % self.sql_table)

    def get_json_template(self):
        # 获取reader和writer部分json模板
        reader_json = [row for row in json_dict["reader"] if row["name"] == "%sreader" % self.reader]
        writer_json = [row for row in json_dict["writer"] if row["name"] == "%swriter" % self.writer]

        # datax的json模版
        template_json = {
            "job": {
                "setting": {
                    "speed": {
                        "byte": 1048576,
                        "channel": "4",
                    }
                },
                "content": [
                    {
                        "reader": reader_json[0],

                        "writer": writer_json[0]
                    }
                ]
            }
        }

        return template_json

    def get_readsql(self):
        # 获取reader的querySql,从配置文件获取
        with open(os.path.join(self.dirname, "conf/read.sql"), "r") as f:
            select_sql = f.read()
            f.close()
        return select_sql

    def get_presql(self):
        with open(os.path.join(self.dirname, "conf/pre.sql"), "r") as f:
            pre_sql = f.read()
            f.close()
        return pre_sql

    def get_postsql(self):
        with open(os.path.join(self.dirname, "conf/post.sql"), "r") as f:
            post_sql = f.read()
            f.close()
        return post_sql

    def get_col_list(self):
        # 获取目标表的字段
        writer_col_list = []
        meta_param = (self.database_w, self.sql_table) if self.schema_w == "" else (self.schema_w, self.sql_table)
        sql = metasql_dict[self.writer].format(meta_param[0], meta_param[1])
        rs = getSQLResult(self.writer, sql, self.host_w, self.user_w, self.password_w, self.database_w,
                          int(self.port_w))

        for row in rs:
            colName = row[0]
            colType = row[1]
            colComment = row[2]
            writer_col_list.append(colName)

        return writer_col_list

    def set_json_parma(self):
        template_json = self.get_json_template()
        select_sql = self.get_readsql()
        pre_sql = self.get_presql()
        post_sql = self.get_postsql()
        writer_col_list = self.get_col_list()

        # 配置reader部分json参数
        template_json["job"]["content"][0]["reader"]["parameter"]["username"] = self.user_r
        template_json["job"]["content"][0]["reader"]["parameter"]["password"] = self.password_r
        reader_jdbc = template_json["job"]["content"][0]["reader"]["parameter"]["connection"][0]["jdbcUrl"]
        template_json["job"]["content"][0]["reader"]["parameter"]["connection"][0]["jdbcUrl"] = [reader_jdbc[0].format(
            host=self.host_r, port=self.port_r, database=self.database_r)]
        template_json["job"]["content"][0]["reader"]["parameter"]["connection"][0]["querySql"] = [select_sql]

        # 配置writer部分json参数
        template_json["job"]["content"][0]["writer"]["parameter"]["username"] = self.user_w
        template_json["job"]["content"][0]["writer"]["parameter"]["password"] = self.password_w
        template_json["job"]["content"][0]["writer"]["parameter"]["column"] = writer_col_list
        template_json["job"]["content"][0]["writer"]["parameter"]["preSql"] = [] if pre_sql.strip() == "" else [pre_sql]
        template_json["job"]["content"][0]["writer"]["parameter"]["postSql"] = [] if post_sql.strip() == "" else [
            post_sql]
        writer_jdbc = template_json["job"]["content"][0]["writer"]["parameter"]["connection"][0]["jdbcUrl"]
        template_json["job"]["content"][0]["writer"]["parameter"]["connection"][0]["jdbcUrl"] = writer_jdbc.format(
            host=self.host_w, port=self.port_w, database=self.database_w)

        sql_table_param = self.sql_table if self.schema_w == "" else "%s.%s" % (self.schema_w, self.sql_table)
        template_json["job"]["content"][0]["writer"]["parameter"]["connection"][0]["table"] = [sql_table_param]

        return template_json

    def del_json_files(self):
        output_json_dir = os.path.join(os.path.dirname(self.output_json_path), "*")
        os.system("rm -rf %s" % output_json_dir)  # 删除output_json文件夹下所有的json文件
        print "output_json文件夹下所有的json文件已删除..."

    def save_json(self):
        self.del_json_files()  # 保存json文件前，先删除output_json目录下的所有文件
        template_json = self.set_json_parma()
        # 保存json文件
        print "开始输出业务库{sql_db}的数据表{sql_table}的DataX Json模板...".format(sql_db=self.database_w, sql_table=self.sql_table)
        with open(self.output_json_path, 'w') as f:
            json.dump(template_json, f, indent=4, ensure_ascii=False)

        print "%s.json生成完毕..." % self.sql_table

        return "Save json file successfully..."

    def run(self):
        self.save_json()


if __name__ == '__main__':
    test = CreateJson()
    test.run()
