# @Time : 2022/7/6 22:30 
# @Author : cyq
# @File : requestParseUtil.py
# @Software: PyCharm
# @Desc:  自定义参数校验
from typing import AnyStr, Dict

from flask import request
from Comment.myResponse import ResponseMsg
from Comment.myException import ParamException


class MyRequestParseUtil:

    def __init__(self, location: AnyStr = "json"):
        """
        :param location: location default json
        """
        self.location = location
        self.args = []
        self.body = getattr(request, self.location, {})

    def add(self, **kwargs):
        """
        添加请求数据与数据类型
        :param kwargs: name type required default choices
        """
        # 默认类型为字符
        if not kwargs.get("type"):
            kwargs.setdefault("type", str)
        # 默认非必传
        if not kwargs.get("required"):
            kwargs.setdefault("required", False)
        self.args.append(kwargs)

    def parse_args(self) -> Dict:
        """
        参数校验
        :return: self.body
        """
        if self.body is None:
            raise ParamException(ResponseMsg.REQUEST_BODY_EMPTY)
        for kw in self.args:
            # 设定 必传 但未传
            if kw['required'] is True and not self.body.get(kw["name"]):
                raise ParamException(ResponseMsg.empty(kw["name"]))
            # 传空字符
            if self.body.get(kw['name']) == "":
                raise ParamException(ResponseMsg.empty(kw["name"]))
            # 传参未按照定义类型
            if not isinstance(self.body[kw['name']], kw['type']):
                raise ParamException(ResponseMsg.error_type(kw["name"], kw['type']))
            # 传参未按照指定区间
            if kw.get('choices'):
                if self.body[kw['name']] not in kw['choices']:
                    raise ParamException(ResponseMsg.error_val(kw["name"], kw['choices']))
            # 未传且设定默认
            if kw.get("default") and self.body.get(kw['name']) is None:
                self.body[kw['name']] = kw.get('default')

        return self.body
