#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2022-09-16
# @Author : cyq
# @File : casesHub
# @Software: PyCharm
# @Desc: 流程接口实体类

from typing import List, Any
from flask import g
from App import db
from Models.base import Base


class InterfaceModel(Base):
    __tablename__ = 'interface'
    title = db.Column(db.String(40), comment="标题")
    desc = db.Column(db.String(200), nullable=True, comment="描述")
    mark = db.Column(db.String(200), nullable=True, comment="备注")
    type = db.Column(db.String(10), default="HTTP", comment='请求类型')
    creator = db.Column(db.INTEGER, comment="创建人")
    updater = db.Column(db.INTEGER, nullable=True, comment="修改人")
    connectTimeout = db.Column(db.INTEGER, nullable=True, default=6000, comment="连接超时")
    responseTimeout = db.Column(db.INTEGER, nullable=True, default=6000, comment="请求超时")
    caseID = db.Column(db.INTEGER, nullable=True, comment="关联的用例")

    partID = db.Column(db.INTEGER, db.ForeignKey('case_part.id', ondelete='SET NULL'), nullable=True,
                       comment="所属模块")
    projectID = db.Column(db.INTEGER, db.ForeignKey("project.id", ondelete="SET NULL"), nullable=True,
                          comment="所属产品")
    versionID = db.Column(db.INTEGER, db.ForeignKey('version.id', ondelete='SET NUll'), nullable=True,
                          comment="所属版本")
    steps = db.Column(db.JSON, comment="接口步骤")

    results = db.relationship("InterfaceResultModel", backref="interface", lazy="dynamic")

    def __init__(self, title: str, steps: List, desc: str = None, creator: int = None, updater: int = None,
                 mark: str = None,
                 type: str = "HTTP",
                 connectTimeout: int = None, responseTimeout
                 : int = None, caseID: int = None, projectID: int = None,
                 partID: int = None,
                 versionID: int = None):
        self.title = title
        self.steps = steps
        self.desc = desc
        self.type = type
        self.creator = creator if creator else g.user.id
        self.updater = updater
        self.mark = mark
        self.connectTimeout = connectTimeout
        self.responseTimeout = responseTimeout
        self.caseID = caseID
        self.projectID = projectID
        self.partID = partID
        self.versionID = versionID


@property
def query_results(self):
    return self.results.order_by("create_time").all()


def __repr__(self):
    return f"<{InterfaceModel.__name__} {self.title}>"


class InterfaceResultModel(Base):
    __tablename__ = 'interface_result'
    interfaceID = db.Column(db.INTEGER, db.ForeignKey('interface.id', ondelete='CASCADE'), comment="所属用例")
    resultInfo = db.Column(db.JSON, nullable=True, comment="响应结果")
    starterID = db.Column(db.INTEGER, comment="运行人ID")
    starterName = db.Column(db.String(20), comment="运行人姓名")
    useTime = db.Column(db.String(20), comment="用时")

    status = db.Column(db.Enum('SUCCESS', 'FAIL'), nullable=False, comment="运行状态")

    def __repr__(self):
        return f"<{InterfaceResultModel.__name__} {self.interfaceID}>"
