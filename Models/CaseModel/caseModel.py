#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023-04-21
# @Author : cyq
# @File : casesHub
# @Software: PyCharm
# @Desc: 测试用例模型
from App import db
from Models.base import Base
from sqlalchemy import Column, INTEGER, String, Enum, JSON


class CaseModel(Base):
    __tablename__ = "caseHub"

    case_title = Column(String(20), nullable=False, comment="用例名称")
    case_desc = Column(String(100), nullable=False, comment="用例描述")
    case_level = Column(Enum('P0', 'P1', 'P2', 'P3'), nullable=False, server_default='P1', comment='用例等级')
    case_type = Column(Enum('COMMENT', 'SMOKE'), nullable=False, server_default='COMMENT', comment='用例类型')
    case_setup = Column(String(100), nullable=True, comment="用例前置")
    case_info = Column(JSON, nullable=False, comment="用例信息")
    case_mark = Column(String(100), nullable=True, comment="用例备注")

    casePartID = Column(INTEGER, db.ForeignKey('case_part.id'), nullable=True,
                           comment="所属模块")
    projectID = db.Column(db.INTEGER, db.ForeignKey("project.id"), nullable=False,
                          comment="所属产品")
