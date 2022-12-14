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
    fileName = db.Column(db.String(50), comment="附件名称")
    fileType = db.Column(db.String(100), comment="附件格式")
    filePath = db.Column(db.String(100), comment="路径")

    def __repr__(self):
        return f"<{FileModel.__name__} {self.fileName}>"

    def __init__(self, fileName: str, fileType: str, filePath: str):
        self.fileName = fileName
        self.fileType = fileType
        self.filePath = filePath
