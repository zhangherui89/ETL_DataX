# -*- coding: utf-8 -*-
__ProductName__ = "PyCharm"
__Author__ = "J.H.Wei"
__CreatedTime__ = "2019/9/20 13:46"
__FileName__ = "MetaSQL.py"

"""

配置mysql, sqlserver, oracle 等数据库获取元数据查询sql

"""

metasql_dict = {
    "mysql": """SELECT
	COLUMN_NAME AS colName,
	DATA_TYPE AS colType,
	IFNULL(COLUMN_COMMENT,'') AS colComment
FROM
	information_schema. COLUMNS
WHERE
	table_schema = '{}'
AND table_name = '{}'
ORDER BY
	ORDINAL_POSITION""",

    "sqlserver": """SELECT
	b.name AS colName,
	c.name AS colType,
	isnull(d.[value], '') AS colComment
FROM
	sys.tables a
INNER JOIN sys.columns b ON b.object_id = a.object_id
INNER JOIN sys.types c ON b.user_type_id = c.user_type_id
LEFT JOIN sys.extended_properties d ON d.major_id = b.object_id
AND d.minor_id = b.column_id
INNER JOIN sys.schemas e ON a.schema_id = e.schema_id
WHERE
	e.name = '{}'
AND a.name = '{}'
ORDER BY
	b.column_id""",

    "oracle": """SELECT
      t1.COLUMN_NAME colName,
      t1.DATA_TYPE colType,
      nvl(t2.COMMENTS,' ') colComment
FROM all_tab_columns t1, all_col_comments t2  
    WHERE t1.COLUMN_NAME = t2.COLUMN_NAME  
      AND t1.TABLE_NAME = t2.TABLE_NAME
      AND t1.OWNER='{}'
      AND t1.TABLE_NAME = '{}'
ORDER BY
    t1.COLUMN_ID"""
}
