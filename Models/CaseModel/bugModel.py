# @Time : 2022/7/10 21:55 
# @Author : cyq
# @File : bugModel.py
# @Software: PyCharm
# @Desc: bug实体
from typing import AnyStr

from flask import g

from Enums import BugLevel, BugType, BugStatus
from Enums.myEnum import IntEnum
from Models.base import Base
from App import db
from Utils import MyLog

log = MyLog.get_log(__file__)


class Bug(Base):
    __tablename__ = "bug"
    title = db.Column(db.String(20), comment="bug名称")
    desc = db.Column(db.String(100), nullable=True, comment="bug描述")
    tag = db.Column(db.String(30), nullable=True, comment="bug标签")
    tester = db.Column(db.String(20), nullable=False, comment="测试人")
    developer = db.Column(db.String(20), comment="开发")
    pr = db.Column(db.String(20), comment="产品")

    type = db.Column(IntEnum(BugType), comment='bug类型')
    level = db.Column(IntEnum(BugLevel), comment="BUG等级")
    status = db.Column(IntEnum(BugStatus), comment="BUG状态")

    file = db.Column(db.String(50), nullable=True, comment="附件地址")
    mark = db.Column(db.String(100), nullable=True, comment="BUG备注")
    # bug与platform 是多对一关系、平台删除、字段置为空、可无平台
    platformID = db.Column(db.INTEGER, db.ForeignKey('platform.id', ondelete="SET NUll"), nullable=True, comment="所属平台")
    # bug 与 version 是多对一关系、版本删除、用例删除、无版本为公共用例
    versionID = db.Column(db.INTEGER, db.ForeignKey('version.id', ondelete="SET NULL"), comment="所属版本")
    # bug v case  ==  n v 1
    caseID = db.Column(db.INTEGER, db.ForeignKey("cases.id", ondelete="SET NULL"), comment="所属用例")

    def __init__(self, title: AnyStr, desc: AnyStr, developer: int, pr: int, bug_type: BugType, level: BugLevel,
                 versionID: int, caseID: int,
                 status: BugStatus = BugStatus.OPEN, file: AnyStr = None, mark: AnyStr = None, platformID: int = None,
                 tester: int = None,
                 ):
        self.title = title
        self.desc = desc
        self.developer = developer
        self.pr = pr
        self.type = bug_type
        self.level = level
        self.versionID = versionID
        self.caseID = caseID
        self.status = status
        self.file = file
        self.mark = mark
        self.platformID = platformID
        self.tester = tester if tester else g.user.id

    def __repr__(self):
        return f"<{Bug.__name__} {self.title}>"
