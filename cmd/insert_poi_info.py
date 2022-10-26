import time
from random import random
from typing import Any

from meituan.core.DataBaseMgr import DataBaseMgr
from meituan.core.RequestMgr import RequestMgr
from meituan.core.SmtpMgr import SmtpMgr
from meituan.MeishiMgr import EStateCode, MeishiMgr
from meituan.MeituanDBMgr import MeituanDBMgr
from meituan.MeituanMgr import MeituanMgr

cityId = MeituanMgr.cityId


def insertPoiInfo(cityId: str, poiId: int, needConnect: bool = True) -> tuple[EStateCode, Any]:
    (code, poiAppState) = MeishiMgr.getPoiAppState(cityId, poiId)
    if (code != EStateCode.c200):
        return (code, poiAppState)

    deals: list[int] = []
    dealList = poiAppState['dealList']
    for deal in dealList["deals"]:
        deals.append(deal["id"])
        MeituanDBMgr.insertDealData(cityId, poiId, 1, deal, needConnect)

    for voucher in dealList["vouchers"]:
        deals.append(voucher["id"])
        MeituanDBMgr.insertDealData(cityId, poiId, 2, voucher, needConnect)

    MeituanDBMgr.updatePoiData(
        cityId,
        poiId,
        poiAppState["detailInfo"],
        poiAppState["photos"],
        poiAppState["recommended"],
        poiAppState["crumbNav"],
        poiAppState["prefer"],
        deals,
        needConnect
    )

    return (code, None)


def insert(needConnect: bool = False):
    if (needConnect == False):
        DataBaseMgr.connect()

    poiList = MeituanDBMgr.getPoiListData(
        cityId, ['id', 'title'], 'WHERE dealUpdatedFlag IS NULL', needConnect)
    for poiData in poiList:
        poiId = poiData[0]
        title = poiData[1]
        print(f"start insert poiId:{poiId} title:{title}")
        (code, content) = insertPoiInfo(cityId, poiId, needConnect)
        subject = f"{code.value} insert poiId:{poiId} title:{title}"
        print(subject)
        if (code == EStateCode.c304):
            MeituanDBMgr.updatePoiDealUpdatedFlag(cityId, poiId, True)
            insert()
            return

        if (code == EStateCode.c407):
            SmtpMgr.sendMail(subject, str(content))
            time.sleep(60)
            insert()
            return

        if (code != EStateCode.c200):
            SmtpMgr.sendMail(subject, str(content))
            return

        time.sleep(2+random()*3)

    if (needConnect == False):
        DataBaseMgr.close()


insert()
# r = RequestMgr.get('http://sz.meituan.com/meishi/591527/')
# print(r.html)

# poiIdList = MeituanDBMgr.getPoiListData(cityId, ['id'], 'WHERE dealUpdatedFlag IS NULL')
# insertPoiInfo(11001)
# insertPoiInfo(11002)
# insertPoiInfo(11003)
