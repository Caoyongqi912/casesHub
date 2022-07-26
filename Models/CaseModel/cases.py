# @Time : 2022/7/10 21:17 
# @Author : cyq
# @File : cases.py 
# @Software: PyCharm
# @Desc: 用例实体
import json
from typing import AnyStr, Dict, List, Any
from flask import g

from Comment.myException import ParamException
from Enums.errorCode import ResponseMsg
from Models.base import Base
from App import db
from Utils.myLog import MyLog
from Utils.myWraps import simpleBug

log = MyLog.get_log(__file__)


class CasePart(Base):
    __tablename__ = 'case_part'
    partName = db.Column(db.String(20), comment="用例模块")
    productID = db.Column(db.INTEGER, db.ForeignKey("product.id"), nullable=True, comment="所属产品")

    def __init__(self, partName: AnyStr, productID: int):
        self.partName = partName
        self.productID = productID

    def __repr__(self):
        return f"<{CasePart.__name__} {self.part}>"


class Cases(Base):
    __tablename__ = "cases"
    part = db.Column(db.String(20), comment="模块")
    title = db.Column(db.String(20), unique=True, nullable=False, comment="用例名称")
    desc = db.Column(db.String(100), nullable=False, comment="用例描述")
    creator = db.Column(db.INTEGER, nullable=False, comment="创建人")
    steps = db.Column(db.JSON, nullable=False, comment="用例步骤")
    status = db.Column(db.Enum("QUEUE", "TESTING", "BLOCK", "SKIP", "PASS", "FAIL", "CLOSE"), server_default="QUEUE",
                       comment="状态")
    platform = db.Column(db.Enum("IOS", "ANDROID", "WEB", "PC", "APP"), server_default="IOS", comment="所属平台")

    case_level = db.Column(db.Enum('P1', 'P2', 'P3', 'P4'), server_default='P1', comment="用例等级")
    case_type = db.Column(db.Enum('功能', '接口', '性能'), server_default='功能', comment="用例类型")

    prd = db.Column(db.String(200), nullable=False, comment="需求链接")

    updater = db.Column(db.INTEGER, nullable=True, comment="修改人")
    mark = db.Column(db.String(100), nullable=True, comment="用例备注")
    versionID = db.Column(db.INTEGER, db.ForeignKey('version.id'), comment="所属版本")
    productID = db.Column(db.INTEGER, db.ForeignKey("product.id"), nullable=True, comment="所属产品")

    from .bugs import Bug
    bug = db.relationship("Bug", backref="bugs", lazy="dynamic")

    def __init__(self, part: AnyStr, title: AnyStr, desc: AnyStr, steps: List[Dict], prd: AnyStr, platform: AnyStr,
                 status: AnyStr,
                 versionID: int, productID: int, case_level: AnyStr, case_type: AnyStr = None, creator: int = None):
        self.part = part
        self.title = title
        self.creator = creator if creator else g.user.id
        self.desc = desc
        self.prd = prd
        self.platform = platform
        self.productID = productID
        self.versionID = versionID
        self.case_type = case_type
        self.case_level = case_level
        self.status = status
        self.steps = self.__verify_steps(steps)

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
    def __verify_steps(steps: List[Dict]) -> json:
        """
        校验steps格式  并按照 step 排序
        [
        {
            "step":1, *
            "setup": "im setup" | null,
            "do": "to do ...", *
            "exp": "exp ....", *

        },
        {
            "step":2,
            "setup": "im setup" | null,
            "do": "to do ...",
            "exp": "exp ....",

        }
        ]
        :param steps: ↑
        :return:
        :raise: ParamErr
        """
        for step in steps:
            if not step.get("step"):
                raise ParamException(ResponseMsg.miss("step"))
            if not step.get("setup"):
                step.setdefault('setup', None)
            if not step.get("do"):
                raise ParamException(ResponseMsg.miss("do"))
            if not step.get("exp"):
                raise ParamException(ResponseMsg.miss("exp"))
        steps.sort(key=lambda s: s['step'])
        return steps

    def __repr__(self):
        return f"<{Cases.__name__} {self.name}>"
