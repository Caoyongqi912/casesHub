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
from Utils import MyLog, variable2dict, MyTools

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
    adminID = db.Column(db.INTEGER, comment="项目负责人ID")
    adminName = db.Column(db.String(20), unique=True, comment="项目负责人姓名")

    # 用户跟产品是 多对多 绑定
    users = db.relationship("User", backref="project", lazy="dynamic", secondary=projectUser)
    # 版本跟产品是 多对一 关系
    versions = db.relationship("Version", backref="project", lazy="dynamic")
    # 用例 与 产品为一对多关系
    cases = db.relationship("Cases", backref="project", lazy="dynamic")
    parts = db.relationship("CasePart", backref="project", lazy="dynamic")
    hosts = db.relationship("HostModel", backref="project", lazy="dynamic")
    variables = db.relationship("VariableModel", backref="project", lazy="dynamic")
    interfaces = db.relationship("InterfaceModel", backref="project", lazy="dynamic")

    # apis = db.relationship("ApiModel", backref="project", lazy="dynamic")

    def __init__(self, name: AnyStr, desc: AnyStr, adminID: int, adminName: AnyStr):
        self.name = name
        self.desc = desc
        self.adminName = adminName
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

        uIds = [u.id for u in self.users.all()]
        for uid in users:
            u: User = User.get(uid, f"uid {uid}")
            if MyTools.search(uIds, u.id):
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
        target = cls.get_by_uid(kwargs.get('uid'))
        if not g.user.isAdmin and not g.user.id == target.adminID:
            raise AuthException()
        return super(Project, Project).update(**kwargs)

    @property
    def query_casePart(self):
        return self.parts.all()

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
    def query_variables(self) -> List:
        """
        query envs
        :return: envs
        """
        return self.variables.all()

    @variable2dict
    def query_variables2dict(self):
        """
        variables obj -> dict
        :return:
        """
        return self.variables.all()

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
