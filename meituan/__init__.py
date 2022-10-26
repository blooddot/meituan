# coding:utf8
__version__ = "0.0.1"
__author__ = "blooddot"
__name__ = "meituan"
# import logging
from warnings import simplefilter

import pymysql
import sqlalchemy
import xalpha

simplefilter(action='ignore', category=FutureWarning)   # 忽略警告

pymysql.install_as_MySQLdb()

engine = sqlalchemy.create_engine(
    'mysql://root@127.0.0.1/xalpha?charset=utf8')
xalpha.set_backend(backend="sql", path=engine)  # 设置合适的本地化方案，也可不设，则数据仅会缓存在内存中

# logger = logging.getLogger('xalpha')
# logger.setLevel(logging.DEBUG)
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)
# logger.addHandler(ch)
