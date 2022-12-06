# @Time : 2022/9/15 20:15 
# @Author : cyq
# @File : variableModel.py
# @Software: PyCharm
# @Desc:
from typing import Dict, Any

from App import db
from Models.base import Base


class VariableModel(Base):
    __tablename__ = "variable"
    key = db.Column(db.String(20), comment="变量名称")
    val = db.Column(db.String(500), comment="变量值")
    projectID = db.Column(db.INTEGER, db.ForeignKey('project.id', ondelete='SET NUll'), nullable=True,
                          comment="所属项目")

    def __init__(self, key: str, val: str, projectID: int):
        self.key = key
        self.val = val
        self.projectID = projectID

    @property
    def to_Dict(self) -> Dict[str, Any]:
        return {self.key: self.val}

    def __repr__(self):
        return f"<{VariableModel.__name__} {self.key}>"
