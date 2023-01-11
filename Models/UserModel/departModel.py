# @Time : 2022/7/9 18:34 
# @Author : cyq
# @File : departModel.py
# @Software: PyCharm
# @Desc: 部门库


from typing import AnyStr

from Comment.myException import AuthException
from Models.base import Base
from App import db


class Department(Base):
    __tablename__ = "department"
    name = db.Column(db.String(20), unique=True, comment="用户名")
    desc = db.Column(db.String(40), nullable=True, comment="部门描述")
    adminID = db.Column(db.INTEGER, comment="部门负责人")
    users = db.relationship("User", backref="department", lazy="dynamic")

    def __init__(self, name: AnyStr, adminID: int, desc: AnyStr = None):
        self.name = name
        self.desc = desc
        self.adminID = adminID

    @property
    def admin(self) -> int:
        """
        返回管理员ID
        :return: adminID
        """
        return self.adminID

    @property
    def product_users(self):
        return self.users.filter_by().all()

    @classmethod
    def update(cls, **kwargs):
        """
        添加权限过滤
        必须是ADMIN or AdminID
        :param kwargs:
        :return:
        """
        from flask import g
        target = cls.get(kwargs.pop('id'), f"{cls.__name__} id")
        if not g.user.isAdmin or not g.user.id != target.adminID:
            raise AuthException()

        return super(Department, Department).update(**kwargs)

    def __repr__(self):
        return f"<{Department.__name__} {self.name}>"


class UserTag(Base):
    __tablename__ = "userTag"
    name = db.Column(db.String(20), unique=True, comment="标签名称")

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<{UserTag.__name__} {self.name}>"
