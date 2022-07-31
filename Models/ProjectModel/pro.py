# @Time : 2022/7/10 21:01 
# @Author : cyq
# @File : pro.py
# @Software: PyCharm
# @Desc: 产品实体


from typing import AnyStr

from flask_sqlalchemy import Pagination

from Comment.myException import AuthException
from Models.base import Base
from App import db
from Utils.myLog import MyLog
from Utils.myWraps import simpleCase, pageSerialize

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

    @classmethod
    def update(cls, **kwargs):
        """
        添加权限过滤
        必须是ADMIN or AdminID
        :param kwargs: Project
        """
        from flask import g
        target = cls.get(kwargs.get('id'), f"{cls.__name__} id")
        if not g.user.isAdmin or not g.user.id != target.adminID:
            raise AuthException()
        return super(Project, Project).update(**kwargs)

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
    parts = db.relationship("CasePart", backref='product_part', lazy="dynamic")
    versions = db.relationship("Version", backref="version", lazy="dynamic")

    def __init__(self, name: AnyStr, desc: AnyStr, adminID: int,
                 projectID: int):
        self.name = name
        self.desc = desc
        self.adminID = adminID
        self.projectID = projectID

    @property
    def getParts(self):
        """
        获取part
        :return:
        """
        return self.parts.all()

    @classmethod
    def update(cls, **kwargs):
        """
        添加权限过滤
        必须是ADMIN or AdminID
        :param kwargs:
        :return:
        """
        from flask import g
        target = cls.get(kwargs.get('id'), f"{cls.__name__} id")
        if not g.user.isAdmin or not g.user.id != target.adminID:
            raise AuthException()

        return super(Product, Product).update(**kwargs)

    @simpleCase
    def page_case(self, page: AnyStr, limit: AnyStr) -> Pagination:
        """
        查询用例分页
        :param limit: limit
        :param page: page
        :return:Pagination
        """
        limit = int(limit)
        page = int(page)
        items = self.cases.limit(limit).offset((page - 1) * limit).all()
        total = self.cases.order_by(None).count()
        return Pagination(self, page, limit, total, items)

    @pageSerialize
    def page_version(self, page: AnyStr, limit: AnyStr):
        """
        查询版本分页
        :param limit: limit
        :param page: page
        :return:Pagination
        """
        limit = int(limit)
        page = int(page)
        items = self.versions.limit(limit).offset((page - 1) * limit).all()
        total = self.versions.order_by(None).count()
        return Pagination(self, page, limit, total, items)

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
