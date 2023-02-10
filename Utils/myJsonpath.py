# @Time : 2022/9/17 15:29 
# @Author : cyq
# @File : myJsonpath.py 
# @Software: PyCharm
# @Desc:
from json import JSONDecodeError
from typing import Any, Dict
from jsonpath import jsonpath
from requests import Response
from Utils import MyLog

log = MyLog.get_log(__file__)


class MyJsonPath:

    def __init__(self, response: Response, expr: str):
        """
        :param response Response
        :param expr
        """
        self.response = response
        self.expr = expr

    @property
    def value(self) -> Any:
        """
        jsonpath 解析
        :return: Any
        """
        try:
            target = self.response.json()
            result = jsonpath(target, self.expr)
            if result:
                return result[0]
            else:
                return
        except JSONDecodeError as e:
            log.error(repr(e))
            return self.response.text
