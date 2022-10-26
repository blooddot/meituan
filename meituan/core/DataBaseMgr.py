from __future__ import annotations

import json
from typing import Any

import pymysql
from pymysql.cursors import Cursor


class __DataBaseMgr:
    """数据库管理器"""

    __db: pymysql.Connection

    @property
    def db(self) -> pymysql.Connection:
        return self.__db

    __cursor: Cursor

    @property
    def cursor(self):
        return self.__cursor

    def __init__(self):
        self.__db = None
        self.__cursor = None

    def connect(self):
        """数据库连接"""
        if (self.__db != None):
            self.__db.close()

        self.__db = pymysql.connect(
            host="localhost", user="root", database="meituan", port=3306
        )
        self.__cursor = self.__db.cursor()

    def directExecuteSql(self, sql: str):
        """不连接数据库操作，直接执行 SQL 语句"""
        try:
            result = self.__cursor.execute(sql)  # 执行sql语句
            self.__db.commit()  # 提交到数据库执行
            return result
        except:
            print("execute sql error: ", sql)
            self.__db.rollback()  # 如果发生错误则回滚
            return

    def directExecuteSqls(self, sqls: list):
        """不连接数据库操作，直接执行多条 SQL 语句"""
        for sql in sqls:
            self.__cursor.execute(sql)
        self.__db.commit()

    def executeSql(self, sql: str):
        """执行指定 DB 中的 SQL 语句"""
        self.connect()
        self.directExecuteSql(sql)
        self.close()

    def executeSqls(self, sqls: list):
        """执行指定 DB 中的多条 SQL 语句"""
        self.connect()
        self.directExecuteSqls(sqls)
        self.close()

    def close(self):
        """关闭数据库连接"""
        if (self.__cursor != None):
            self.__cursor.close()
            self.__cursor = None

        if (self.__db != None):
            self.__db.close()
            self.__db = None

    def __formatData(self, value):
        """获取格式化数据"""
        if (isinstance(value, str)):
            return f"\"{value}\"" if value.find("\"") < 0 else f"\'{value}\'"

        if (isinstance(value, dict)
           | isinstance(value, list)
           | isinstance(value, tuple)
           | isinstance(value, set)):
            return "'{0}'".format(json.dumps(value, ensure_ascii=False).replace("'", "\\'"))

        return f"{value}"

    def replaceData(self, tableName: str, data: list[tuple[str, Any]], condition: str = "", needConnect: bool = True):
        """替换数据"""
        fields = ""
        values = ""
        for i in range(len(data)):
            [field, value] = data[i]

            value = self.__formatData(value)
            fields += field if i == 0 else f",{field}"
            values += value if i == 0 else f",{value}"

        sql = f"REPLACE INTO {tableName} ({fields}) VALUES({values}) {condition}"
        if (needConnect):
            self.executeSql(sql)
        else:
            self.directExecuteSql(sql)

    def insertData(self,  tableName: str, data: list[tuple[str, Any]], condition: str = "", needConnect: bool = True):
        """插入数据"""
        fields = ""
        values = ""
        for i in range(len(data)):
            [field, value] = data[i]

            value = self.__formatData(value)
            fields += field if i == 0 else f",{field}"
            values += value if i == 0 else f",{value}"

        sql = f"INSERT INTO {tableName} ({fields}) VALUES({values}) {condition}"
        if (needConnect):
            self.executeSql(sql)
        else:
            self.directExecuteSql(sql)

    def updateData(self, tableName: str, data: list[tuple[str, Any]], condition: str = "", needConnect: bool = True):
        """插入数据"""
        dataStr = ""
        length = len(data)
        for i in range(length):
            [field, value] = data[i]

            value = self.__formatData(value)
            if (i == length-1):
                dataStr += f"""{field} = {value} """
            else:
                dataStr += f"""{field} = {value},"""

        sql = f"UPDATE {tableName} SET {dataStr} {condition}"
        if (needConnect):
            self.executeSql(sql)
        else:
            self.directExecuteSql(sql)

    def fetchData(self, tableName: str, fields: list[str] = [], condition: str = "", needConnect: bool = True):
        """查询数据库中的数据"""
        if (needConnect):
            self.connect()

        self.directExecuteSql(
            f"SELECT {self.__joinFields(fields)} FROM {tableName} {condition}")
        data = self.cursor.fetchall()

        if (needConnect):
            self.close()

        return data

    def __joinFields(self, fields: list[str] = []):
        """拼接字段名"""
        length = len(fields)
        if (length == 0):
            return "*"

        result = ""
        for i in range(length):
            result += fields[i] if i == 0 else ", {0}".format(fields[i])

        return result


DataBaseMgr = __DataBaseMgr()
