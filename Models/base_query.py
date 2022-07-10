# @Time : 2022/7/5 21:38 
# @Author : cyq
# @File : base_query.py
# @Software: PyCharm
# @Desc:
from flask_sqlalchemy import BaseQuery


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
        # if not rv:
        #     abort(400, **myResponse(ResponseCode.ERROR, None, f"{name}: {ident} non-existent "))
        # elif rv.status == 0:
        #     abort(400, **myResponse(ResponseCode.ERROR, None, f"{name}: {ident} Deleted"))
        return rv
