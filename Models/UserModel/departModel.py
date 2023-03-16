# @Time : 2022/7/9 18:34 
# @Author : cyq
# @File : departModel.py
# @Software: PyCharm
# @Desc: 部门库


from typing import AnyStr, Dict

from flask_sqlalchemy import Pagination

from Comment.myException import AuthException
from Models.UserModel.userModel import User
from Models.base import Base
from App import db
from Utils import UUID


class Department(Base):
    __tablename__ = "department"
    name = db.Column(db.String(20), unique=True, comment="用户名")
    desc = db.Column(db.String(40), nullable=True, comment="部门描述")
    adminID = db.Column(db.INTEGER, nullable=True, comment="部门负责人")
    adminName = db.Column(db.String(10), nullable=True, comment="部门负责人名称")
    users = db.relationship("User", backref="department", lazy="dynamic")
    tags = db.relationship("UserTag", backref="departTags", lazy="dynamic")

    def __init__(self, name: AnyStr, adminID: int = None, desc: AnyStr = None, tags: list = None):
        self.name = name
        self.desc = desc
        self.adminID = adminID
        self.adminName = User.get(adminID).username if adminID else None
        if tags:
            self.tags = [UserTag(name=tag, departmentID=self.id) for tag in tags]

    @property
    def admin(self) -> int:
        """
        返回管理员ID
        :return: adminID
        """
        return self.adminID

    @property
    def query_tags(self):
        return self.tags.all()

    @classmethod
    def update(cls, **kwargs):
        """
        添加权限过滤
        必须是ADMIN or AdminID
        :param kwargs:
        :return:
        """
        from flask import g
        target = cls.get_by_uid(kwargs.get('uid'))
        if not g.user.isAdmin or not g.user.id != target.adminID:
            raise AuthException()
        return super(Department, Department).update(**kwargs)

    def __repr__(self):
        return f"<{Department.__name__} {self.name}>"


class UserTag(Base):
    __tablename__ = "userTag"
    name = db.Column(db.String(20), unique=True, comment="标签名称")
    departmentID: int = db.Column(db.INTEGER, db.ForeignKey("department.id", ondelete="set null"), nullable=True,
                                  comment="所属部门")

    def __init__(self, name: str, departmentID: int, uid: str = UUID().getUId):
        self.name = name
        self.departmentID = departmentID
        self.uid = uid

    def __repr__(self):
        return f"<{UserTag.__name__} {self.name}>"
