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

log = MyLog.get_log(__file__)


class Cases(Base):
    __tablename__ = "cases"
    title = db.Column(db.String(20), unique=True, nullable=False, comment="用例名称")
    desc = db.Column(db.String(100), nullable=False, comment="用例描述")
    creator = db.Column(db.INTEGER, nullable=False, comment="创建人")
    steps = db.Column(db.JSON, nullable=False, comment="用例步骤")

    case_level = db.Column(db.Enum('P1', 'P2', 'P3', 'P4'), server_default='P1', comment="用例等级")
    case_type = db.Column(db.Enum('功能', '接口', '性能'), server_default='功能', comment="用例类型")

    prd = db.Column(db.String(200), nullable=False, comment="需求链接")

    updater = db.Column(db.INTEGER, nullable=True, comment="修改人")
    mark = db.Column(db.String(100), nullable=True, comment="用例备注")

    platformID = db.Column(db.INTEGER, db.ForeignKey('platform.id'), comment="所属平台")
    versionID = db.Column(db.INTEGER, db.ForeignKey('version.id'), comment="所属版本")
    productID = db.Column(db.INTEGER, db.ForeignKey("product.id"), nullable=True, comment="所属产品")

    from .bugs import Bug
    bug = db.relationship("Bug", backref="bugs", lazy="dynamic")

    def __init__(self, title: AnyStr, desc: AnyStr, steps: List[Dict], prd: AnyStr, platformID: int,
                 versionID: int, productID: int, case_level: AnyStr, case_type: AnyStr = None):
        self.title = title,
        self.creator = g.user.id
        self.desc = desc,
        self.prd = prd,
        self.productID = productID
        self.platformID = platformID
        self.versionID = versionID
        self.case_type = case_type
        self.case_level = case_level
        self.steps = self.__verify_steps(steps)


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
