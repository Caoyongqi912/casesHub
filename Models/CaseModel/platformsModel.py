# @Time : 2022/7/10 21:15 
# @Author : cyq
# @File : platformsModel.py
# @Software: PyCharm
# @Desc: 平台实体


from typing import AnyStr

from flask_sqlalchemy import Pagination

from Models.base import Base
from App import db
from Utils import simpleCase


class Platform(Base):
    __tablename__ = "platform"

    name = db.Column(db.String(30), unique=True, comment="平台名称")
    cases = db.relationship("Cases", backref="platform", lazy="dynamic")

    def __init__(self, name: AnyStr):
        self.name = name

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def __repr__(self):
        return f"{Platform.__name__} {self.name}"
