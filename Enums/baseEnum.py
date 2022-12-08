# @Time : 2022/9/15 20:04 
# @Author : cyq
# @File : baseEnum.py 
# @Software: PyCharm
# @Desc:
from enum import Enum


class BaseEnum(Enum):

    @classmethod
    def e(cls, value: int) -> Enum:
        """
        获取枚举的value
        :param value:
        :return:
        """
        for k, v in cls.__members__.items():
            if v.value == value:
                return v

    @classmethod
    def getValue(cls, name: str) -> int:
        for k, v in cls.__members__.items():
            if v.name == name:
                return v.value

    @classmethod
    def values(cls):
        return [v.value for v in cls]

    @classmethod
    def names(cls):
        return [v.name for v in cls]

    @classmethod
    def getName(cls, value: int) -> str:
        for k, v in cls.__members__.items():
            if v.value == value:
                return v.name



