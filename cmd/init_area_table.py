from meituan.MeishiMgr import MeishiMgr
from meituan.MeituanDBMgr import MeituanDBMgr

MeituanDBMgr.createAreaTable('sz')
MeishiMgr.insertAreaData('sz')
