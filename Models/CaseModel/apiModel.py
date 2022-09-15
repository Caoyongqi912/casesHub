from Comment.myException import ParamException
from Enums import CaseLevel, IntEnum, APIMethodEnum, ResponseMsg
from Models.base import Base
from App import db
from Utils import MyLog
from flask import g
from typing import  List, Dict, NoReturn

log = MyLog.get_log(__file__)


class ApiModel(Base):
    __tablename__ = "case_api"
    title = db.Column(db.String(20), comment="接口名称")
    desc = db.Column(db.String(300), comment="接口描述")
    path = db.Column(db.String(500), comment="接口路径")

    method = db.Column(IntEnum(APIMethodEnum), comment="请求方法")
    case_level = db.Column(IntEnum(CaseLevel), comment="用例等级")

    creator = db.Column(db.INTEGER, nullable=False, comment="创建人")
    updater = db.Column(db.INTEGER, nullable=True, comment="修改人")

    info = db.Column(db.JSON, nullable=True, comment="请求详情")

    connectTimeout = db.Column(db.INTEGER, nullable=True, default=6000, comment="连接超时")
    responseTimeout = db.Column(db.INTEGER, nullable=True, default=6000, comment="请求超时")

    caseID = db.Column(db.INTEGER, nullable=True, comment="关联caseID")

    partID = db.Column(db.INTEGER, db.ForeignKey('case_part.id', ondelete='SET NULL'), nullable=True, comment="模块")
    projectID = db.Column(db.INTEGER, db.ForeignKey("project.id", ondelete="SET NULL"), nullable=True, comment="所属产品")
    versionID = db.Column(db.INTEGER, db.ForeignKey('version.id', ondelete='SET NUll'), nullable=True, comment="所属版本")

    mark = db.Column(db.String(100), nullable=True, comment="用例备注")

    def __init__(self, title: str, desc: str, path: str, method: APIMethodEnum, case_level: CaseLevel,
                 creator: int = None, updater: int = None, info: Dict = None, connectTimeout: int = 60000,
                 responseTimeout: int = 60000, caseID: int = None, partID: int = None, projectID: int = None,
                 versionID: int = None,
                 mark: str = None):
        self.title = title
        self.desc = desc
        self.path = path
        self.method = method
        self.case_level = case_level
        self.creator = creator if creator else g.user.id
        self.updater = updater
        self.info = self._verify_info(info)
        self.connectTimeout = connectTimeout
        self.responseTimeout = responseTimeout
        self.caseID = caseID
        self.partID = partID
        self.projectID = projectID
        self.versionID = versionID
        self.mark = mark

    def _verify_info(self, info: Dict | None):
        """
        info:{
            headers:[{name:Content-Type,value:application/json}],
            body:[{name:xx,value:x}],
            query:[{name:xx,value:x}],
            verify:{
                "jsonPath":[{expression:$.name,expect:cyq,option:eq}],
                # "re":[{expression:"&&&(^&**",expect:ada,option:eq}]
            }
        }
        :return:
        """
        if info:
            self._verify_hbq(info.get("headers"))
            self._verify_hbq(info.get("body"))
            self._verify_hbq(info.get("query"))
            self._verify(info.get("verify"))
            return info
        return None

    @staticmethod
    def _verify_hbq(hbq: List[Dict[str, str]] | None) -> NoReturn:
        """
        校验header key has[name,value] and  value not empty
        :param hbq: header | body | query
        """
        if hbq:
            for header in hbq:
                name = header.get("name")
                value = header.get("value")
                if not name or not value:
                    raise ParamException(ResponseMsg.PARAM_ERROR)

    @staticmethod
    def _verify(v: Dict) -> NoReturn:
        """
        断言校验、暂支支持jsonpath
        :param v:
        :return:
        """
        if v and v.get("jsonPath"):
            for jp in v.get("jsonPath"):
                expression = jp.get("expression")
                expect = jp.get("expression")
                option = jp.get("option")
                if not expect and not expression and not option:
                    raise ParamException(ResponseMsg.PARAM_ERROR)
