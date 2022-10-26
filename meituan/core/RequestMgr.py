import json
import math
import random
from time import time
from requests_html import HTMLSession

proxyListUrl = 'http://pubproxy.com/api/proxy?limit=1&format=txt&country=CHN&http=true&https=true&type=http'
MIN_REQUEST_COUNT = 5  # 切换配置的最小请求数量
MAX_REQUEST_COUNT = 20  # 切换配置的最大请求数量

kuaiIntrProxyUrl = 'https://www.kuaidaili.com/free/intr/'
kuaiIntaProxyUrl = 'https://www.kuaidaili.com/free/inha'

# http://www.useragentstring.com/pages/useragentstring.php
USER_AGENTS = [
    "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
    "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
    "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
    "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
    "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
]


class __RequestMgr:
    """请求管理器"""

    __session: HTMLSession
    __proxyMaxCount: int  # 代理最大请求计数
    __proxyCount: int = 0  # 当前代理请求计数
    __proxyList: list[str]
    __proxy: str
    __userAgent: str

    __userAgentMaxCount: int
    __userAgentCount: int = 0

    def __init__(self):
        self.__session = HTMLSession()
        self.__resetUserAgent()
        # self.__initProxyList(kuaiIntrProxyUrl)
        # self.__resetProxy()

    # def __initProxyList(self):
    #     self.__proxyList = []
    #     proxyList: list[str] = self.__session.get(proxyListUrl, headers=self.headers).text.split('\n')
    #     proxyList.pop()  # 移除末尾空字符串值
    #     for url in proxyList:
    #         [valid, anonymity, interval] = self.__getProxyInfo("http://www.baidu.com")
    #         # print(f'{url} {anonymity} {interval}')
    #         if valid:
    #             self.__proxyList.append(url)
    #             # print(f'{url} {anonymity} {interval}')

    #     # print(self.__proxyList)

    def __resetProxy(self):
        self.__proxyCount = 0
        self.__proxyMaxCount = MIN_REQUEST_COUNT + \
            math.floor(random.random()*(MAX_REQUEST_COUNT-MIN_REQUEST_COUNT))
        # proxyList = self.__session.get(proxyListUrl, headers=self.headers).text.split('\n')
        # self.__proxy = proxyList[0]

        self.__proxy = random.choice(self.__proxyList) if len(self.__proxyList) > 0 else None

    def __resetUserAgent(self):
        self.__userAgentCount = 0
        self.__userAgentMaxCount = MIN_REQUEST_COUNT + \
            math.floor(random.random()*(MAX_REQUEST_COUNT-MIN_REQUEST_COUNT))
        self.__userAgent = random.choice(USER_AGENTS)

    # def __getProxyInfo(self, url):
    #     try:
    #         start_point = time()
    #         response = self.__session.get(url, proxies={
    #             'http': f'http://{url}',
    #             'https': f'http://{url}'
    #         }, **{'timeout': 10, 'headers': self.headers})
    #         if response.ok:
    #             interval = round(time() - start_point, 2)
    #             res_json = json.loads(response.text)
    #             ip = res_json['origin']
    #             if ',' in ip:
    #                 anonymity = 'transparent'
    #             else:
    #                 anonymity = 'anonymous'
    #             return True, anonymity, interval
    #         else:
    #             print(response)
    #             return False, False, False
    #     except (Exception,) as e:
    #         print(e)
    #         return False, False, False

    def __initProxyList(self, url: str, page=1):
        self.__proxyList = []
        ip_list = self.__session.get(f'{url}{page}').html.xpath(".//*[@id='list']/table[position()=1]/tbody/tr")

        if not ip_list:
            return []

        for item in ip_list:
            ip = item.xpath('./tr/td[1]')[0].text
            port = item.xpath('./tr/td[2]')[0].text
            self.__proxyList.append(f'{ip}:{port}')

            # 协议
            # protocol = item.xpath('./td[4]')[0].text.lower()

            # proxy = {
            #     'ip': ip,
            #     'port': port,
            #     'anonymity': '',  # anonymous transparent
            #     'protocol': protocol,  # http https http&https
            #     'speed': 0.00
            # }

            # proxyList.append(proxy)

    @ property
    def headers(self):
        """
        模拟浏览器爬取代理 http 头信息
        :return:
        """
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'h-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'Connection': 'close',  # 长连接过多会导致异常,所以取消
            'User-Agent': self.__userAgent
        }

    def get(self, url: str, **kwargs):
        # if(self.__proxyCount >= self.__proxyMaxCount):
        #     self.__resetProxy()

        if(self.__userAgentCount >= self.__userAgentMaxCount):
            self.__resetUserAgent()

        # self.__proxyCount += 1
        self.__userAgentCount += 1
        # self.__proxy = '121.8.215.106:9797'
        # return self.__session.get(url, headers=self.headers, proxies={
        #     'http': f'http://{self.__proxy}'
        # }, timeout=10, **kwargs)
        return self.__session.get(url, headers=self.headers, **kwargs)


RequestMgr = __RequestMgr()
