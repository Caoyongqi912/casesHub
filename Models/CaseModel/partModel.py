# @Time : 2022/9/17 10:04 
# @Author : cyq
# @File : partModel.py 
# @Software: PyCharm
# @Desc:
from typing import List, Dict, Any

from App import db
from Models.base import Base


class CasePart(Base):
    __tablename__ = 'case_part'
    partName = db.Column(db.String(20), unique=True, comment="用例模块")

    # 用例模块与产品是多对一关系
    projectID = db.Column(db.INTEGER, db.ForeignKey("project.id"), nullable=True, comment="所属产品")
    # 模块与用例是一对多关系
    cases = db.relationship("Cases", backref='case_part', lazy='dynamic')
    interfaces = db.relationship("InterfaceModel", backref='case_part', lazy='dynamic')

    # apis = db.relationship("ApiModel", backref="case_part", lazy="dynamic")

    def __init__(self, partName: str, projectID: int):
        self.partName = partName
        self.projectID = projectID

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

    def __repr__(self):
        return f"<{CasePart.__name__} {self.part}>"
