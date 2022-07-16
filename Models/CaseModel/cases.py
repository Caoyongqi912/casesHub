# @Time : 2022/7/10 21:17 
# @Author : cyq
# @File : cases.py 
# @Software: PyCharm
# @Desc: 用例实体
from typing import AnyStr, Dict
from flask import g

from Models.base import Base
from App import db
from Utils.myLog import MyLog

log = MyLog.get_log(__file__)


class Cases(Base):
    __tablename__ = "cases"
    title = db.Column(db.String(20), unique=True, nullable=False, comment="用例名称")
    desc = db.Column(db.String(100), nullable=False, comment="用例描述")
    creator = db.Column(db.INTEGER, nullable=False, comment="创建人")
    steps = db.Column(db.JSON, nullable=False, comment="用例步骤")
    exp = db.Column(db.String(100), nullable=False, comment="用例预期")
    level = db.Column(db.Enum("P1", "P2", "P3", "P4"), server_default="P1", comment="用例等级")
    prd = db.Column(db.String(200), nullable=False, comment="需求链接")

    updater = db.Column(db.INTEGER, nullable=True, comment="修改人")
    setup = db.Column(db.String(100), nullable=True, comment="用例前置")
    res = db.Column(db.String(100), nullable=True, comment="用例实际")
    # show_type = db.Column(db.Enum(1, 2, 3), server_default=1, comment="用例等级")  # 1 excel # xmind # normal
    case_type = db.Column(db.Enum(1, 2, 3), server_default=1, comment="用例等级")  # 1 功能 2 接口 3 性能
    mark = db.Column(db.String(100), nullable=True, comment="用例备注")

    platformID = db.Column(db.INTEGER, db.ForeignKey('platform.id'), comment="所属平台")

    versionID = db.Column(db.INTEGER, db.ForeignKey('version.id'), comment="所属版本")

    productID = db.Column(db.INTEGER, db.ForeignKey("product.id"), nullable=True, comment="所属产品")

    # bugID = db.Column(db.INTEGER, db.ForeignKey("bug.id"), nullable=True, comment="bug")
    bug = db.relationship("Bug", backref="cases", lazy="dynamic")

    def __init__(self, title: AnyStr, desc: AnyStr, steps: Dict, case_type: int, prd: AnyStr, platformID: int,
                 versionID: int, exp: AnyStr, productID: int,
                 setup: AnyStr = None, level: AnyStr = None):
        self.title = title,
        self.creator = g.user.id
        self.desc = desc,
        self.steps = steps,
        self.case_type = case_type,
        self.prd = prd,
        self.productID = productID
        self.platformID = platformID
        self.versionID = versionID
        self.exp = exp
        self.setup = setup
        self.level = level
