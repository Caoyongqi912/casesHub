# @Time : 2022/7/15 20:10 
# @Author : cyq
# @File : classTest.py 
# @Software: PyCharm
# @Desc:
import json
import re


class Test:
    name = "cyq"
    desc = "desc"

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

    def __str__(self):
        return json.dumps({"name": self.name,
                           "desc": self.desc})

    def __setattr__(self, key, value):
        self.__dict__[key] = "set + " + value
        print(self.__dict__)


if __name__ == '__main__':
    import uuid
    print(uuid.uuid4())
    print(uuid.uuid4())