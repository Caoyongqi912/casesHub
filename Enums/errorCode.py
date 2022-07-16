# @Time : 2022/7/6 22:35 
# @Author : cyq
# @File : errorCode.py
# @Software: PyCharm
# @Desc: response data
from enum import Enum
from typing import AnyStr, Any, List


class ResponseCode:
    DATA = None
    SUCCESS = 0
    SERVER_ERROR = 100
    PARAMS_ERROR = 1000
    AUTH_ERROR = 2000


class ResponseMsg:
    OK = "ok !"
    ERROR = "server error !"
    REQUEST_BODY_ERROR = "request body error !"
    AUTH_ERROR = " auth error No permission !"

    @staticmethod
    def miss(target: AnyStr) -> AnyStr:
        return f"miss {target} arg !"

    @staticmethod
    def empty(target: AnyStr) -> AnyStr:
        return f"{target} cant be empty or ''!"

    @staticmethod
    def error_type(target: AnyStr, t: type) -> AnyStr:
        return f"{target} must be {t} !"

    @staticmethod
    def error_val(target: Any, choices: List[Any]) -> AnyStr:
        return f"{target} must in {choices} !"

    @staticmethod
    def error_param(target: Any, msg: AnyStr):
        return f"{target} err ! {msg}"

    @staticmethod
    def no_existent(target: AnyStr) -> AnyStr:
        return f"{target} not existent !"

    @staticmethod
    def already_exist(target: AnyStr) -> AnyStr:
        return f"{target} already exist !"
