import math
import time
from random import random

from meituan.MeishiMgr import MeishiMgr
from meituan.MeituanDBMgr import MeituanDBMgr
from meituan.MeituanMgr import MeituanMgr


def insert():
    pageCount = 15
    cityId = MeituanMgr.cityId
    areaData = MeituanDBMgr.getAreaData(
        'sz', ['areaId', 'name'], 'WHERE subAreas IS NULL AND updatedFlag IS NULL')
    for area in areaData:
        areaId = area[0]
        areaName = area[1]
        try:
            poiList = MeishiMgr.getRemotePoiList(cityId, areaId, 1)
            totalCounts = poiList['data']['totalCounts']
            totalPage = math.ceil(totalCounts/pageCount)
            print(
                f"start insert area:{areaName} areaId:{areaId} totalCounts:{totalCounts} totalPage:{totalPage}")
            MeituanDBMgr.deletePoiData(cityId, areaId)
        except:
            print(poiList)
            return

        for i in range(1, totalPage+1):
            time.sleep(1+random()*2)
            result = MeishiMgr.insertPoiListData('sz', areaId, i)
            if (result == False):
                return

        poiCounts = MeituanDBMgr.getPoiCounts(MeituanMgr.cityId, str(areaId))

        print(
            f"success insert area:{areaName} areaId:{areaId} poiCounts:{poiCounts}")
        MeituanDBMgr.updateAreaPoiCounts(cityId, areaId, totalCounts)
        MeituanDBMgr.updateAreaTime('sz', areaId)


insert()
