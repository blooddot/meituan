from __future__ import annotations

import math
from datetime import datetime

from meituan.core.DataBaseMgr import DataBaseMgr


class __MeituanDBMgr:
    """美团数据库管理器"""

    def __getAreaTableName(self, cityId: str) -> str:
        return f"{cityId}_area"

    def createAreaTable(self, cityId: str):
        """创建指定城市 area 表"""
        tableName = self.__getAreaTableName(cityId)
        DataBaseMgr.executeSql(
            f"""CREATE TABLE IF NOT EXISTS {tableName} (
                    id INT NOT NULL AUTO_INCREMENT,
                    areaId CHAR(15) unique,
                    name CHAR(15),
                    subAreas VARCHAR(500),
                    poiCounts INT,
                    updateTime DOUBLE,
                    updatedFlag BOOL,
                    PRIMARY KEY(id))""",
        )
        return tableName

    def insertAreaData(self, cityId: str, appState: dict, needConnect: bool = True):
        """插入指定城市 area 数据"""
        tableName = self.__getAreaTableName(cityId)
        for area in appState['filters']['areas']:
            areaId = area['id']
            subAreas = ''
            for subArea in area['subAreas']:
                subAreaId = subArea['id']
                if (subAreaId != areaId):
                    subAreas += f'{subAreaId},'
                    DataBaseMgr.insertData(
                        tableName,
                        [
                            ("areaId", str(subAreaId)),
                            ("name", subArea['name'])
                        ]
                    )

            DataBaseMgr.insertData(
                tableName,
                [
                    ("areaId", str(areaId)),
                    ("name", area['name']),
                    ("subAreas", str(subAreas))
                ],
                "",
                needConnect
            )

    def updateAreaTime(self, cityId: str, areaId: str):
        """更新 area 数据"""
        tableName = self.__getAreaTableName(cityId)
        DataBaseMgr.executeSql(
            f"""UPDATE {tableName} SET updateTime = {datetime.now().timestamp()}, updatedFlag = TRUE WHERE areaId = {areaId}""",
        )

    def updateAreaPoiCounts(self, cityId: str, areaId: str, poiCounts: int):
        """更新 area poiCounts 数据"""
        tableName = self.__getAreaTableName(cityId)
        DataBaseMgr.updateData(tableName, [(
            "poiCounts", poiCounts)], f"WHERE areaId = {areaId}")

    def getAreaData(self, cityId: str, fields: list[str] = [], condition: str = "") -> tuple[list[str | int]]:
        """获取指定城市 area 数据"""
        tableName = self.__getAreaTableName(cityId)
        return DataBaseMgr.fetchData(tableName, fields, condition)

    def __getPoiTableName(self, cityId: str) -> str:
        return f"{cityId}_poi"

    def createPoiTable(self, cityId: str):
        """创建 poi 表"""
        tableName = self.__getPoiTableName(cityId)
        DataBaseMgr.executeSql(
            f"""CREATE TABLE IF NOT EXISTS {tableName} (
                    id INT,
                    areaId CHAR(15),
                    title VARCHAR(200),
                    avgScore DOUBLE,
                    address CHAR(100),
                    phone CHAR(30),
                    openTime VARCHAR(500),
                    extraInfos TEXT,
                    hasFoodSafeInfo BOOL,
                    longitude DOUBLE,
                    latitude DOUBLE,
                    avgPrice DOUBLE,
                    brandId INT,
                    brandName VARCHAR(100),
                    showStatus INT,
                    isMeishi BOOL,
                    photos TEXT,
                    recommended TEXT,
                    crumbNav TEXT,
                    prefer TEXT,
                    dealList TEXT,
                    deals VARCHAR(500),
                    allCommentNum DOUBLE,
                    updateTime DOUBLE,
                    dealUpdateTime DOUBLE,
                    dealUpdatedFlag BOOL,
                    PRIMARY KEY(id))""",
        )
        return tableName

    def insertPoiListData(self, cityId: str, areaId: str, poiInfos: list, needConnect: bool = True):
        """替换 poiList 数据"""
        tableName = self.__getPoiTableName(cityId)
        for poiInfo in poiInfos:
            DataBaseMgr.insertData(
                tableName,
                [
                    ("id", str(poiInfo['poiId'])),
                    ("areaId", areaId),
                    ("title", poiInfo['title']),
                    ("avgScore", str(poiInfo['avgScore'])),
                    ("allCommentNum", str(poiInfo['allCommentNum'])),
                    ("address", str(poiInfo['address'])),
                    ("avgPrice", str(poiInfo['avgPrice'])),
                    ("dealList", poiInfo["dealList"]),
                    ("updateTime", datetime.now().timestamp()),
                ],
                "",
                needConnect
            )

    def getPoiListData(self, cityId: str, fields: list[str] = [], condition: str = "", needConnect: bool = True) -> list[list]:
        """获取指定城市 poiList 数据"""
        tableName = self.__getPoiTableName(cityId)
        data = DataBaseMgr.fetchData(
            tableName, fields, condition, needConnect)

        if (len(data[0]) == 0):
            return []

        return data

    def updatePoiData(self, cityId: str, poiId: int, detailInfo: dict, photos: dict, recommended: list, crumbNav: list, prefer: list, deals: list[int],  needConnect: bool = True):
        """更新 poi 数据"""
        tableName = self.__getPoiTableName(cityId)
        DataBaseMgr.updateData(
            tableName,
            [
                ("address", detailInfo["address"]),
                ("phone", detailInfo["phone"]),
                ("openTime", detailInfo["openTime"]),
                ("extraInfos", detailInfo["extraInfos"]),
                ("hasFoodSafeInfo", detailInfo["hasFoodSafeInfo"]),
                ("longitude", detailInfo["longitude"]),
                ("latitude", detailInfo["latitude"]),
                ("avgPrice", detailInfo["avgPrice"]),
                ("brandId", detailInfo["brandId"]),
                ("brandName", detailInfo["brandName"]),
                ("showStatus", detailInfo["showStatus"]),
                ("isMeishi", detailInfo["isMeishi"]),
                ("photos", photos),
                ("recommended", recommended),
                ("crumbNav", crumbNav),
                ("prefer", prefer),
                ("deals", deals),
                ("dealUpdateTime", datetime.now().timestamp()),
                ("dealUpdatedFlag", True)
            ],
            f"WHERE id = {poiId}",
            needConnect
        )

    def updatePoiDealUpdatedFlag(self, cityId: str, poiId: int, value: bool, needConnect: bool = True):
        """更新 poi dealUpdatedFlag 数据"""
        tableName = self.__getPoiTableName(cityId)
        DataBaseMgr.updateData(
            tableName,
            [
                ("dealUpdatedFlag", value)
            ],
            f"WHERE id = {poiId}",
            needConnect
        )

    def getPoiCounts(self, cityId: str, areaId: str):
        tableName = self.__getPoiTableName(cityId)
        data = DataBaseMgr.fetchData(tableName, [
            'COUNT(*)'], f'WHERE areaId={areaId}')
        if (len(data[0]) == 0):
            return 0

        return data[0][0]

    def deletePoiData(self, cityId: str, areaId: str):
        """删除指定 poi 数据"""
        tableName = self.__getPoiTableName(cityId)
        DataBaseMgr.executeSql(
            f"""DELETE FROM {tableName} WHERE areaId = {areaId}""")

    def __getDealTableName(self, cityId: str) -> str:
        return f"{cityId}_deal"

    def createDealTable(self, cityId: str):
        """创建 deal 表"""
        tableName = self.__getDealTableName(cityId)
        DataBaseMgr.executeSql(
            f"""CREATE TABLE IF NOT EXISTS {tableName} (
                    id INT,
                    poiId TEXT,
                    type INT,
                    frontImgUrl VARCHAR(500),
                    title VARCHAR(200),
                    soldNum INT,
                    price DOUBLE,
                    value DOUBLE,
                    campaignPrice DOUBLE,
                    discount DOUBLE,
                    updateTime DOUBLE,
                    PRIMARY KEY(id))""",
        )
        return tableName

    def insertDealData(self, cityId: str, poiId: int, type: int, deal: dict, needConnect: bool = True):
        tableName = self.__getDealTableName(cityId)
        DataBaseMgr.insertData(
            tableName,
            [
                ("id", deal["id"]),
                ("poiId", poiId),
                ("type", type),
                ("frontImgUrl", deal["frontImgUrl"]),
                ("title", deal["title"]),
                ("soldNum", deal["soldNum"]),
                ("price", deal["price"]),
                ("value", deal["value"]),
                ("discount", math.ceil(deal["price"]/deal["value"]*100)/100),
                ("updateTime", datetime.now().timestamp()),
            ],
            f"ON DUPLICATE KEY UPDATE poiId = concat(poiId,',{poiId}'), updateTime = {datetime.now().timestamp()}",
            needConnect
        )


MeituanDBMgr = __MeituanDBMgr()
