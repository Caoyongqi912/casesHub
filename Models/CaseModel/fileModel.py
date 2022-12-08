#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2022-12-08
# @Author : cyq
# @File : casesHub
# @Software: PyCharm
# @Desc:
from App import db
from Models.base import Base


class FileModel(Base):
    __tablename__ = "file"
    name = db.Column(db.String(50), comment="附件名称")
    url = db.Column(db.String(50), comment="路由")
    bugID = db.Column(db.INTEGER, db.ForeignKey("bug.id", ondelete="SET NULL"), nullable=True, comment="所属BUG")


    def __repr__(self):
        return f"<{FileModel.__name__} {self.name}>"
