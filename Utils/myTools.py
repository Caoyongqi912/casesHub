# @Time : 2022/9/17 10:30 
# @Author : cyq
# @File : myTools.py 
# @Software: PyCharm
# @Desc:
import copy
import re
from typing import List, Dict, Any, Mapping
from copy import deepcopy
from httpx import Response as HTTPxResponse
from requests import Response as RequestResponse

from Utils.myJsonpath import MyJsonPath


class MyTools:

    @staticmethod
    def list2Dict(extracts: List | None = None, params: List[Dict[str, str]] | None = None, ) -> Dict[str, str] | None:
        """
        1、参数转换 extracts ↓
        [{'id': 1677578978008, 'key': 'Authorization', 'value': 'hahah - {{token}}'}]
        ==>
        {"Content-Type":"application/json","Authorization": "{{token}}"}
        :param extracts: [{'id': 1679377815262, 'key': 'token', 'val': 'im token', 'target': '1'}]
        :param params:   [{"key":"Content-Type","val":"application/json"},{"key":"token","val":"{{token}}"}]
        :return:
        """
        if not params:
            return params
        D = {}
        for _ in params:
            D[_["key"].strip()] = _["value"]
        DD = deepcopy(D)
        if extracts:  # 如果存在待提取的参数
            for k, v in DD.items():
                v = MyTools.getValue(extracts, v)
                D[k] = v
        return D

    @staticmethod
    def getValue(extracts: List[Mapping[str, Any]], target: str) -> Any:
        """
        target :'hahah - {{token}}
        提取转换   extracts ↓
        target :'hahah - im token'
        ===> 返回
        :param target: 'hahah - {{token}}
        :param extracts:[{'id': 1679377815262, 'key': 'token', 'val': 'im token', 'target': '1'}]
        :return:
        """

        # 如果是字符串 并且符合{{}}规则
        if isinstance(target, str) and "{{" in target and "}}" in target:
            val = re.findall(r"\{\{(.*?)\}\}", target)[0]
            _ = target.replace("{{", "").replace("}}", "")
            for ext in extracts:
                if ext.get("key") == val:
                    v = ext.get("val")
                    if v is not None:
                        return _.replace(val, str(v))
                else:
                    continue
        else:
            return target

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

    @classmethod
    def delKey(cls, **kwargs):
        """
        如果value为空直接删除key
        :param kwargs:
        :return:
        """
        DICT = copy.deepcopy(kwargs)
        for k, v in DICT.items():
            if v is None or v == []:
                kwargs.pop(k)
        return kwargs

    @classmethod
    def get_extract_from_response(cls, response: HTTPxResponse | RequestResponse,
                                  extract: List[Dict[str, Any]]):
        """
        从请求响应解析想要的值
        :param response: HTTPxResponse | RequestResponse
        :param extract:
        :return:
        """
        from Enums import ExtractTargetEnum

        if extract and response.status_code == 200:
            for ext in extract:
                target = ext.get("target")
                mjp = MyJsonPath(response, ext.get("val"))
                value = None
                if target == ExtractTargetEnum.JSON.value:
                    value = mjp.value
                elif target == ExtractTargetEnum.HEADER.value:
                    value = mjp.getHeaderValue
                ext["val"] = value
            return extract


if __name__ == '__main__':
    e = [{'id': 1677578978008, 'key': 'Authorization', 'value': "{{token}}", },
         {'id': 1677578978008, 'key': 'Authorization2', 'value': 'hahah - {{token2}}'},
         {'id': 1677578978008, 'key': 'Authorization3', 'value': 'hahah - {{token3}}'}]
    p = [{'id': 1679377815262, 'key': 'token', 'val': {"haha": 123}, 'target': '1'},
         {'id': 1679377815262, 'key': 'token2', 'val': 'im token2', 'target': '1'},
         {'id': 1679377815262, 'key': 'token3', 'val': 'im token3', 'target': '1'}]
    extracts = [
        {
            "id": 1679377815262,
            "key": "token",
            "val": "$.data",
            "target": "1"
        }
    ]

    res = MyTools.list2Dict(p, e)
    print(res)
