# @Time : 2022/9/17 10:30 
# @Author : cyq
# @File : myTools.py 
# @Software: PyCharm
# @Desc:
import re
from typing import List, Dict, Any, Mapping
from copy import deepcopy


class MyTools:

    # def __init__(self, extracts: List = None, headers: List = None, params: List = None, body: List = None,
    #              auth: Dict = None):
    #     self.extracts = extracts
    #     self.headers = headers
    #     self.params = params
    #     self.body = body
    #     self.auth = auth

    @staticmethod
    def list2Dict(extracts: List | None = None, params: List[Dict[str, str]] | None = None, ) -> Dict[str, str] | None:
        """
        1、参数转换 extracts ↓
       [{'id': 1677578978008, 'key': 'Authorization', 'value': '{{token}}'}]
        ==>
        {"Content-Type":"application/json",token:  {{token}}}
        2、提取转换  params  ↓
        [{'token': 0}]
        ===> 返回
        {"Content-Type":"application/json",token:0}
        :param extracts: [{token:xxx}]
        :param params:   [{"key":"Content-Type","val":"application/json"},{"key":"token","val":"{{token}}"}]
        :return:
        """
        if not params:
            return params
        D = {}
        for _ in params:
            D[_["key"]] = _["value"]
        DD = deepcopy(D)
        for k, v in DD.items():
            v = MyTools.getValue(extracts, v)
            D[k] = v
        return D

    @staticmethod
    def kw2str(**kwargs):
        """
        {name:cyq,age:13}
        ->
        name = cyq or age = 13
        :param kwargs:
        :return:
        """
        _ = ""
        for k, v in kwargs.items():
            _ += f"`{k}`" + " = " + f"'{str(v)}'" + ' or '
        return _.strip(" or ")

    @staticmethod
    def getValue(extracts: List[Mapping[str, Any]], target: str) -> Any:
        """
        {{value}} -> value
        :param target:
        :param extracts
        :return:
        """
        if isinstance(target, str) and "{{" in target and "}}" in target:
            val = re.findall(r"\{\{(.*?)\}\}", target)[0]
            _ = target.replace("{{", "").replace("}}", "")
            for ext in extracts:
                v = ext.get(val)
                if v is not None:
                    return _.replace(val, str(v))
                else:
                    continue
        else:
            return target

    @staticmethod
    def auth(extracts: List[Mapping[str, Any]] | None = None, authBody: Dict[str, str] | None = None) -> Dict | None:
        """
        处理auth 请求
        :param extracts: [{token:xxx}]
        :param authBody: {username:{{token},password}
        :return:{"username":token|mame,""password":"" | "xx"}
        """
        if authBody:
            username = MyTools.getValue(extracts, authBody.get("username", ""))
            password = MyTools.getValue(extracts, authBody.get("password", ""))
            return {"username": username, "password": password}
        return

    @staticmethod
    def search(nums: List[int], target: int) -> bool:
        """
        二分查找 存在返回True 不存在返回False
        :param nums:
        :param target:
        :return:bool
        """
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (right - left) // 2 + left
            num = nums[mid]
            if num == target:
                return True
            elif num > target:
                right = mid - 1
            else:
                left = mid + 1
        return False

    @staticmethod
    def pinyin(word):
        import pypinyin
        s = ''
        for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
            s += ''.join(i)
        return s

    @staticmethod
    def list2Tree(data: List):
        """
        列表转树
        :param data:
        :return:
        """
        mapping: dict = dict(zip([i['id'] for i in data], data))
        c = []
        for d in data:
            parent: dict = mapping.get(d['parentID'])
            if parent is None:
                c.append(d)
            else:
                children: list = parent.get("children")
                if not children:
                    children = []
                children.append(d)
                parent.update({"children": children})
        return c

    @classmethod
    def to_ms(cls, number: int | float) -> str:
        return f"{round(number * 1000, 2)}ms"


if __name__ == '__main__':
    e = [{'id': 1677578978008, 'key': 'Authorization', 'value': '{{token}}'}]
    p = [{'token': 0}]

    MyTools.list2Dict(p, e)
