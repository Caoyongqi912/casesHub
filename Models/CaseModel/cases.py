# @Time : 2022/7/10 21:17 
# @Author : cyq
# @File : cases.py 
# @Software: PyCharm
# @Desc: 用例实体
import json
from typing import AnyStr, Dict, List, Any
from Comment import ParamException
from Enums import ResponseMsg
from Models.base import Base
from App import db
from Utils import MyLog,simpleBug

from flask import g

log = MyLog.get_log(__file__)


class CasePart(Base):
    __tablename__ = 'case_part'
    partName = db.Column(db.String(20), comment="用例模块")

    # 用例模块与产品是多对一关系
    productID = db.Column(db.INTEGER, db.ForeignKey("product.id"), nullable=True, comment="所属产品")
    # 模块与用例是一对多关系
    cases = db.relationship("Cases", backref='case_part', lazy='dynamic')

    def __init__(self, partName: AnyStr, productID: int):
        self.partName = partName
        self.productID = productID

    def __repr__(self):
        return f"<{CasePart.__name__} {self.part}>"


class Cases(Base):
    __tablename__ = "cases"
    title = db.Column(db.String(20), nullable=False, comment="用例名称")
    tag = db.Column(db.Enum('常规', '冒烟'), server_default='常规', comment="用例标签")
    desc = db.Column(db.String(100), nullable=False, comment="用例描述")
    case_level = db.Column(db.Enum('P1', 'P2', 'P3', 'P4'), comment="用例等级")
    # 暂时全是功能用例 、接口性能未定义
    case_type = db.Column(db.Enum('功能', '接口', '性能'), server_default='功能', comment="用例类型")
    status = db.Column(db.Enum("QUEUE", "TESTING", "BLOCK", "SKIP", "PASS", "FAIL", "CLOSE"), server_default="QUEUE",
                       comment="用例状态")
    setup = db.Column(db.String(40), nullable=True, comment='用例前置')
    info = db.Column(db.JSON, nullable=False, comment="用例步骤与预期结果")
    mark = db.Column(db.String(100), nullable=True, comment="用例备注")

    # case 与 模块 属于多对一 关系
    partID = db.Column(db.INTEGER, db.ForeignKey('case_part.id', ondelete='SET NULL'), nullable=True, comment="模块")
    # case 与 product 是多对一关系 、产品删除、用例productID 置为null
    productID = db.Column(db.INTEGER, db.ForeignKey("product.id", ondelete="SET NULL"), nullable=True, comment="所属产品")
    # case与platform 是多对一关系、平台删除、字段置为空、可无平台
    platformID = db.Column(db.INTEGER, db.ForeignKey('platform.id', ondelete="SET NUll"), nullable=True, comment="所属平台")
    # bug 与 用例是一对多关系
    bugs = db.relationship("Bug", backref="case", lazy="dynamic")

    creator = db.Column(db.INTEGER, nullable=False, comment="创建人")
    updater = db.Column(db.INTEGER, nullable=True, comment="修改人")

    def __init__(self, title: AnyStr, desc: AnyStr, info: List[Dict], tag: Any = None,
                 case_level: AnyStr = "QUEUE", case_type: AnyStr = None,
                 status: AnyStr = None, setup: AnyStr = None, mark: AnyStr = None, partID: int = None,
                 productID: int = None,
                 platformID: int = None):
        self.title = title
        self.desc = desc
        self.creator = g.user.id
        self.status = status
        self.productID = productID
        self.platformID = platformID
        self.partID = partID
        self.case_type = case_type
        self.case_level = case_level
        self.setup = setup
        self.mark = mark
        self.tag = tag
        self.info = self.__verify_info(info)

    @property
    @simpleBug
    def bugs(self):
        """
        获取所有bug
        :return: Pagination
        """
        return self.bug.all()

    @classmethod
    def update(cls, **kwargs):
        """
        case 更新 重写父类 不需要校验用户。
        :param kwargs:0
        :return:
        """
        from flask import g
        kwargs.setdefault("updater", g.user.id)  # 修改人
        return super(Cases, Cases).update(**kwargs)

    @staticmethod
    def __verify_info(info: List[Dict]) -> json:
        """
        校验steps格式  并按照 step 排序
        [
        {
            "step":1, *
            "do": "to do ...", *
            "exp": "exp ....", *

        },
        {
            "step":2,
            "do": "to do ...",
            "exp": "exp ....",

        }
        ]
        :param info: ↑
        :return:
        :raise: ParamErr
        """
        for step in info:
            if not step.get("step"):
                raise ParamException(ResponseMsg.miss("step"))
            if not step.get("do"):
                raise ParamException(ResponseMsg.miss("do"))
            if not step.get("exp"):
                raise ParamException(ResponseMsg.miss("exp"))
        info.sort(key=lambda s: s['step'])
        return info

    def __repr__(self):
        return f"<{Cases.__name__} {self.name}>"
