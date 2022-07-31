# @Time : 2022/7/10 21:01 
# @Author : cyq
# @File : pro.py
# @Software: PyCharm
# @Desc: 产品实体


from typing import AnyStr, NoReturn, List

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
        if not g.user.isAdmin and not g.user.id == target.adminID:
            raise AuthException()
        return super(Project, Project).update(**kwargs)

    def page_product(self, **kwargs) -> List:
        return self.products.all()
        # return super(Product, self.products).page(**kwargs)

    def __repr__(self):
        return f"<{Project.__name__} {self.name}>"


class Product(Base):
    __tablename__ = "product"
    name = db.Column(db.String(20), unique=True, comment="产品名称")
    desc = db.Column(db.String(100), nullable=True, comment="产品描述")
    projectID = db.Column(db.INTEGER, db.ForeignKey("project.id"), nullable=False, comment="所属项目")

    # users = db.relationship("User", backref="user", lazy="dynamic")
    # cases = db.relationship("Cases", backref="case", lazy="dynamic")
    # parts = db.relationship("CasePart", backref='product_part', lazy="dynamic")
    # versions = db.relationship("Version", backref="version", lazy="dynamic")

    def __init__(self, name: AnyStr, desc: AnyStr,
                 projectID: int):
        self.name = name
        self.desc = desc
        self.projectID = projectID

    @property
    def getParts(self):
        """
        获取part
        :return:
        """
        return self.parts.all()

    def save(self) -> NoReturn:
        """
        添加权限过滤
        ADMIN or ProjectAdmin 可添加
        """
        from flask import g
        ProjectAdmin = Project.get(self.projectID).adminID

        if not g.user.isAdmin and not g.user.id == ProjectAdmin:
            raise AuthException()
        return super(Product, self).save()

    @classmethod
    def update(cls, **kwargs) -> NoReturn:
        """
        添加权限过滤
        ADMIN or ProjectAdmin 可添加
        :param kwargs: Product fields
        """
        from flask import g
        target = cls.get(kwargs.get('id'))
        ProjectAdmin = Project.get(target.projectID).adminID
        if not g.user.isAdmin and not g.user.id == ProjectAdmin:
            raise AuthException()
        return super(Product, target).update(**kwargs)

    @classmethod
    def delete(cls, **kwargs) -> NoReturn:
        """
        添加权限过滤
        ADMIN or ProjectAdmin 可添加
        :return:
        """
        from flask import g
        target = cls.get(kwargs.get('id'))
        ProjectAdmin = Project.get(target.projectID).adminID
        if not g.user.isAdmin and not g.user.id == ProjectAdmin:
            raise AuthException()
        return super(Product, target).delete_by_id(**kwargs)

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


productUsers = db.Table(
    "product_user",
    db.Column("productID", db.INTEGER, db.ForeignKey("product.id")),
    db.Column("userID", db.INTEGER, db.ForeignKey("user.id")),

)
