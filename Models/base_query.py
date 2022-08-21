# @Time : 2022/7/5 21:38 
# @Author : cyq
# @File : base_query.py
# @Software: PyCharm
# @Desc: MyBaseQuery
from flask_sqlalchemy import BaseQuery, Pagination
from Comment.myException import ParamException
from Enums import ResponseMsg
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

    def get_or_NoFound(self, ident: int | str, name: str) -> BaseQuery:
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
    def my_paginate(self, pageSize: int, current: int, sort: str = None) -> Pagination:
        """
        paginate
        :param pageSize:    pageSize
        :param current:    current
        :param sort:    order_by(sort)
        :return:    Pagination
        """

        items = self.order_by(sort).limit(pageSize).offset((current - 1) * pageSize).all()
        total = self.order_by(sort).count()
        return Pagination(self, current, pageSize, total, items)
