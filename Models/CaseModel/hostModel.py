# @Time : 2022/9/15 20:11
# @Author : cyq
# @File : hostModel.py
# @Software: PyCharm
# @Desc:
from typing import NoReturn

from flask import g

from App import db
from Comment.myException import ParamException
from Enums import ResponseMsg
from Models.ProjectModel.projectModel import Project
from Models.base import Base
from Utils import UUID, MyLog

log = MyLog.get_log(__file__)


class HostModel(Base):
    __tablename__ = "api_host"
    name = db.Column(db.String(20), unique=True, comment="host 名称")
    host = db.Column(db.String(50), comment="host 值")
    desc = db.Column(db.String(100), nullable=True, comment="描述")
    creator = db.Column(db.String(20), comment="创建人")
    updater = db.Column(db.String(20), nullable=True, comment="修改人")

    def __init__(self, name: str, host: str, desc: str = None, creator: str = None, updater: str = None):
        self.name = name
        self.host = host
        self.desc = desc
        self.creator = creator if creator else g.user.username

    def __repr__(self):
        return f"<{HostModel.__name__} {self.name}>"
