# @Time : 2022/7/6 22:30 
# @Author : cyq
# @File : myRequestParseUtil.py
# @Software: PyCharm
# @Desc:  自定义参数校验
import enum
from typing import AnyStr, Dict, Any, List, Union
from flask import request
from Comment.myException import ParamException
from Enums.errorCode import ResponseMsg
from Utils.myLog import MyLog

log = MyLog.get_log(__file__)


class MyRequestParseUtil:

    def __init__(self, location: str = "json"):
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
        :param kwargs: enum 枚举字段 返回其枚举值
        :param kwargs: page 页
        :param kwargs: limit 数量
        :param kwargs: target 类

        """
        # 默认类型为字符
        if not kwargs.get("type"):
            kwargs.setdefault("type", str)
        # 默认非必传
        if not kwargs.get("required"):
            kwargs.setdefault("required", False)
        self.args.append(kwargs)

    def page(self, cls: Any) -> Dict:
        """
        分页参数校验
        :param pageSize:    pageSize
        :param current:    current
        :param sort:    order_by(sort)
        :param filter:  filter_by(** filter_key)
        :return: Dict
        """
        body = dict(self.body)
        pageSize = body.pop("pageSize") if body.get("pageSize") else 10
        current = body.pop("current") if body.get("current") else 1
        sort = body.pop("sort") if body.get("sort") else 1
        pageInfo = {
            "pageSize": self.__verify_pageSize(pageSize),
            "current": self.__verify_current(current),
            "sort": self.__verify_sort(sort, cls),
            "filter_key": self.__verify_filterKey(body, cls)
        }
        return pageInfo

    def parse_args(self) -> Dict:
        """
        参数校验
        :return: self.body
        """
        self.body = dict(self.body)
        for kw in self.args:
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

            # 枚举校验
            if kw.get("enum"):
                self.body[kw['name']] = self.__verify_enum(kw['enum'], self.body.get(kw["name"]))
        return self.body

    @staticmethod
    def __verify_enum(ENUM: enum, value: int):
        """
        校验枚举值
        :param ENUM: 枚举类
        :param value: 整形值
        :return: enum
        """
        vs = [v.value for v in ENUM]
        if value not in vs:
            raise ParamException(ResponseMsg.error_val(value, vs))
        return ENUM.e(value)

    @staticmethod
    def __verify_empty(target: AnyStr, filed: AnyStr):
        """
        校验参数是否为空
        :param target:  目标值
        :param filed:   参数名
        :raise: ParamException
        """
        if target is None or target == "":
            raise ParamException(ResponseMsg.empty(filed))

    @staticmethod
    def __verify_type(target: Any, t: type):
        """
        校验类型
        :param target: 目标值
        :param t: 期望类型
        :raise: ParamException
        """
        if not isinstance(target, t):
            raise ParamException(ResponseMsg.error_type(target, t))

    @staticmethod
    def __verify_choices(target: Any, choices: List, filedName: AnyStr):
        """
        区间校验
        :param target: 目标值
        :param choices:
        :raise: ParamException
        """

        if target not in choices:
            raise ParamException(ResponseMsg.error_val(filedName, choices))

    @staticmethod
    def __verify_current(current: int | str) -> int:
        """
        page校验
        :param current: 页
        :raise: ParamException
        :return current
        """
        if isinstance(current, str):
            current = int(current)
        if current < 1:
            raise ParamException(ResponseMsg.error_param("current", "must > 0"))
        return current

    @staticmethod
    def __verify_pageSize(pageSize: int | str) -> int:
        """
        pageSize 校验
        :param pageSize: 行
        :return: pageSize
        """
        if isinstance(pageSize, str):
            pageSize = int(pageSize)
        if pageSize < 0:
            raise ParamException(ResponseMsg.error_param("pageSize", "must > 0"))
        return pageSize

    @staticmethod
    def __verify_sort(sort: str, cls: Any) -> Union[None, str]:
        columns = [c.name for c in cls.__table__.columns]
        if sort not in columns:
            return None
        return sort

    @staticmethod
    def __verify_filterKey(key: Dict | None, cls: Any) -> Union[Dict, None]:
        """
        :key like {username:"ADMIN,tag:"xx",other:"",} => {username:"ADMIN}
        :param key:
        :param cls:
        :return:
        """
        if not key:
            return key

        columns = [c.name for c in cls.__table__.columns]
        from copy import deepcopy
        kk = deepcopy(key)
        for k, v in kk.items():
            if k not in columns or v == "":
                key.pop(k)

        return key
