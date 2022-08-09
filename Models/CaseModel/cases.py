# @Time : 2022/7/10 21:17 
# @Author : cyq
# @File : cases.py 
# @Software: PyCharm
# @Desc: 用例实体
import json
from typing import AnyStr, Dict, List, Any, Optional
from Comment.myException import ParamException
from Enums.myEnum import CaseLevel, CaseTag, CaseType, CaseStatus, IntEnum
from Enums.errorCode import ResponseMsg
from Models.base import Base
from App import db
from Utils import MyLog, simpleBug

from flask import g

log = MyLog.get_log(__file__)


class CasePart(Base):
    __tablename__ = 'case_part'
    partName = db.Column(db.String(20), unique=True, comment="用例模块")

    # 用例模块与产品是多对一关系
    projectID = db.Column(db.INTEGER, db.ForeignKey("project.id"), nullable=True, comment="所属产品")
    # 模块与用例是一对多关系
    cases = db.relationship("Cases", backref='case_part', lazy='dynamic')

    def __init__(self, partName: AnyStr, projectID: int):
        self.partName = partName
        self.projectID = projectID

    def __repr__(self):
        return f"<{CasePart.__name__} {self.part}>"


class Cases(Base):
    __tablename__ = "cases"
    title = db.Column(db.String(20), nullable=False, comment="用例名称")
    desc = db.Column(db.String(100), nullable=False, comment="用例描述")

    tag = db.Column(IntEnum(CaseTag), comment="用例标签")
    case_level = db.Column(IntEnum(CaseLevel), comment="用例等级")
    case_type = db.Column(IntEnum(CaseType), comment="用例类型")
    status = db.Column(IntEnum(CaseStatus), comment="用例状态")

    setup = db.Column(db.String(40), nullable=True, comment='用例前置')
    info = db.Column(db.JSON, nullable=False, comment="用例步骤与预期结果")
    mark = db.Column(db.String(100), nullable=True, comment="用例备注")

    # case 与 模块 属于多对一 关系
    partID = db.Column(db.INTEGER, db.ForeignKey('case_part.id', ondelete='SET NULL'), nullable=True, comment="模块")
    # case 与 product 是多对一关系 、产品删除、用例productID 置为null
    projectID = db.Column(db.INTEGER, db.ForeignKey("project.id", ondelete="SET NULL"), nullable=True, comment="所属产品")
    # case与platform 是多对一关系、平台删除、字段置为空、可无平台
    platformID = db.Column(db.INTEGER, db.ForeignKey('platform.id', ondelete="SET NUll"), nullable=True, comment="所属平台")
    # version yu case 是1vn
    versionID = db.Column(db.INTEGER, db.ForeignKey('version.id', ondelete='SET NUll'), nullable=True, comment="所属版本")

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
                 versionID: Optional[int] = None):
        self.title = title
        self.desc = desc
        self.creator = g.user.id
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
