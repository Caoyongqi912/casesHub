# @Time : 2022/7/5 21:38 
# @Author : cyq
# @File : base_query.py
# @Software: PyCharm
# @Desc: MyBaseQuery

from flask_sqlalchemy import BaseQuery
from Comment.myException import ParamException
from Enums.errorCode import ResponseMsg


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
        rv = self.get(ident)
        if not rv:
            raise ParamException(ResponseMsg.no_existent(name))
        return rv
