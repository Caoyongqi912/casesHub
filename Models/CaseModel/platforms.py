# @Time : 2022/7/10 21:15 
# @Author : cyq
# @File : platforms.py 
# @Software: PyCharm
# @Desc: 平台实体


from typing import AnyStr

from flask_sqlalchemy import Pagination

from Models.base import Base
from App import db
from Utils import simpleCase


class Platform(Base):
    __tablename__ = "platform"

    name = db.Column(db.Enum("IOS", "ANDROID", "WEB", "PC"), comment="平台名称")
    cases = db.relationship("Cases", backref="platform", lazy="dynamic")

    def __init__(self, name: AnyStr):
        self.name = name

    @simpleCase
    def page_case(self, **kwargs) -> Pagination:
        """
        查询用例分页
        :param limit: limit
        :param page: page
        :return:Pagination
        """
        return self.cases.my_paginate(**kwargs)

    def __repr__(self):
        return f"{Platform.__name__} {self.name}"
