# @Time : 2022/7/6 23:09 
# @Author : cyq
# @File : myException.py 
# @Software: PyCharm
# @Desc: 自定义错误
import json
from flask import Response
from werkzeug.exceptions import HTTPException
from typing import Dict, AnyStr
from Utils import MyLog
from .myResponse import MyResponse, ParamError, AuthError

log = MyLog.get_log(__file__)


class MyException(HTTPException):
    """
    自定义 Exception 基类
    """

    def __init__(self, response: Dict | str = None):
        """
        :param response: MyResponse
        """
        if response:
            self._response = response
        else:
            self._response = MyResponse.server_error()
        super(MyException, self).__init__(response=self._make_response())

    def _make_response(self) -> Response:
        """
        自定义返回 response
        :return: Response
        """
        log.error(self._response)
        if isinstance(self._response, str):
            return Response(json.dumps(MyResponse.limiter_err(self._response)), mimetype="application/json", status=500)

        return Response(json.dumps(self._response), mimetype="application/json", status=500)


class ParamException(HTTPException):

    def __init__(self, msg: AnyStr):
        self._response = ParamError.error(msg)
        super(ParamException, self).__init__(response=self._make_response())

    def _make_response(self) -> Response:
        """
        自定义返回 response
        :return: Response
        """
        log.error(self._response)
        return Response(json.dumps(self._response), mimetype="application/json")


class AuthException(HTTPException):

    def __init__(self):
        self._response = AuthError.error()
        super(AuthException, self).__init__(response=self._make_response())

    def _make_response(self) -> Response:
        """
        自定义返回 response
        :return: Response
        """
        log.error(self._response)
        return Response(json.dumps(self._response), mimetype="application/json")
