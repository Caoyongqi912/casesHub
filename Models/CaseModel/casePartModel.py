# @Time : 2022/9/17 10:04 
# @Author : cyq
# @File : casePartModel.py
# @Software: PyCharm
# @Desc:
from typing import List, Dict, Any, NoReturn

from App import db
from Comment.myException import ParamException
from Enums import ResponseMsg
from Models.ProjectModel.projectModel import Project
from Models.base import Base


class CasePart(Base):
    __tablename__ = 'case_part'
    partName = db.Column(db.String(20), comment="用例模块")

    # 用例模块与产品是多对一关系
    projectID = db.Column(db.INTEGER, db.ForeignKey("project.id"), nullable=True, comment="所属产品")
    # 模块与用例是一对多关系
    parentID = db.Column(db.INTEGER, nullable=True, comment='父模块')
    cases = db.relationship("Cases", backref='case_part', lazy='dynamic')
    interfaces = db.relationship("InterfaceModel", backref='case_part', lazy='dynamic')

    def __init__(self, partName: str, projectID: int, parentID: int = None):
        self.partName = partName
        self.projectID = projectID
        self.parentID = parentID

    @classmethod
    def getOrCreate(cls, partName: str, projectID: str | int) -> List[Dict[str, Any]] | Dict[str, Any]:
        """
        获取用例模块ID 或者创建一个在获取其ID
        :param partName:
        :param projectID
        :return: casePart
        """
        sql = "select * from case_part where partName = '{}' and projectID = '{}'".format(partName, projectID)
        val = CasePart.execute_sql(sql=sql)
        # 如果查询不到 创建一个新的
        if not val:
            c = cls(partName, projectID)
            c.save()
            return c
        return val

    def save_(self) -> NoReturn:
        """
        项目下、name唯一校验
        """
        p: Project = Project.get(self.projectID)
        if self.partName in [h.partName for h in p.query_casePart]:
            raise ParamException(ResponseMsg.already_exist(self.partName))
        return super(CasePart, self).save()

    def __repr__(self):
        return f"<{CasePart.__name__} {self.part}>"
