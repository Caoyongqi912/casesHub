#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2022-12-08
# @Author : cyq
# @File : casesHub
# @Software: PyCharm
# @Desc:
import time

from werkzeug.datastructures import FileStorage

from App import db
from Models.base import Base
from Utils import UUID, MyLog, getBugFilePath

log = MyLog.get_log(__file__)


class FileModel(Base):
    __tablename__ = "file"
    fileName = db.Column(db.String(50), comment="附件名称")
    fileType = db.Column(db.String(20), comment="附件格式")
    filePath = db.Column(db.String(100), comment="路径")
    bugID = db.Column(db.INTEGER, db.ForeignKey("bug.id", ondelete="SET NULL"), nullable=True, comment="所属BUG")

    def __repr__(self):
        return f"<{FileModel.__name__} {self.fileName}>"

    def todo(self, bugID: str, file: FileStorage = None):
        self.bugID = bugID
        self.fileName = UUID().getUId
        self.fileType = file.mimetype
        self.filePath = getBugFilePath(self.fileName)
        file.save(self.filePath)
        self.save()
