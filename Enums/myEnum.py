from Enums.baseEnum import BaseEnum


class CaseLevel(BaseEnum):
    P1 = 1
    P2 = 2
    P3 = 3
    P4 = 4


class CaseAPIStatus(BaseEnum):
    DEBUG = 1
    CLOSE = 2
    NORMAL = 3


class CaseTag(BaseEnum):
    COMMENT = 1
    SMOCK = 2


class CaseType(BaseEnum):
    COMMENT = 1
    API = 2
    PERF = 3


class CaseStatus(BaseEnum):
    QUEUE = 1
    TESTING = 2
    BLOCK = 3
    SKIP = 4
    PASS = 5
    FAIL = 6
    CLOSE = 7


class BugLevel(BaseEnum):
    P1 = 1
    P2 = 2
    P3 = 3
    P4 = 4


class BugType(BaseEnum):
    ONLINE = 1  # 线上BUG
    OPTIMIZE = 2  # 优化BUG
    FAIL = 3  # 常规缺陷


class BugStatus(BaseEnum):
    OPEN = 1
    CLOSE = 2
    BLOCK = 3


class Gender(BaseEnum):
    MALE = 1
    FEMALE = 0


class UserTag(BaseEnum):
    P1 = 1
    P2 = 2
    P3 = 3
    ADMIN = 0


class FileEnum(BaseEnum):
    AVATAR = "avatar"
    BUG = "bug"
    Excel = "excel"


EnumDict = {
    "case_level": CaseLevel,
    "case_tag": CaseTag,
    "case_type": CaseType,
    "status": CaseStatus,
    "gender": Gender,
    "tag": UserTag

}


class ExtractTargetEnum(BaseEnum):
    JSON = "1"
    HEADER = "2"


if __name__ == '__main__':
    print(CaseType.getValue("dsf"))
