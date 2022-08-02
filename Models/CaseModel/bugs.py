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
    tag = db.Column(db.String(30), nullable=True, comment="bug标签")
    tester = db.Column(db.String(20), nullable=False, comment="测试人")
    developer = db.Column(db.String(20), nullable=False, comment="开发")
    pr = db.Column(db.String(20), nullable=False, comment="产品")
    bug_type = db.Column(db.Enum('线上问题', '优化', '缺陷'), server_default="缺陷", comment='bug类型')
    level = db.Column(db.Enum("P1", "P2", "P3", "P4"), server_default="P1", comment="BUG等级")
    status = db.Column(db.Enum("OPEN", "CLOSE", "BLOCK"), server_default="OPEN", comment="BUG状态")
    file = db.Column(db.String(50), nullable=True, comment="附件地址")
    mark = db.Column(db.String(100), nullable=True, comment="BUG备注")
    # bug与platform 是多对一关系、平台删除、字段置为空、可无平台
    platformID = db.Column(db.INTEGER, db.ForeignKey('platform.id', ondelete="SET NUll"), nullable=True, comment="所属平台")
    # bug 与 version 是多对一关系、版本删除、用例删除、无版本为公共用例
    versionID = db.Column(db.INTEGER, db.ForeignKey('version.id', ondelete="SET NULL"), nullable=True, comment="所属版本")
    # bug v case  ==  n v 1
    caseID = db.Column(db.INTEGER, db.ForeignKey("cases.id", ondelete="SET NULL"), comment="所属用例")



    def __repr__(self):
        return f"<{Bug.__name__} {self.title}>"
