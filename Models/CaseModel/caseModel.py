#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023-04-21
# @Author : cyq
# @File : casesHub
# @Software: PyCharm
# @Desc: 测试用例模型
from flask import g
from App import db
from Comment.myException import ParamException
from Enums import ResponseMsg
from Models.base import Base
from sqlalchemy import Column, INTEGER, String, Enum, JSON
from typing import AnyStr, Mapping, Any, Optional, Union, NoReturn, List, Dict


class CaseModel(Base):
    __tablename__ = "caseHub"
    case_title = Column(String(20), nullable=False, comment="用例名称")
    case_desc = Column(String(100), nullable=False, comment="用例描述")
    case_level = Column(Enum('P0', 'P1', 'P2', 'P3'), nullable=False, server_default='P1', comment='用例等级')
    case_type = Column(Enum('COMMENT', 'SMOKE'), nullable=False, server_default='COMMENT', comment='用例类型')
    case_setup = Column(String(100), nullable=True, comment="用例前置")
    case_info = Column(JSON, nullable=False, comment="用例信息")
    case_mark = Column(String(100), nullable=True, comment="用例备注")

    creator = db.Column(db.INTEGER, comment="创建人")
    updater = db.Column(db.INTEGER, nullable=True, comment="修改人")
    creatorName = db.Column(db.String(20), comment="创建人姓名")
    updaterName = db.Column(db.String(20), comment="修改人姓名")

    casePartID = Column(INTEGER, db.ForeignKey('case_part.id'), nullable=False,
                        comment="所属模块")
    projectID = db.Column(db.INTEGER, db.ForeignKey("project.id"), nullable=False,
                          comment="所属产品")

    def __init__(self, case_title: AnyStr, case_desc: AnyStr, case_level: AnyStr, case_type: AnyStr,
                 case_setup: AnyStr, case_info: List[Dict[str, Any]],
                 casePartID: int, projectID: int, case_mark: Optional[Union[str, None]] = None, ) -> NoReturn:
        self.case_title = case_title
        self.case_level = case_level
        self.case_desc = case_desc
        self.case_type = case_type
        self.case_setup = case_setup
        self.case_info = self.__verify_info(case_info)
        self.casePartID = casePartID
        self.projectID = projectID
        self.case_mark = case_mark
        self.creator = g.user.id
        self.creatorName = g.user.username

    @staticmethod
    def __verify_info(info: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        校验steps格式  并按照 step 排序
        [
        {
            "step":1, *
            "todo": "to do ...",
            "exp": "exp ....", *

        },
        {
            "step":2,
            "todo": "to do ...",
            "exp": "exp ....",

        }
        ]
        :param info: ↑
        :return: info
        :raise: ParamException
        """

        def check_step(step):
            if not all(key in step for key in ["step", "todo", "exp"]):

                raise ParamException(ResponseMsg.error_param(target="case_info", msg="key err"))
        list(map(check_step, info))
        return sorted(info, key=lambda s: s["step"])
