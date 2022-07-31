# @Time : 2022/7/5 21:38 
# @Author : cyq
# @File : base_query.py
# @Software: PyCharm
# @Desc: MyBaseQuery
from typing import Any, AnyStr, ClassVar

from flask_sqlalchemy import BaseQuery, Pagination
from Comment.myException import ParamException
from Enums.errorCode import ResponseMsg
from Utils.myWraps import pageSerialize
from Utils.myLog import MyLog

log = MyLog.get_log(__file__)


class MyBaseQuery(BaseQuery):

    # def filter_by(self, **kwargs):
    #     """
    #     ¹ıÂËÈíÉ¾³ı
    #     :param kwargs:
    #     :return:
    #     """
    #
    #     kwargs.setdefault('status', 1)
    #     return super().filter_by(**kwargs)

    def get_or_NoFound(self, ident, name):
        """
        get self by id
        :param ident: id
        :param name:  cls.__name__
        :return: cls.self
        :raise:ParamException
        """

        rv = self.get(ident)
        if not rv:
            raise ParamException(ResponseMsg.no_existent(name))
        return rv

    @pageSerialize
    def my_paginate(self, page: AnyStr, limit: AnyStr, by: AnyStr = None) -> Pagination:
        """
        paginate
        :param by: order_by
        :param page:  page
        :param limit: limit
        :return: Pagination
        """
        page = int(page)
        limit = int(limit)
        items = self.order_by(by).limit(limit).offset((page - 1) * limit).all()
        total = self.order_by(by).count()
        return Pagination(self, page, limit, total, items)
