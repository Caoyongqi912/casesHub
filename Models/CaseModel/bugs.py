# @Time : 2022/7/10 21:55 
# @Author : cyq
# @File : bugs.py 
# @Software: PyCharm
# @Desc: bug实体
from typing import AnyStr

from Models.base import Base
from App import db
from Utils.myLog import MyLog

log = MyLog.get_log(__file__)


class Bug(Base):
    __tablename__ = "bug"
    title = db.Column(db.String(20), unique=True, comment="bug名称")
    desc = db.Column(db.String(100), nullable=True, comment="bug描述")
    tester = db.Column(db.String(20), nullable=False, comment="测试")
    developer = db.Column(db.String(20), nullable=False, comment="测试")
    pr = db.Column(db.String(20), nullable=False, comment="产品")
    level = db.Column(db.Enum("P1", "P2", "P3", "P4"), server_default="P1", comment="BUG等级")
    status = db.Column(db.Enum("OPEN", "CLOSE","BLOCK"), server_default="OPEN", comment="BUG状态")
    file = db.Column(db.String(50), nullable=True, comment="附件地址")
    mark = db.Column(db.String(100), nullable=True, comment="BUG备注")
    caseID = db.Column(db.INTEGER, db.ForeignKey("cases.id"), comment="所属用例")

    def __init__(self, title: AnyStr, desc: AnyStr, tester: int, developer: int, pr: AnyStr, level: AnyStr,
                 status: AnyStr, caseID: int):
        self.title = title
        self.desc = desc
        self.tester = tester
        self.developer = developer
        self.pr = pr
        self.level = level
        self.status = status
        self.caseID = caseID

    def __repr__(self):
        return f"<{Bug.__name__} {self.title}>"
