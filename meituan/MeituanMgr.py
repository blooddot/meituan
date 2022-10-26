import base64
import json
import zlib
from datetime import datetime

from meituan.core.RequestMgr import RequestMgr


class __MeituanMgr:
    typeDict = {
        '代金券': '393', '蛋糕甜点': '11', '火锅': '17', '自助餐': '40', '川菜': '30', '湘菜': '510', '小吃快餐': '36',
        '其他美食': '24', '日韩料理': '28', '东北菜': '20003', '聚餐宴请': '395', '西餐': '35', '香锅烤鱼': '20004',
        '烧烤烤肉': '54', '江浙菜': '56', '中式烧烤/烤串': '400', '粤菜': '57', '咖啡酒吧': '41', '西北菜': '58', '京菜鲁菜': '59',
        '云贵菜': '60', '东南亚菜': '62', '海鲜': '63', '素食': '217', '台湾/客家菜': '227', '创意菜': '228', '汤/粥/炖菜': '229',
        '蒙餐': '232', '新疆菜': '233'
    }

    # 热门城市，城市太多，懒得全加上去
    cityDict = {
        'chs': '长沙', 'cd': '成都', 'cq': '重庆', 'hz': '杭州', 'sh': '上海',
        'nj': '南京', 'wh': '武汉', 'bj': '北京', 'gz': '广州', 'sz': '深圳'
    }

    cityId = 'sz'
    cityName = cityDict[cityId]
    userId = '265087521'
    uuid = 'b0076377cb5e418dabcc.1652879170.1.0.0'
    token = 'xWS-50nG-Ar8RT76APRLwLQHi8UAAAAAoRQAAC_iwBMjSf3FRXaQFycQizU_qswNWUYQAe3FOp-IyuTiyLHqgopniy_uwiEVG67-4g'

    __cookies = {
        'uuid': uuid,
        'token2': token,
    }

    def getCityName(self, cityId: str) -> str:
        return self.cityDict[cityId]

    def __createSign(self, baseUrl: str, page: int) -> str:
        url = baseUrl + f'pn{page}/'

        sign = f"areaId=0&cateId=17&cityName={self.cityName}&dinnerCountAttrId=&optimusCode=1&originUrl={url}&page={page}&partner=126&platform=1&riskLevel=1&sort=&userId=&uuid={self.uuid}"
        sign_ = zlib.compress(
            bytes(json.dumps(sign, ensure_ascii=False), encoding='utf-8'))
        return str(base64.b64encode(sign_), encoding='utf-8')

    def createToken(self, baseUrl: str, page: int) -> str:
        sign = self.__createSign(baseUrl, page)
        ts = int(datetime.now().timestamp() * 1000)
        data = {
            'rId': 100900,
            'ver': '1.0.6',
            'ts': ts,
            'cts': ts + 100 * 1000,
            'brVD': [1326, 538],
            'brR': [[1326, 538], [1326, 538], 24, 24],
            'bI': [f"${baseUrl}/pn{page}/", f"${baseUrl}/pn{page-1}/"],
            'mT': [],
            'kT': [],
            'aT': [],
            'tT': [],
            'aM': '',
            'sign': sign
        }
        token_decode = zlib.compress(
            bytes(json.dumps(data, separators=(',', ':'), ensure_ascii=False), encoding="utf8"))
        token = str(base64.b64encode(token_decode), encoding="utf8")
        return token

    def request(self, url: str, params: dict = None):
        return RequestMgr.get(url, cookies=self.__cookies, params=params)


MeituanMgr = __MeituanMgr()
