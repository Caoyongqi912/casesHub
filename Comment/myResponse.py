# @Time : 2022/7/6 22:32 
# @Author : cyq
# @File : myResponse.py
# @Software: PyCharm
# @Desc: 返回自定义
from typing import Any, Dict
from flask import jsonify
from Enums import ResponseCode, ResponseMsg


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
    def req_err() -> make_response:
        return make_response(ResponseCode.PARAMS_ERROR, None, ResponseMsg.REQUEST_BODY_ERROR)

    @staticmethod
    def server_error() -> Dict:
        return {"code": ResponseCode.SERVER_ERROR, "data": None, "msg": ResponseMsg.ERROR}

    @staticmethod
    def not_find() -> make_response:
        return make_response(ResponseCode.NOT_FOUND, None, ResponseMsg.NOT_FOUND)

    @staticmethod
    def limiter_err(msg: str):
        return {"code": ResponseCode.LIMITER_ERROR, "data": None, "msg": msg}


class ParamError:

    @staticmethod
    def error(msg: ResponseMsg) -> dict:
        return {"code": ResponseCode.PARAMS_ERROR, "data": None, "msg": msg}


class AuthError:

    @staticmethod
    def error() -> dict:
        return {"code": ResponseCode.AUTH_ERROR, "data": None, "msg": ResponseMsg.AUTH_ERROR}
