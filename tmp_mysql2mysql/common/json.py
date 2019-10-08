# -*- coding: utf-8 -*-
__ProductName__ = "PyCharm"
__Author__ = "J.H.Wei"
__CreatedTime__ = "2019/9/20 10:58"
__FileName__ = "json.py"

"""

配置DataX所需的json文件中reader和writer部分的模板

"""
json_dict = {
    "reader": [
        {
            "name": "mysqlreader",
            "parameter": {
                "username": "",
                "password": "",
                "column": [],
                "where": "",
                "splitPk": "",
                "connection": [
                    {
                        "querySql": [],
                        "jdbcUrl": ["jdbc:mysql://{host}:{port}/{database}"]
                    }
                ]
            }
        },

        {
            "name": "sqlserverreader",
            "parameter": {
                "username": "",
                "password": "",
                "column": [],
                "where": "",
                "splitPk": "",
                "connection": [
                    {
                        "querySql": [],
                        "jdbcUrl": ["jdbc:sqlserver://{host}:{port};DatabaseName={database}"]
                    }
                ]
            }
        },
    ],

    "writer": [
        {
            "name": "mysqlwriter",
            "parameter": {
                "writeMode": "replace",
                "username": "",
                "password": "",
                "column": [],
                "session": [],
                "preSql": [],
                "postSql": [],
                "connection": [
                    {
                        "jdbcUrl": "jdbc:mysql://{host}:{port}/{database}",
                        "table": []
                    }
                ]
            }
        },

        {
            "name": "sqlserverwriter",
            "parameter": {
                "username": "",
                "password": "",
                "column": [],
                "connection": [
                    {
                        "table": [],
                        "jdbcUrl": "jdbc:sqlserver://{host}:{port};DatabaseName={database}"
                    }
                ],
                "preSql": [],
                "postSql": []
            }
        }

    ]
}
