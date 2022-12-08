# @Time : 2022/9/15 20:11
# @Author : cyq
# @File : hostModel.py
# @Software: PyCharm
# @Desc:
from typing import NoReturn

from App import db
from Comment.myException import ParamException
from Enums import ResponseMsg
from Models.ProjectModel.projectModel import Project
from Models.base import Base
from Utils import UUID, MyLog

log = MyLog.get_log(__file__)


class HostModel(Base):
    __tablename__ = "api_host"
    name = db.Column(db.String(20), comment="host 名称")
    host = db.Column(db.String(50), comment="host 值")
    projectID = db.Column(db.INTEGER, db.ForeignKey('project.id', ondelete='SET NUll'), nullable=True,
                          comment="所属版本")

    def __init__(self, name: str, host: str, projectID: int):
        self.name = name
        self.host = host
        self.projectID = projectID

    def save_(self) -> NoReturn:
        """
        项目下、name唯一校验
        """
        p: Project = Project.get(self.projectID)
        if self.name in [h.name for h in p.query_host]:
            raise ParamException(ResponseMsg.already_exist(self.name))
        return super(HostModel, self).save()

    def __repr__(self):
        return f"<{HostModel.__name__} {self.name}>"
