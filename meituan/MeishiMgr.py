from __future__ import annotations

import json
from enum import Enum
from typing import Any, Union

from meituan.core.SmtpMgr import SmtpMgr
from meituan.MeituanDBMgr import MeituanDBMgr
from meituan.MeituanMgr import MeituanMgr


class EStateCode(Enum):
    """返回状态码"""

    c200 = "200"    # 成功
    c304 = "304"    # 重定向
    c403 = "403"   # 服务器拒绝提供所请求的资源
    c407 = "407"   # 代理服务器认证要求
    c404 = "404"   # 服务器未知原因


class __MeishiMgr:
    """美团美食管理器"""

    _cityAppState = None

    _baseUri = 'meituan.com/meishi/'

    def __getCityBaseUri(self, cityId: str) -> str:
        return f'{cityId}.{self._baseUri}'

    def __getPoiListUrl(self, cityId: str) -> str:
        return f'{self.__getCityBaseUri(cityId)}api/poi/getPoiList?'

    def __getAppState(self, uri: str) -> tuple[EStateCode, Union[dict, Any]]:
        r = MeituanMgr.request(f'http://{uri}')
        result = r.html.find(
            "script", containing="window._appState", first=True)
        if (result == None):
            htmlContent = str(r.html)
            print(htmlContent)
            code = EStateCode.c404
            # 验证
            if (htmlContent.find("<HTML url='https://verify.meituan.com") >= 0):
                code = EStateCode.c407
            # 服务器错误
            elif (htmlContent.find("<HTML url='https://www.meituan.com/error/") >= 0):
                code = EStateCode.c404
            # 跳转页面
            elif (htmlContent.find("<HTML url='https://www.meituan.com") >= 0):
                code = EStateCode.c304

            return (code, r.html)

        result = result.text
        result = result.replace('window._appState = ', '')
        result = result.replace('};', '}')
        return (EStateCode.c200, json.loads(result))

    def getCityAppState(self, cityId: str):
        if (self._cityAppState == None):
            (code, self._cityAppState) = self.__getAppState(
                self.__getCityBaseUri(cityId))

        return self._cityAppState

    def getPoiAppState(self, cityId: str, poiId: int) -> tuple[EStateCode, Union[dict, Any]]:
        return self.__getAppState(f'{self.__getCityBaseUri(cityId)}{poiId}/')
        # return self.__getAppState(f'{self._baseUri}{poiId}/')

    def getRemotePoiList(self, cityId: str, areaId: str = '0', page: int = 1):
        token = MeituanMgr.createToken(self.__getCityBaseUri(cityId), page)
        params = {
            'cityName': MeituanMgr.getCityName(cityId),
            'cateId': '0',
            'areaId': areaId,
            'sort': '',
            'dinnerCountAttrId': '',
            'page': page,
            'userId': MeituanMgr.userId,
            'uuid': MeituanMgr.uuid,
            'platform': '1',
            'partner': '126',
            'originUrl': self.__getCityBaseUri(cityId) + f'pn{page}/',
            'riskLevel': '1',
            'optimusCode': '10',
            '_token': token
        }

        r = MeituanMgr.request(
            f'http://{self.__getPoiListUrl(cityId)}', params)

        result = json.loads(r.text)
        return result

    def insertAreaData(self, cityId: str):
        """插入指定城市 area 数据"""
        appState = self.getCityAppState(cityId)
        if (appState == None):
            return

        MeituanDBMgr.insertAreaData(cityId, appState)

    def insertPoiListData(self, cityId: str, areaId: str, page: int, needConnect: bool = True):
        """插入 poiList 数据"""
        poiList = MeishiMgr.getRemotePoiList(cityId, areaId, page)
        if (poiList == None):
            return False

        try:
            poiInfos = poiList['data']['poiInfos']
            MeituanDBMgr.insertPoiListData(
                cityId, areaId, poiInfos, needConnect)
            return True
        except:
            print(poiList)
            return False

    def getCampaignPrice(self, dealId: str):
        r = MeituanMgr.request(f'https://{self._baseUri}{dealId}.html')
        return r.html.xpath("//span[@class='campaign-price']", first=True).text


MeishiMgr = __MeishiMgr()
