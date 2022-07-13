# @Time : 2022/7/6 22:32 
# @Author : cyq
# @File : myResponse.py
# @Software: PyCharm
# @Desc: 返回自定义
from typing import Any, AnyStr, Dict
from flask import jsonify
from Enums.errorCode import ResponseCode, ResponseMsg


class MyResponse:

    @staticmethod
    def success(data: Any = None) -> jsonify:
        return jsonify({"code": ResponseCode.SUCCESS, "data": data, "msg": ResponseMsg.OK})

    @staticmethod
    def error(code: ResponseCode) -> Dict:
        return {"code": code, "data": None, "msg": ResponseMsg.ERROR}


class ParamError:

    @staticmethod
    def error(msg: AnyStr) -> Dict:
        return {"code": ResponseCode.PARAMS_ERROR, "data": None, "msg": msg}


class AuthError:

    @staticmethod
    def error() -> Dict:
        return {"code": ResponseCode.AUTH_ERROR, "data": None, "msg": ResponseMsg.AUTH_ERROR}


if __name__ == '__main__':
    print(MyResponse.success())
