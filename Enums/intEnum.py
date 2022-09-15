# @Time : 2022/9/15 20:03 
# @Author : cyq
# @File : intEnum.py
# @Software: PyCharm
# @Desc:
from typing import TypeVar, Generic, Union
import sqlalchemy as sql
from enum import Enum
from Enums.baseEnum import Base

enumType = TypeVar("enumType", bound=Base)


class IntEnum(sql.types.TypeDecorator):
    impl = sql.Integer
    cache_ok = True

    def __init__(self, enumType: Generic[enumType], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__enumType = enumType

    def process_bind_param(self, value, dialect) -> Union[Enum, int]:
        """
        :param value:
        :param dialect:
        :return:
        """
        if isinstance(value, self.__enumType):
            return value.value
        else:
            return value

    def process_result_value(self, value, dialect):
        """
        :param value: Enum value
        :param dialect:
        :return: Enum name
        """
        e = self.__enumType(value)
        return e.name
