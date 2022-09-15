from Enums import IntEnum, CaseLevel, CaseTag
from Models.base import Base
from App import db
from Utils import MyLog
from flask import g
from typing import AnyStr

log = MyLog.get_log(__file__)


class ApiModel(Base):
    __tablename__ = "case_api"
    title = db.Column(db.String(20), comment="接口名称")
    desc = db.Column(db.String(300), comment="接口描述")
    path = db.Column(db.String(500), comment="接口路径")
    method = db.Column(db.String(500), comment="请求方法")
    creator = db.Column(db.INTEGER, nullable=False, comment="创建人")
    updater = db.Column(db.INTEGER, nullable=True, comment="修改人")
    case_level = db.Column(IntEnum(CaseLevel), comment="用例等级")
    tag = db.Column(IntEnum(CaseTag), comment="接口标签")
    info = db.Column(db.JSON, nullable=True, comment="请求详情")
    connectTimeout = db.Column(db.INTEGER, nullable=True, comment="请求详情")
    responseTimeout = db.Column(db.INTEGER, nullable=True, comment="请求详情")
    mark = db.Column(db.String(100), nullable=True, comment="用例备注")

    caseID = db.Column(db.INTEGER, nullable=True, comment="关联caseID")

    # api 与 模块 属于多对一 关系
    partID = db.Column(db.INTEGER, db.ForeignKey('case_part.id', ondelete='SET NULL'), nullable=True, comment="模块")
    # api 与 project 是多对一关系 、产品删除、用例productID 置为null
    projectID = db.Column(db.INTEGER, db.ForeignKey("project.id", ondelete="SET NULL"), nullable=True, comment="所属产品")
    # api yu case 是1vn
    versionID = db.Column(db.INTEGER, db.ForeignKey('version.id', ondelete='SET NUll'), nullable=True, comment="所属版本")

    def _verify_info(self):
        """
        info:{
            headers:[{name:Content-Type,value:application/json}],
            body:[{name:xx,value:x}],
            query:[{name:xx,value:x}],
            verify:{
                "jsonPath":[{expression:$.name,expect:cyq,option:eq}],
                "re":[{expression:"&&&(^&**",expect:ada,option:eq}]
            }
        }
        :return:
        """
        pass
