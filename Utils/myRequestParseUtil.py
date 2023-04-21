# @Time : 2022/7/6 22:30 
# @Author : cyq
# @File : myRequestParseUtil.py
# @Software: PyCharm
# @Desc:  自定义参数校验
import enum
import json
from json import JSONDecodeError
from typing import AnyStr, Dict, Any, List, Union, TypeVar, Generic, NoReturn, Optional, Type
from flask import request
from Comment.myException import ParamException
from Models.CaseModel.caseModel import Cases
from Models.base import Base
from Utils.myLog import MyLog
from Enums import ResponseMsg
from Enums.baseEnum import BaseEnum

log = MyLog.get_log(__file__)

clsType = TypeVar("clsType", bound=Base)
enumType = TypeVar("enumType", bound=BaseEnum)
StrType = TypeVar("StrType", bound=str)


class MyRequestParseUtil:
    """
    请求参数解析工具类。该类用于验证请求参数的正确性，
    支持参数类型校验、必填项校验、区间校验、枚举校验、分页参数校验等。
    """

    def __init__(self, location: str = "json"):
        """
        :param location:  "json" -> application/json | "values"  -> query default json
        """

        self.location: str = location
        self.args: List = []
        try:
            self.body = dict(getattr(request, self.location, {}))
        except Exception as e:
            log.error(repr(e))
            raise ParamException(ResponseMsg.REQUEST_BODY_ERROR)

    def add(self, **kwargs):
        """
        添加请求数据与数据类型
        :param kwargs: name  参数名称
        :param kwargs: type  参数类型
        :param kwargs: required bool default false 是否必传
        :param kwargs: default 默认值
        :param kwargs: choices 是否在区间内
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

    def page(self, cls: Generic[clsType]) -> Dict[str, Any]:
        """
        分页参数校验
        pageSize ： if request get pageSize  else 10
        current ： if request get current  else 1
        sort : if request get sort  else None
        like select * from cls order by (sort)
        :param cls: 目标类
        :return: Dict
        """
        body = dict(self.body)
        pageSize = body.pop("pageSize") if body.get("pageSize") else 10
        current = body.pop("current") if body.get("current") else 1
        sort = body.pop("sort") if body.get("sort") else None

        pageInfo = {
            "pageSize": self._verify_pageSize(pageSize),
            "current": self._verify_current(current),
            "sort": self._verify_sort(cls, sort),
        }
        pageInfo.update(body)
        return pageInfo

    @property
    def parse_args(self) -> Dict:
        """
        参数校验
        :return: self.body
        """

        for kw in self.args:
            #  必传
            if kw['required'] is True:
                self._verify_empty(self.body.get(kw["name"]), kw["name"])
            # 非必传
            else:
                # 未传
                if self.body.get(kw["name"]) is None:
                    if kw.get('default'):
                        self.body[kw['name']] = kw.get('default')
                    else:
                        continue

            self._verify_type(self.body.get(kw["name"]), kw['type'], kw['name'])

            if kw.get("choices"):
                self._verify_choices(self.body.get(kw["name"]), kw['choices'], kw['name'])
            #  校验cls ID
            if kw.get("isExist"):
                cls: clsType = kw.get("isExist")
                cls.get(self.body.get(kw['name']), kw['name'])
            #   校验cls 重名
            if kw.get("unique"):
                cls = kw.get("unique")
                cls.verify_unique(**{kw['name']: self.body.get(kw['name'])})

            # 枚举校验
            if kw.get("enum"):
                self.body[kw['name']] = self._verify_enum(kw['enum'], self.body.get(kw["name"]), kw["name"])

        return self.body

    @staticmethod
    def _verify_enum(ENUM: Generic[enumType], name: str, param: str) -> enum.Enum:
        """
        校验枚举值
        :param ENUM: 枚举类
        :param name: name
        :param param
        :return: enum
        """
        vs: List[int] = ENUM.names()
        if name not in vs:
            raise ParamException(ResponseMsg.error_val(param, vs))
        return ENUM.getValue(name)

    @staticmethod
    def _verify_empty(target: AnyStr, filed: AnyStr) -> NoReturn:
        """
        校验参数是否为空
        :param target:  目标值
        :param filed:   参数名
        :raise: ParamException
        """
        if target is None or target == "":
            raise ParamException(ResponseMsg.empty(filed))

    @staticmethod
    def _verify_type(target: Any, t: Type[StrType], param: str) -> NoReturn:
        """
        校验类型
        :param target: 目标值
        :param t: 期望类型
        :param param:字段名
        :raise: ParamException
        """
        if not isinstance(target, t):
            raise ParamException(ResponseMsg.error_type(param, t))

    @staticmethod
    def _verify_choices(target: Any, choices: List, filedName: AnyStr) -> NoReturn:
        """
        区间校验
        :param target: 目标值
        :param choices:
        :raise: ParamException
        """

        if target not in choices:
            raise ParamException(ResponseMsg.error_val(filedName, choices))

    @staticmethod
    def _verify_current(current: int | str) -> int:
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
    def _verify_pageSize(pageSize: int | str) -> int:
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
    def _verify_sort(cls: Generic[clsType], sort: str = None) -> Optional[Dict[str, Any]]:
        """

        verify sort value in  cls.__table__.columns if not return None
        :param sort: str | None  Generic[clsType]
        :param cls: Generic[clsType]
        :return:  Optional[Dict[str,Any]]
        """
        if isinstance(sort, str):
            try:
                sort = json.loads(sort)
            except JSONDecodeError as e:
                log.error(repr(e))
                raise ParamException(ResponseMsg.error_param("sort"))
            for k, v in sort.items():
                if k not in cls.columns() or v not in ['descend', "ascend"]:
                    return None
            return sort
        else:
            return sort
