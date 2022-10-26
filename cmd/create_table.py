import json

from meituan.MeituanDBMgr import MeituanDBMgr

# MeituanDBMgr.createAreaTable('sz')
# MeituanDBMgr.createPoiTable('sz')
# MeituanDBMgr.createDealTable('sz')

# value = [{"title": "招牌小炒双人餐，提供免费WiFi", "price": 108, "soldCounts": 0}, {"title": "羊肉煲一份、配菜生菜1/茼蒿（二选一）、 土豆片1、 金针菇1、 鲜鱿1/虾1 （二选一）、莴笋1、 啤酒2支/饮料1'支（二选一）1份", "price": 268, "soldCounts": 0}, {"title": "羊肉煲一份、配菜淮山1、  腐竹皮1、 白萝卜/莴笋(二选一)1、 沙白1、 猪肉丸1/牛肉丸(二选一)、  啤酒2支/饮料1支(二选一)1份", "price": 258, "soldCounts": 0}, {
#     "title": "羊肉煲一份、 配菜莲藕1 /土豆片1(二选一)、茼蒿1/ 波菜1（二选一）、肥牛卷1、 牛肉丸1、 蟹柳1、腐竹皮1、白菜11份", "price": 458, "soldCounts": 0}, {"title": "双人砂锅粥套餐，提供免费WiFi", "price": 86, "soldCounts": 0}, {"title": "四人砂锅粥套餐，提供免费WiFi", "price": 188, "soldCounts": 0}]
# value = json.dumps(value, ensure_ascii=False).replace("'", "\\'")
# # value = f"""'{value}'"""

# print(value)
