# @Time : 2022/7/9 18:34 
# @Author : cyq
# @File : departments.py 
# @Software: PyCharm
# @Desc: 部门库


from typing import AnyStr
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

    def __repr__(self):
        return f"<{Department.__name__} {self.name}>"
