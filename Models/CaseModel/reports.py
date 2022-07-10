# @Time : 2022/7/10 22:20 
# @Author : cyq
# @File : reports.py 
# @Software: PyCharm
# @Desc: 报告实体
from Models.base import Base
from App import db
from Utils.log import MyLog

log = MyLog.get_log(__file__)


class Report(Base):
    __tablename__ = "report"
    name = db.Column(db.String(20), unique=True, comment="名称")
    desc = db.Column(db.String(100), nullable=True, comment="描述")
    status = db.Column(db.Enum("RELEASE", "UNRELEASE"), server_default="UNRELEASE", comment="发布状态")
    players = db.Column(db.JSON, nullable=True, comment="参与人")
    bugs = db.Column(db.JSON, nullable=True, comment="bug")
    demand = db.Column(db.JSON, nullable=True, comment="需求链接")
