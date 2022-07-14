# @Time : 2022/7/6 22:30 
# @Author : cyq
# @File : myRequestParseUtil.py
# @Software: PyCharm
# @Desc:  自定义参数校验
from typing import AnyStr, Dict, Any, List

from flask import request
from Comment.myResponse import ResponseMsg
from Comment.myException import ParamException


class MyRequestParseUtil:

    def __init__(self, location: AnyStr = "json"):
        """
        :param location: location ["json","values"] default json
        """

        self.location = location
        self.args = []
        self.body = dict(getattr(request, self.location, {}))

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
            # 分页数据
            if kw["name"] == "page":
                self.body[kw["name"]] = self.__verify_page(self.body.get(kw['name'], kw.get("default")))
            if kw['name'] == "limit":
                self.body[kw["name"]] = self.__verify_limit(self.body.get(kw["name"], kw.get("default")))

            #  必传
            if kw['required'] is True:
                self.__verify_empty(self.body.get(kw["name"]))
            # 非必传
            else:
                # 未传
                if self.body.get(kw["name"]) is None:
                    if kw.get('default'):
                        self.body[kw['name']] = kw.get('default')
                    else:
                        continue
            self.__verify_type(self.body.get(kw["name"]), kw['type'])

            if kw.get("choices"):
                self.__verify_choices(self.body.get(kw["name"]), kw['choices'])

        return self.body

    def __verify_page(self, page: AnyStr) -> int:
        """
        page校验
        :param page: 页
        :raise: ParamException
        :return page
        """
        if int(page) < 1:
            raise ParamException(ResponseMsg.error_param("page", "must > 0"))
        return page

    def __verify_limit(self, limit: AnyStr) -> int:
        """
        limit 校验
        :param limit: 行
        :return: limit
        """
        if int(limit) < 0:
            raise ParamException(ResponseMsg.error_param("limit", "must > 0"))
        return limit

    def __verify_empty(self, target: AnyStr):
        """
        校验参数是否为空
        :param target:  目标
        :raise: ParamException
        """
        if target is None or target == "":
            raise ParamException(ResponseMsg.empty(target))

    def __verify_type(self, target: Any, t: type, ):
        """
        校验类型
        :param target: 目标值
        :param t: 期望类型
        :raise: ParamException
        """
        if not isinstance(target, t):
            raise ParamException(ResponseMsg.error_type(target, t))

    def __verify_choices(self, target: Any, choices: List):
        """
        区间校验
        :param target: 目标值
        :param choices:
        :raise: ParamException
        """

        if target not in choices:
            raise ParamException(ResponseMsg.error_val(target, choices))
