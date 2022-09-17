# @Time : 2022/9/17 15:29 
# @Author : cyq
# @File : myJsonpath.py 
# @Software: PyCharm
# @Desc:
from typing import Any, Dict

from requests import Response
from jsonpath import jsonpath


class MyJsonPath:

    def __init__(self, response: Dict[str, Any], expr: str):
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
        return jsonpath(self.response, self.expr)[0]
