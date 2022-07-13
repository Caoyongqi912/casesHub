# @Time : 2022/7/5 21:38 
# @Author : cyq
# @File : base_query.py
# @Software: PyCharm
# @Desc: MyBaseQuery
from typing import Any, AnyStr

from flask_sqlalchemy import BaseQuery, Pagination
from sqlalchemy.exc import OperationalError

from Comment.myException import ParamException,MyException
from Enums.errorCode import ResponseMsg
from Utils.myWraps import pageSerialize
from Utils.myLog import MyLog

log = MyLog.get_log(__file__)

class MyBaseQuery(BaseQuery):

    # def filter_by(self, **kwargs):
    #     """
    #     ¹ýÂËÈíÉ¾³ý
    #     :param kwargs:
    #     :return:
    #     """
    #
    #     kwargs.setdefault('status', 1)
    #     return super().filter_by(**kwargs)

    def get_or_NoFound(self, ident, name):
        try:
            rv = self.get(ident)
            if not rv:
                raise ParamException(ResponseMsg.no_existent(name))
            return rv
        except OperationalError as e:
            raise MyException()

    @pageSerialize
    def my_paginate(self, page: int, limit: int):
        items = self.limit(limit).offset((page - 1) * limit).all()
        total = self.order_by(None).count()
        return Pagination(self, page, limit, total, items)
