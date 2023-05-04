#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2022-09-16
# @Author : cyq
# @File : casesHub
# @Software: PyCharm
# @Desc: 流程接口实体类

from typing import List, Any, NoReturn, Mapping, Dict
from flask import g
from sqlalchemy import Column, String, JSON

from App import db
from Enums import CaseLevel, IntEnum, CaseStatus
from Enums.myEnum import CaseAPIStatus
from Models.base import Base


class InterfaceModel(Base):
    __tablename__ = 'interface'
    title = db.Column(db.String(40), comment="标题")
    desc = db.Column(db.String(200), nullable=True, comment="描述")
    http = db.Column(db.String(10), default="HTTP", comment='请求类型')
    level = db.Column(IntEnum(CaseLevel), comment="接口用例等级")
    status = db.Column(IntEnum(CaseAPIStatus), comment="接口用例状态")
    steps = db.Column(db.JSON, nullable=True, comment="接口步骤")
    creator = db.Column(db.INTEGER, comment="创建人")
    updater = db.Column(db.INTEGER, nullable=True, comment="修改人")
    creatorName = db.Column(db.String(20), comment="创建人姓名")
    updaterName = db.Column(db.String(20), comment="修改人姓名")

    connectTimeout = db.Column(db.INTEGER, nullable=True, default=6000, comment="连接超时")
    responseTimeout = db.Column(db.INTEGER, nullable=True, default=6000, comment="请求超时")

    casePartID = db.Column(db.INTEGER, db.ForeignKey('case_part.id'), nullable=True,
                           comment="所属模块")
    projectID = db.Column(db.INTEGER, db.ForeignKey("project.id"), nullable=False,
                          comment="所属产品")
    results = db.relationship("InterfaceResultModel", backref="interface", lazy="dynamic")

    def __init__(self, title: str, steps: List, desc: str = None, creator: int = None,
                 http: str = "HTTP",
                 connectTimeout: int = None,
                 responseTimeout
                 : int = None, projectID: int = None,
                 status: CaseAPIStatus = CaseAPIStatus.DEBUG.value,
                 level: CaseLevel = None,
                 casePartID: int = None):
        self.title = title
        self.steps = steps
        self.desc = desc
        self.http = http
        self.level = level
        self.status = status
        self.creator = creator if creator else g.user.id
        self.creatorName = g.user.username if g.user else None
        self.connectTimeout = connectTimeout
        self.responseTimeout = responseTimeout
        self.projectID = projectID
        self.casePartID = casePartID

    @property
    def query_results(self):
        return self.results.order_by("create_time").all()

    @classmethod
    def update(cls, **kwargs) -> NoReturn:
        """
        更新、添加updaterName字段
        :param kwargs:
        :return:
        """
        kwargs.setdefault("updaterName", g.user.username)
        return super(InterfaceModel, cls).update(**kwargs)

    def __repr__(self):
        return f"<{InterfaceModel.__name__} {self.title}>"


class InterfaceResultModel(Base):
    __tablename__ = 'interface_result'
    interfaceID = db.Column(db.INTEGER, db.ForeignKey('interface.id', ondelete='CASCADE'), comment="所属用例")
    interfaceName = db.Column(db.String(20), comment="用例名称")
    interfaceSteps = db.Column(db.INTEGER, comment="用例步长")
    interfaceLog = db.Column(db.TEXT, comment="运行日志")
    useTime = db.Column(db.String(20), comment="用时")
    resultInfo = db.Column(db.JSON, nullable=True, comment="响应结果")
    starterID = db.Column(db.INTEGER, comment="运行人ID")
    starterName = db.Column(db.String(20), comment="运行人姓名")
    status = db.Column(db.Enum('SUCCESS', 'FAIL'), nullable=False, comment="运行状态")

    def __repr__(self):
        return f"<{InterfaceResultModel.__name__} {self.interfaceID}>"


class InterfaceGroupResultModel(Base):
    __tabename__ = "interfaces_result"
    status = db.Column(db.String(10), default="RUNNING", comment="状态")
    totalNumber = db.Column(db.INTEGER, comment="总运行数量")
    successNumber = db.Column(db.INTEGER, comment="成功数量")
    failNumber = db.Column(db.INTEGER, comment="失败梳理")
    starter = db.Column(db.String(20), comment="运行人")
    totalUseTime = db.Column(db.String(20), comment="运行时间")
    detail = db.Column(db.JSON, comment="运行详情")

    def __repr__(self):
        return f"<{InterfaceGroupResultModel.__name__}>"
