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
    a = [
        {
            "step": 1,
            "setup": "im setup",
            "do": "to do ...",
            "exp": "exp ....",

        },
        {
            "step": 3,
            "setup": "im setup",
            "do": "to do ...",
            "exp": "exp ....",

        },
        {
            "step": 2,
            "setup": "im setup",
            "do": "to do ...",
            "exp": "exp ....",

        }
    ]
    # a.sort(key=lambda s:s['step'])
    # print(a)
    t = {'steps': '1.打开baidu.com\n2.录入py\n3.校验内容', 'exp': '1.打开成功\n2.录入成功\n3.校验成功'}
    print(dict(zip(t.get("steps"), t.get("exp"))))
