# @Time : 2022/7/6 22:30 
# @Author : cyq
# @File : myRequestParseUtil.py
# @Software: PyCharm
# @Desc:  自定义参数校验
from typing import AnyStr, Dict, Any, List, ClassVar, Union, NoReturn

from flask import request
from Comment.myResponse import ResponseMsg
from Comment.myException import ParamException
from Utils.myLog import MyLog

log = MyLog.get_log(__file__)


class MyRequestParseUtil:

    def __init__(self, location: AnyStr = "json"):
        """
        :param location:  "json" -> application/json | "values"  -> query default json
        """

        self.location = location
        self.args = []
        try:
            self.body = getattr(request, self.location, {})
        except Exception as e:
            log.error(e)
            raise ParamException(ResponseMsg.REQUEST_BODY_ERROR)

    def add(self, **kwargs):
        """
        添加请求数据与数据类型
        :param kwargs: name
        :param kwargs: type
        :param kwargs: required bool
        :param kwargs: default
        :param kwargs: choices
        :param kwargs: isExist=cls  put 请求主键还会再校验一次 不需要添加 添加外键
        :param kwargs: unique  put 不要添加


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

        self.body = dict(self.body)
        for kw in self.args:
            # 分页数据
            if kw["name"] == "page":
                self.body[kw["name"]] = self.__verify_page(self.body.get(kw['name'], kw.get("default")))
            if kw['name'] == "limit":
                self.body[kw["name"]] = self.__verify_limit(self.body.get(kw["name"], kw.get("default")))
            if kw['name'] == "by":
                self.__verify_by(self.body.get(kw['name']), kw.get("target"))

            #  必传
            if kw['required'] is True:
                self.__verify_empty(self.body.get(kw["name"]), kw["name"])
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
                self.__verify_choices(self.body.get(kw["name"]), kw['choices'], kw['name'])
            #  校验cls ID
            if kw.get("isExist"):
                cls = kw.get("isExist")
                cls.get(self.body.get(kw['name']), kw['name'])
            #   校验cls 重名
            if kw.get("unique"):
                cls = kw.get("unique")
                cls.verify_unique(**{kw['name']: self.body.get(kw['name'])})

        return self.body

    def __verify_by(self, by: AnyStr, cls: Any):
        """
        orderby columns 字段校验 如果不存在 返回None
        :param by: filed
        :param cls: entity
        :return:
        """
        columns = [c.name for c in cls.__table__.columns]
        if by not in columns:
            return None

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

    def __verify_empty(self, target: AnyStr, filed: AnyStr):
        """
        校验参数是否为空
        :param target:  目标值
        :param filed:   参数名
        :raise: ParamException
        """
        if target is None or target == "":
            raise ParamException(ResponseMsg.empty(filed))

    def __verify_type(self, target: Any, t: type, ):
        """
        校验类型
        :param target: 目标值
        :param t: 期望类型
        :raise: ParamException
        """
        if not isinstance(target, t):
            raise ParamException(ResponseMsg.error_type(target, t))

    def __verify_choices(self, target: Any, choices: List, filedName: AnyStr):
        """
        区间校验
        :param target: 目标值
        :param choices:
        :raise: ParamException
        """

        if target not in choices:
            raise ParamException(ResponseMsg.error_val(filedName, choices))
