# @Time : 2022/9/17 10:30 
# @Author : cyq
# @File : myTools.py 
# @Software: PyCharm
# @Desc:
import re
from typing import List, Dict, Any
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
        1、参数转换 ↓
        [{"key":"Content-Type","val":"application/json"},{"key":"token","val":"{{token}}"}]
        ==>
        {"Content-Type":"application/json",token:  {{token}}}
        2、提取转换 ↓
        [{token:xxx}]
        ===>
        {"Content-Type":"application/json",token:xxx}
        :param extracts: [{token:xxx}]
        :param params:   [{"key":"Content-Type","val":"application/json"},{"key":"token","val":"{{token}}"}]
        :return:
        """
        if not params:
            return params
        D = {}
        for _ in params:
            D[_["key"]] = _["val"]
        DD = deepcopy(D)
        for k, v in DD.items():
            v = MyTools.getValue(extracts, v)
            D[k] = v
        return D

    @staticmethod
    def getValue(extracts: List[Dict[str, Any]], target: str) -> Any:
        """
        {{value}} -> value
        :param target:
        :param extracts
        :return:
        """
        if "{{" in target and "}}" in target:
            val = re.findall(r"\{\{(.*?)\}\}", target)[0]
            _ = target.replace("{{", "").replace("}}", "")
            for ext in extracts:
                v = ext.get(val)
                if v:
                    return _.replace(val, v)
                else:
                    continue
        else:
            return target

    @staticmethod
    def auth(extracts: List[Dict[str, Any]] | None = None, authBody: Dict[str, str] | None = None) -> Dict | None:
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