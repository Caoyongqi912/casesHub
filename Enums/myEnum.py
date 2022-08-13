from enum import Enum
import sqlalchemy as sql



class Base(Enum):

    @classmethod
    def e(cls, value: int) -> Enum:
        for k, v in cls.__members__.items():
            if v.value == value:
                return v

    @classmethod
    def values(cls):
        return [v.value for v in cls]


class CaseLevel(Base):
    P1 = 1
    P2 = 2
    P3 = 3
    P4 = 4


class CaseTag(Base):
    COMMENT = 1
    SMOCK = 2


class CaseType(Base):
    COMMENT = 1
    API = 2
    PERF = 3


class CaseStatus(Base):
    QUEUE = 1
    TESTING = 2
    BLOCK = 3
    SKIP = 4
    PASS = 5
    FAIL = 6
    CLOSE = 7


class BugLevel(Base):
    P1 = 1
    P2 = 2
    P3 = 3
    P4 = 4


class BugType(Base):
    ONLINE = 1
    OPTIMIZE = 2
    FAIL = 3


class BugStatus(Base):
    OPEN = 1
    CLOSE = 2
    BLOCK = 3


class Gender(Base):
    MALE = 1
    FEMALE = 0


class UserTag(Base):
    QA = 1
    PR = 2
    DEV = 3
    ADMIN = 0


class IntEnum(sql.types.TypeDecorator):
    impl = sql.Integer
    cache_ok = True

    def __init__(self, enumType, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__enumType = enumType

    def process_bind_param(self, value, dialect):
        """
        :param value:
        :param dialect:
        :return:
        """
        return value

    def process_result_value(self, value, dialect):
        """
        :param value: Enum value
        :param dialect:
        :return: Enum name
        """
        return self.__enumType(value).name

