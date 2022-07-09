# @Time : 2022/7/6 23:09 
# @Author : cyq
# @File : myException.py 
# @Software: PyCharm
# @Desc: 自定义错误
import json
from flask import Response
from werkzeug.exceptions import HTTPException
from typing import Dict, AnyStr

from Comment.myResponse import MyResponse, ParamError
from Enums.errorCode import ResponseCode
from Utils.log import MyLog


class MyException(HTTPException):
    """
    自定义 Exception 基类
    """
    log = MyLog.get_log(__file__)

    def __init__(self, response: Dict = None):
        """
        :param response: MyResponse
        """
        if response:
            self._response = response
        else:
            self._response = MyResponse.error(ResponseCode.SERVER_ERROR)
        super(MyException, self).__init__(response=self.__make_response())

    def __make_response(self) -> Response:
        """
        自定义返回 response
        :return: Response
        """
        self.log.error(self._response)
        return Response(json.dumps(self._response), mimetype="application/json")


class ParamException(MyException):

    def __init__(self, msg: AnyStr):
        self._response = ParamError.error(msg)
