# @Time : 2022/7/10 22:20 
# @Author : cyq
# @File : reports.py 
# @Software: PyCharm
# @Desc: 报告实体
from typing import AnyStr, List, Dict
from Models.base import Base
from App import db
from Utils import MyLog

log = MyLog.get_log(__file__)


class Report(Base):
    __tablename__ = "report"
    title = db.Column(db.String(20), unique=True, comment="名称")
    desc = db.Column(db.String(100), comment="描述")
    version = db.Column(db.String(40), comment="版本")
    status = db.Column(db.Enum("RELEASE", "UNRELEASE"), server_default="UNRELEASE", comment="发布状态")
    online = db.Column(db.String(20), comment="上线时间")
    players = db.Column(db.JSON, nullable=True, comment="参与人")
    bugs = db.Column(db.JSON, nullable=True, comment="bug")
    demands = db.Column(db.JSON, nullable=True, comment="需求链接")

    def __init__(self, title: AnyStr, version: AnyStr, desc: AnyStr, status: AnyStr, online: AnyStr,
                 players: List[Dict] = None, bugs: List[Dict] = None, demands: List[Dict] = None):
        self.title = title
        self.desc = desc
        self.online = online
        self.version = version
        self.status = status
        self.players = players
        self.bugs = bugs
        self.demands = demands

    def __repr__(self):
        return f"<{Report.__name__} {self.title}>"
