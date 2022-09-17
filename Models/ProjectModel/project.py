# @Time : 2022/7/10 21:01 
# @Author : cyq
# @File : projectController.py
# @Software: PyCharm
# @Desc: 产品实体


from typing import AnyStr, List, NoReturn
from flask_sqlalchemy import Pagination
from Comment.myException import AuthException, ParamException
from Comment.myResponse import ParamError
from Enums import ResponseMsg
from Models.DepartModel.userModel import User
from Models.base import Base
from App import db
from Utils import MyLog, simpleCase, simpleUser

log = MyLog.get_log(__file__)

projectUser = db.Table(
    "project_user",
    db.Column("project_id", db.INTEGER, db.ForeignKey("project.id"), primary_key=True),
    db.Column("user_id", db.INTEGER, db.ForeignKey("user.id"), primary_key=True)

)


class Project(Base):
    __tablename__ = "project"
    name = db.Column(db.String(20), unique=True, comment="项目名称")
    desc = db.Column(db.String(100), nullable=True, comment="项目描述")
    adminID = db.Column(db.INTEGER, comment="项目负责人")

    # 用户跟产品是 多对多 绑定
    users = db.relationship("User", backref="project", lazy="dynamic", secondary=projectUser)
    # 版本跟产品是 多对一 关系
    versions = db.relationship("Version", backref="project", lazy="dynamic")
    # 用例 与 产品为一对多关系
    cases = db.relationship("Cases", backref="project", lazy="dynamic")
    parts = db.relationship("CasePart", backref="project", lazy="dynamic")
    hosts = db.relationship("HostModel", backref="project", lazy="dynamic")
    envs = db.relationship("EnvValueModel", backref="project", lazy="dynamic")
    interfaces = db.relationship("InterfaceModel", backref="project", lazy="dynamic")

    # apis = db.relationship("ApiModel", backref="project", lazy="dynamic")

    def __init__(self, name: AnyStr, desc: AnyStr, adminID: int):
        self.name = name
        self.desc = desc
        self.adminID = adminID

    def addUsers(self, users: List[int]) -> NoReturn:
        """
        批量添加用户
        必须是admin or adminID可添加
        需要校验是否已经添加过
        :param users:
        :raise ParamError
        """
        self.__verify_auth()

        uIds: List[int] = [u.id for u in self.users.all()]
        for uid in users:
            u: User = User.get(uid, f"uid {uid}")
            if self.search(uIds, u.id):
                raise ParamException(ResponseMsg.already_exist(str(id)))
            else:
                self.users.append(u)
        self.save()

    @classmethod
    def update(cls, **kwargs):
        """
        添加权限过滤
        必须是ADMIN or AdminID
        :param kwargs: Project
        """
        from flask import g
        target = cls.get(kwargs.get('id'), f"{cls.__name__} id")
        if not g.user.isAdmin and not g.user.id == target.adminID:
            raise AuthException()
        return super(Project, Project).update(**kwargs)

    def page_case(self, **kwargs) -> Pagination:
        """
        查询用例分页
        :param kwargs: limit
        :param kwargs:  page
        :return: Pagination
        """
        return self.cases.my_paginate(**kwargs)

    def page_version(self, **kwargs) -> Pagination:
        """
        查询版本分页
        """
        return self.versions.my_paginate(**kwargs)

    def page_casePart(self, **kwargs) -> Pagination:
        """
        查询用例分组分页
        """
        return self.parts.my_paginate(**kwargs)

    def page_user(self, **kwargs) -> Pagination:
        """
        分页查询用户分页
        """
        return self.users.my_paginate(**kwargs)

    @property
    def query_host(self) -> List:
        """
        query host
        :return: hosts
        """
        return self.hosts.all()

    @property
    def query_version(self) -> List:
        """
        query versions
        :return: versions
        """
        return self.versions.all()

    @property
    def query_env(self) -> List:
        """
        query envs
        :return: envs
        """
        return self.envs.all()

    def __verify_auth(self) -> NoReturn:
        """
        权限校验
        :raise:  AuthException
        """
        from flask import g
        if not g.user.isAdmin and not g.user.id == self.adminID:
            raise AuthException()

    def __repr__(self):
        return f"<{Project.__name__} {self.name}>"
