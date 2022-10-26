from meituan.MeishiMgr import MeishiMgr
from meituan.MeituanDBMgr import MeituanDBMgr
from meituan.MeituanMgr import MeituanMgr

areaData = MeituanDBMgr.getAreaData(
    'sz', ['areaId', 'name', 'poiCounts'], 'WHERE subAreas IS NULL')
for area in areaData:
    [areaId, areaName, poiCounts] = area

    if (poiCounts == None):
        continue

    realCounts = MeituanDBMgr.getPoiCounts(MeituanMgr.cityId, str(areaId))

    if (int(poiCounts) != int(realCounts)):
        print(
            f'count error areaName:{areaName} areaId:{areaId} poiCounts:{poiCounts} realCounts:{realCounts} ')


# data = DataBaseMgr.fetchData('sz_poi', ['COUNT(*)'], 'WHERE areaId=745')
# print(data[0][0])

# pageCount = 15
# poiList = MeishiMgr.getPoiList('sz', '757', 1)
# totalCounts = poiList['data']['totalCounts']
# totalPage = math.ceil(totalCounts/pageCount)
# print(f'totalCounts:{totalCounts} totalPage:{totalPage}')
