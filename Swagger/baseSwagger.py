# @Time : 2022/8/5 23:20 
# @Author : cyq
# @File : baseSwagger.py 
# @Software: PyCharm
# @Desc:

from flask_restx import Namespace, fields
from Enums import ResponseCode, ResponseMsg


class BaseSwagger:

    def __init__(self, ns: Namespace):
        self.ns = ns

    @property
    def success(self):
        return {"code": 200, "description": "success", "model": self.__model()}



    def __model(self):
        return self.ns.model("response", {
            "code": fields.Integer,
            "data": fields.Raw,
            "msg": fields.String
        })
