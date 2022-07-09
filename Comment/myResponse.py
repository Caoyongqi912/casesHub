# @Time : 2022/7/6 22:32 
# @Author : cyq
# @File : myResponse.py
# @Software: PyCharm
# @Desc: 返回自定义
from typing import Any, AnyStr, Dict
from Enums.errorCode import ResponseCode, ResponseMSg



class MyResponse:

    @staticmethod
    def success(data: Any) -> Dict:
        return {"code": ResponseCode.SUCCESS, "data": data, "msg": ResponseMSg.OK}

    @staticmethod
    def error(code: ResponseCode, *args) -> Dict:
        return {"code": code, "data": None, "msg": ResponseMSg.ERROR}


class ParamError(MyResponse):

    @staticmethod
    def error(msg: AnyStr, *args) -> Dict:
        return super(ParamError, ParamError).error(ResponseCode.PARAMS_ERROR, msg)
