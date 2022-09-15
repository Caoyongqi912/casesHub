# @Time : 2022/9/15 20:15 
# @Author : cyq
# @File : envValueModel.py
# @Software: PyCharm
# @Desc:
from App import db
from Models.base import Base


class EnvValueModel(Base):
    __tablename__ = "api_env_value"
    name = db.Column(db.String(20), comment="变量名称")
    value = db.Column(db.String(500), comment="变量值")
    projectID = db.Column(db.INTEGER, db.ForeignKey('project.id', ondelete='SET NUll'), nullable=True, comment="所属项目")

    def __init__(self, name: str, value: str, projectID: int):
        self.name = name
        self.value = value
        self.projectID = projectID

    def __repr__(self):
        return f"<{EnvValueModel.__name__} {self.name}>"
