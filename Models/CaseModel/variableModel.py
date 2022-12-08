# @Time : 2022/9/15 20:15 
# @Author : cyq
# @File : variableModel.py
# @Software: PyCharm
# @Desc:
from typing import Dict, Any

from flask import g

from App import db
from Models.base import Base


class VariableModel(Base):
    __tablename__ = "variable"
    key = db.Column(db.String(20), comment="变量名称")
    val = db.Column(db.String(500), comment="变量值")
    desc = db.Column(db.String(500), comment="描述")
    creator = db.Column(db.String(20), comment="创建人")
    updater = db.Column(db.String(20), comment="修改人")
    projectID = db.Column(db.INTEGER, db.ForeignKey('project.id', ondelete='SET NUll'), nullable=True,
                          comment="所属项目")

    def __init__(self, key: str, val: str, projectID: int, desc: str = None):
        self.key = key
        self.val = val
        self.projectID = projectID
        self.desc = desc
        self.creator = g.user.username

    @property
    def to_Dict(self) -> Dict[str, Any]:
        return {self.key: self.val}

    def __repr__(self):
        return f"<{VariableModel.__name__} {self.key}>"
