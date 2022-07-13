# @Time : 2022/7/9 18:34 
# @Author : cyq
# @File : departments.py 
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
    users = db.relationship("User", backref="users", lazy="dynamic")

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
        userAdmin departAdmin权限
        :param kwargs: Department
        :return:
        """
        department = cls.get(kwargs.get("departID"), "departID")
        from flask import g
        if not g.user.admin or not g.user.id != department.adminID:
            # 非admin or departAdmin 无权修改
            raise AuthException()
        department.name = kwargs.get("name")
        department.desc = kwargs.get("desc")
        if kwargs.get("adminID"):
            # 校验adminID是否存在
            from .users import User
            u = User.get(kwargs.get("adminID"), "adminID")
            department.adminID = u.id
        department.save()

    def __repr__(self):
        return f"<{Department.__name__} {self.name}>"
