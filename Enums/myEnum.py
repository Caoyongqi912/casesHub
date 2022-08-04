from enum import Enum


class CaseLevel(Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class CaseTag(Enum):
    COMMENT = "常规"
    SMOCK = "冒烟"


class CaseType(Enum):
    COMMENT = "功能"
    API = "接口"
    PERF = "性能"


class CaseStatus(Enum):
    QUEUE = 1
    TESTING = 2
    BLOCK = 3
    SKIP = 4
    PASS = 5
    FAIL = 6
    CLOSE = 7


class BugLevel(Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class BugType(Enum):
    ONLINE = 1
    OPTIMIZE = 2
    FAIL = 3


class BugStatus(Enum):
    OPEN = 1
    CLOSE = 2
    BLOCK = 3


class Gender(Enum):
    MALE = 1
    FEMALE = 0


class UserTag(Enum):
    QA = 1
    PR = 2
    DEV = 3
    ADMIN = 0
