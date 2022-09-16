#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2022-09-16
# @Author : cyq
# @File : casesHub
# @Software: PyCharm
# @Desc: 流程接口实体类
from typing import List

from flask import g

from App import db
from Models.base import Base


class InterfaceModel(Base):
    __tablename__ = 'interface'
    title = db.Column(db.String(40), comment="标题")
    desc = db.Column(db.String(200), nullable=True, comment="描述")
    mark = db.Column(db.String(200), nullable=True, comment="备注")
    creator = db.Column(db.INTEGER, comment="创建人")
    updater = db.Column(db.INTEGER, nullable=True, comment="修改人")
    connectTimeout = db.Column(db.INTEGER, nullable=True, default=6000, comment="连接超时")
    responseTimeout = db.Column(db.INTEGER, nullable=True, default=6000, comment="请求超时")
    caseID = db.Column(db.INTEGER, nullable=True, comment="关联的用例")

    partID = db.Column(db.INTEGER, db.ForeignKey('case_part.id', ondelete='SET NULL'), nullable=True, comment="所属模块")
    projectID = db.Column(db.INTEGER, db.ForeignKey("project.id", ondelete="SET NULL"), nullable=True, comment="所属产品")
    versionID = db.Column(db.INTEGER, db.ForeignKey('version.id', ondelete='SET NUll'), nullable=True, comment="所属版本")

    steps = db.Column(db.JSON, comment="接口步骤")

    def __init__(self, title: str, steps: List, desc: str = None, creator: int = None, updater: int = None,
                 mark: str = None,
                 connectTimeout: int = None, responseTimeout: int = None, caseID: int = None, projectID: int = None,
                 partID: int = None,
                 versionID: int = None):
        self.title = title
        self.steps = steps
        self.desc = desc
        self.creator = creator if creator else g.user.id
        self.updater = updater
        self.mark = mark
        self.connectTimeout = connectTimeout
        self.responseTimeout = responseTimeout
        self.caseID = caseID
        self.projectID = projectID
        self.partID = partID
        self.versionID = versionID
