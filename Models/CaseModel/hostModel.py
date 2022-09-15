# @Time : 2022/9/15 20:11 
# @Author : cyq
# @File : hostModel.py
# @Software: PyCharm
# @Desc:
from App import db
from Models.base import Base


class HostModel(Base):
    __tablename__ = "api_host"
    name = db.Column(db.String(20), comment="host 名称")
    host = db.Column(db.String(50), comment="host 值")
    projectID = db.Column(db.INTEGER, db.ForeignKey('project.id', ondelete='SET NUll'), nullable=True, comment="所属版本")

    def __init__(self, name: str, host: str, projectID: int):
        self.name = name
        self.host = host
        self.projectID = projectID

    def __repr__(self):
        return f"<{HostModel.__name__} {self.name}>"
