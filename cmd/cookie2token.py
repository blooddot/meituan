import json


def cookie2json(cookie: str):
    cookieArr = cookie.split(";")
    obj = {}

    for cookie in cookieArr:
        cookieItems = cookie.split(";")
        for cookieItem in cookieItems:
            index = cookieItem.index('=')
            obj[cookieItem[:index].lstrip()] = cookieItem[index+1:].lstrip()

    return json.loads(json.dumps(obj, ensure_ascii=False))


cookie = 'uuid=ac76bdc59c894005841f.1666809046.1.0.0; _lxsdk_cuid=184158e475bc8-0a759f639aa053-26021f51-144000-184158e475bc8; ci=30; _lxsdk_s=184158e475c-694-c3d-8a8%7C%7C5; qruuid=7b271a0f-f5d5-414d-baf2-7e28214577f1; token2=xWS-50nG-Ar8RT76APRLwLQHi8UAAAAAoRQAAC_iwBMjSf3FRXaQFycQizU_qswNWUYQAe3FOp-IyuTiyLHqgopniy_uwiEVG67-4g; oops=xWS-50nG-Ar8RT76APRLwLQHi8UAAAAAoRQAAC_iwBMjSf3FRXaQFycQizU_qswNWUYQAe3FOp-IyuTiyLHqgopniy_uwiEVG67-4g; lt=xWS-50nG-Ar8RT76APRLwLQHi8UAAAAAoRQAAC_iwBMjSf3FRXaQFycQizU_qswNWUYQAe3FOp-IyuTiyLHqgopniy_uwiEVG67-4g; u=265087521; n=%E9%9B%AA%E7%B3%95%E5%95%8A%E5%93%88%E5%93%88; firstTime=1666808985400; unc=%E9%9B%AA%E7%B3%95%E5%95%8A%E5%93%88%E5%93%88'
print(cookie2json(cookie)['token2'])
