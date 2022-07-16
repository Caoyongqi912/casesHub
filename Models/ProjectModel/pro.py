# @Time : 2022/7/10 21:01 
# @Author : cyq
# @File : pro.py
# @Software: PyCharm
# @Desc: 产品实体


from typing import AnyStr

from Comment.myException import AuthException
from Models.base import Base
from App import db
from Utils.myLog import MyLog

log = MyLog.get_log(__file__)


class Project(Base):
    __tablename__ = "project"
    name = db.Column(db.String(20), unique=True, comment="项目名称")
    desc = db.Column(db.String(100), nullable=True, comment="项目描述")
    adminID = db.Column(db.INTEGER, comment="项目负责人")

    products = db.relationship("Product", backref="products", lazy="dynamic")
    users = db.relationship("User", backref="project_user", lazy="dynamic")

    def __init__(self, name: AnyStr, desc: AnyStr, adminID: int):
        self.name = name
        self.desc = desc
        self.adminID = adminID

    def __repr__(self):
        return f"<{Project.__name__} {self.name}>"


class Product(Base):
    __tablename__ = "product"
    name = db.Column(db.String(20), unique=True, comment="产品名称")
    desc = db.Column(db.String(100), nullable=True, comment="产品描述")
    adminID = db.Column(db.INTEGER, comment="产品负责人")

    projectID = db.Column(db.INTEGER, db.ForeignKey("project.id"), nullable=False, comment="所属项目")
    users = db.relationship("User", backref="user", lazy="dynamic")
    cases = db.relationship("Cases", backref="case", lazy="dynamic")

    def __init__(self, name: AnyStr, desc: AnyStr, adminID: int,
                 projectID: int):
        self.name = name
        self.desc = desc
        self.adminID = adminID
        self.projectID = projectID

    def page_by(self, **kwargs):
        """
        分页
        :param kwargs:
        :return:
        """
        return self.cases.my_paginate(**kwargs)

    def __repr__(self):
        return f"<{Product.__name__} {self.name}>"


projectUsers = db.Table(
    "project_user",
    db.Column("projectID", db.INTEGER, db.ForeignKey("project.id")),
    db.Column("userID", db.INTEGER, db.ForeignKey("user.id")),

)
productUsers = db.Table(
    "product_user",
    db.Column("productID", db.INTEGER, db.ForeignKey("product.id")),
    db.Column("userID", db.INTEGER, db.ForeignKey("user.id")),

)
