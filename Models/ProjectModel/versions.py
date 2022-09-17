# @Time : 2022/7/10 21:12 
# @Author : cyq
# @File : versions.py 
# @Software: PyCharm
# @Desc: 版本实体

from typing import AnyStr, NoReturn

from flask_sqlalchemy import Pagination

from Comment.myException import ParamException
from Enums import ResponseMsg
from Models.ProjectModel.project import Project
from Models.base import Base
from App import db
from Utils import MyLog

log = MyLog.get_log(__file__)


class Version(Base):
    __tablename__ = "version"
    name = db.Column(db.String(20), comment="版本名称")
    desc = db.Column(db.String(100), nullable=True, comment="版本描述")
    projectID = db.Column(db.INTEGER, db.ForeignKey("project.id", ondelete="CASCADE"), comment="所属产品")
    # prd = db.Column(db.String(200), nullable=False, comment="需求链接")
    cases = db.relationship("Cases", backref='version', lazy='dynamic')
    bugs = db.relationship("Bug", backref='version', lazy="dynamic")
    interfaces = db.relationship("InterfaceModel", backref="version", lazy="dynamic")

    # apis = db.relationship("ApiModel", backref="version", lazy="dynamic")

    def __init__(self, name: AnyStr, projectID: int, desc: AnyStr = None):
        self.name = name
        self.desc = desc
        self.projectID = projectID
        self.__uniqueName()

    def __uniqueName(self) -> NoReturn:
        """
        表设置不重名 但是产品下的不可重名 不同产品的版本重名
        :raise:  ParamError
        """
        v = [v.name for v in Project.get(self.projectID).query_version]
        if self.name in v:
            raise ParamException(ResponseMsg.already_exist(self.name))

    def page_cases(self, **kwargs) -> Pagination:
        """
        查询用力分页
        """
        return self.cases.my_paginate(**kwargs)

    def page_bugs(self, **kwargs) -> Pagination:
        """
        查询bug分页
        """
        return self.bugs.my_paginate(**kwargs)

    def __repr__(self):
        return f"<{Version.__name__} {self.name}>"
