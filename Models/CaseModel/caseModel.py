# @Time : 2022/7/10 21:17 
# @Author : cyq
# @File : caseModel.py
# @Software: PyCharm
# @Desc: 用例实体
import json
from typing import AnyStr, Dict, List, Any, Optional
from Comment.myException import ParamException
from Enums import CaseLevel, CaseTag, CaseType, CaseStatus, IntEnum, EnumDict
from Enums import ResponseMsg
from Models.base import Base
from App import db
from Utils import MyLog, simpleBug

from flask import g

log = MyLog.get_log(__file__)


class Cases(Base):
    __tablename__ = "cases"
    title = db.Column(db.String(20), nullable=False, comment="用例名称")
    desc = db.Column(db.String(100), nullable=False, comment="用例描述")

    tag = db.Column(IntEnum(CaseTag), comment="用例标签")
    case_level = db.Column(IntEnum(CaseLevel), comment="用例等级")
    case_type = db.Column(IntEnum(CaseType), comment="用例类型")

    setup = db.Column(db.String(40), nullable=True, comment='用例前置')
    info = db.Column(db.JSON, nullable=False, comment="用例步骤与预期结果")
    mark = db.Column(db.String(100), nullable=True, comment="用例备注")

    # case 与 模块 属于多对一 关系
    partID = db.Column(db.INTEGER, db.ForeignKey('case_part.id', ondelete='SET NULL'), nullable=True, comment="模块")
    # case 与 product 是多对一关系 、产品删除、用例productID 置为null
    projectID = db.Column(db.INTEGER, db.ForeignKey("project.id", ondelete="SET NULL"), nullable=True,
                          comment="所属产品")
    # case与platform 是多对一关系、平台删除、字段置为空、可无平台
    platformID = db.Column(db.INTEGER, db.ForeignKey('platform.id', ondelete="SET NUll"), nullable=True,
                           comment="所属平台")
    # version yu case 是1vn
    versionID = db.Column(db.INTEGER, db.ForeignKey('version.id', ondelete='SET NUll'), nullable=True,
                          comment="所属版本")

    # bug 与 用例是一对多关系
    bugs = db.relationship("Bug", backref="case", lazy="dynamic")
    creator = db.Column(db.INTEGER, nullable=False, comment="创建人")
    updater = db.Column(db.INTEGER, nullable=True, comment="修改人")

    def __init__(self, title: AnyStr, desc: AnyStr, info: List[Dict], tag: CaseTag = CaseTag.COMMENT,
                 case_level: CaseLevel = CaseLevel.P4, case_type: CaseType = CaseType.COMMENT,
                 status: CaseStatus = CaseStatus.QUEUE, setup: Optional[str] = None, mark: Optional[str] = None,
                 partID: Optional[int] = None,
                 projectID: Optional[int] = None,
                 platformID: Optional[int] = None,
                 creator: int = None,
                 versionID: Optional[int] = None):
        self.title = title
        self.desc = desc
        self.creator = creator if creator else g.user.id
        self.status = status
        self.projectID = projectID
        self.platformID = platformID
        self.versionID = versionID
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

    @staticmethod
    def column2Enum(col: Dict[str, Any]) -> Dict[str, Any]:
        """
        枚举类型转化
        :param col:{"case_type":"COMMENT","case_level":"P1"...}
        :return: {"case_type":1","case_level":1...}
        """
        from copy import deepcopy
        dk = deepcopy(col)
        for k, v in dk.items():
            col[k] = EnumDict[k].getValue(v)
        return col

    def __repr__(self):
        return f"<{Cases.__name__} {self.name}>"
