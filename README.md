# ETL_DataX
基于DataX的ETL工具，目前实现了Mysql和Sqlserver共四种组合的reader到writer过程



其中：
tmp_mysql2mysql：为目标表的表名

common：为通用模块，主要为json模板，读取配置文件参数模块，一些工具类模块，获取目标表元数据相关sql

conf：为配置文件模块，主要为配置数据库参数config.ini，读取数据read.sql，预处理pre.sql，后处理post.sql

master：为程序主要模块，分为创建DataX所需的json文件模块，执行DataX任务抽取数据模块

output_json：为存放json文件的目录

main.py：为程序入口


