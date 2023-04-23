# @Time : 2022/7/10 21:01 
# @Author : cyq
# @File : projectController.py
# @Software: PyCharm
# @Desc: 产品实体


from typing import AnyStr, List, NoReturn
from Comment.myException import AuthException, ParamException
from Enums import ResponseMsg
from Models.UserModel.userModel import User
from Models.base import Base
from App import db
from Utils import MyLog, variable2dict, MyTools

log = MyLog.get_log(__file__)

projectUser = db.Table(
    "project_user",
    db.Column("project_id", db.INTEGER, db.ForeignKey("project.id", ondelete='CASCADE'), primary_key=True),
    db.Column("user_id", db.INTEGER, db.ForeignKey("user.id", ondelete='CASCADE'), primary_key=True)

)


class Project(Base):
    __tablename__ = "project"

    name = db.Column(db.String(20), unique=True, comment="项目名称")
    desc = db.Column(db.String(100), nullable=True, comment="项目描述")

    adminID = db.Column(db.INTEGER, comment="项目负责人ID")
    adminName = db.Column(db.String(20), nullable=True, comment="项目负责人姓名")

    # 用户跟项目是 多对多 绑定
    users = db.relationship("User", backref="project", lazy="dynamic",
                            secondary=projectUser)
    # 版本跟项目是 多对一 关系
    # versions = db.relationship("Version", backref="project", lazy="dynamic")
    # 用例与项目为一对多关系
    cases = db.relationship("CaseModel", backref="project", lazy="dynamic")
    parts = db.relationship("CasePart", backref="project", lazy="dynamic")
    variables = db.relationship("VariableModel", backref="project", lazy="dynamic")
    interfaces = db.relationship("InterfaceModel", backref="project", lazy="dynamic")

    def __init__(self, name: AnyStr, desc: AnyStr, adminID: int, adminName: AnyStr):
        self.name = name
        self.desc = desc
        self.adminID = adminID
        self.adminName = adminName

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
            if MyTools.search(uIds, u.id):
                raise ParamException(ResponseMsg.already_exist(u.username))
            else:
                self.users.append(u)
        self.save(new=False)

    def delUser(self, uid: str) -> NoReturn:
        """
        删除单个用户
        :param uid: 用户uid
        :return:
        """
        self.__verify_auth()
        u = User.get_by_uid(uid)
        self.users.remove(u)

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
    def tree_casePart(self):
        query = self.parts.all()
        res = []
        for part in query:
            res.append(Base.to_json(part))
        return res

    @property
    def query_users(self):
        return self.users.all()

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
