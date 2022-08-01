# @Time : 2022/7/6 22:32 
# @Author : cyq
# @File : myResponse.py
# @Software: PyCharm
# @Desc: 返回自定义
from typing import Any
from flask import jsonify
from Enums.errorCode import ResponseCode, ResponseMsg


def make_response(code: ResponseCode, data: Any, msg: ResponseMsg) -> jsonify:
    return jsonify({"code": code, "data": data, "msg": msg})


class MyResponse:

    @staticmethod
    def success(data: Any = None) -> make_response:
        return make_response(ResponseCode.SUCCESS, data, ResponseMsg.OK)

    @staticmethod
    def error(code: ResponseCode) -> make_response:
        return make_response(code, None, ResponseMsg.ERROR)

    @staticmethod
    def not_find() -> make_response:
        return make_response(ResponseCode.NOT_FOUND, None, ResponseMsg.NOT_FOUND)


class ParamError:

    @staticmethod
    def error(msg: ResponseMsg) -> make_response:
        return make_response(ResponseCode.PARAMS_ERROR, None, msg)


class AuthError:

    @staticmethod
    def error() -> make_response:
        return make_response(ResponseCode.AUTH_ERROR, None, ResponseMsg.AUTH_ERROR)


if __name__ == '__main__':
    print(MyResponse.success())
