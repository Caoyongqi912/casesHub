import enum


class CaseLevel(enum.Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class CaseTag(enum.Enum):
    COMMENT = "常规"
    SMOCK = "冒烟"


class CaseType(enum.Enum):
    COMMENT = "功能"
    API = "接口"
    PERF = "性能"


class CaseStatus(enum.Enum):
    QUEUE = 1
    TESTING = 2
    BLOCK = 3
    SKIP = 4
    PASS = 5
    FAIL = 6
    CLOSE = 7


class BugLevel(enum.Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class BugType(enum.Enum):
    ONLINE = 1
    OPTIMIZE = 2
    FAIL = 3


class BugStatus(enum.Enum):
    OPEN = 1
    CLOSE = 2
    BLOCK = 3


class Gender(enum.Enum):
    MALE = 1
    FEMALE = 0


class UserTag(enum.Enum):
    QA = 1
    PR = 2
    DEV = 3
    ADMIN = 0
