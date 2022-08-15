# -*- coding: utf-8 -*-

# @Time    : 2021/2/5 下午2:46
# @Author  : cyq
# @File    : myRequest.py
import json

import requests
import random
from faker import Faker
import os

f = Faker(locale="zh_CN")


class MyRequest:
    Host = "http://127.0.0.1:5000/"
    host = "https://sit-beijing.nhcbs.5i5j.com/nhapigw/uam-api/zuul/baseData/findDictByType.json?dictType=PROJECT_APPROVE_STATUS"

    def __init__(self):
        pass

    def go(self, method="GET", url="", params=None, headers=None, body=None, files=None, auth=None):

        if method == "GET":
            return requests.get(url=self.host + url, params=params, json=body, auth=auth)
        elif method == "POST":
            resp = requests.post(url=self.Host + url, params=params, json=body, auth=auth, files=files, headers=headers)
            return resp

        elif method == "PUT":
            resp = requests.put(url=self.Host + url, params=params, json=body, auth=auth)
            return resp
        else:
            resp = requests.delete(url=self.Host + url, params=params, json=body, auth=auth)
            return resp

    def adduser(self):

        for i in range(50):
            self.body = {
                "username": f.name(),
                "password": f.pystr(),
                "phone": f.phone_number(),
                "gender": random.choices(["MALE", "FEMALE"])[0],
                "tag": random.choices(["QA", "PR", "DEV"])[0]

            }
            rep = self.go(method="POST", url="v1/api/user/addUser", body=self.body)
            print(rep.text)

    def addDepart(self):
        for i in range(10):
            self.body = {
                "name": f.name(),
                "desc": f.pystr(),

            }
            rep = self.go(method="POST", url="v1/api/user/department", body=self.body)
            print(rep.text)

    def addAvatar(self):
        # 用open的方式打开文件，作为字典的值。file是请求规定的参数，每个请求都不一样。
        files = {'file': open("../resource/casesHub.png", 'rb')}
        # 请求的地址，这个地址中规定请求文件的参数必须是file
        # 用files参数接收 PFbUdtKZfSMYTdeOdUYJ_casesHub.png
        res = self.go(method="POST", url="v1/api/user/avatar", files=files)
        print(res.text)

    def addExcel(self):
        # 用open的方式打开文件，作为字典的值。file是请求规定的参数，每个请求都不一样。

        files = {'file': open("../resource/case.xlsx", 'rb')}
        # 请求的地址，这个地址中规定请求文件的参数必须是file
        # 用files参数接收 PFbUdtKZfSMYTdeOdUYJ_casesHub.png
        b = {"versionID": 1, "productID": 1}
        res = self.go(method="POST", url="v1/api/case/upload/excel", params=b, files=files)
        print(res.text)

    def t(self):
        headers = {
            "Authorization": 'eyJhbGciOiJSUzUxMiJ9.eyJqb2JJZCI6IjgzMTIxIiwiY29tcElkIjoiMSIsImNpdHlDb2RlIjoiMTEwMTAwIiwidHlwZSI6IkFQUCIsInVzZXJJZCI6IjE1MDc3Iiwib3JnSWQiOiIxMTgiLCJ1c2VybmFtZSI6IjE1MDc3IiwidG9rZW4iOiI0MjY4YzRkNDYyYzc0MGVhODRmZGQ4OGExZWMwNzFkMyJ9.GjeyWZ4bgt2tTnqbdiI5zY_3H5CmC0dRG3OsiHzEwM3Qm6FSUilAvEU5RJvdshpcgZPNA_0EiPL7V7ezJRyjvp5NmAjLSx7X2k33wik0QK63q0euuO37ZKDVc2w3jQdRGC8hszTLIy5M8wxZjjdqvk--AL1JCaSkVyEoLFFPGp4',
            "Cookie": "sidebarStatus=1; suid=ac9b412c-738d-40c0-9a61-99541c3f95f0; Admin-Token=eyJhbGciOiJSUzUxMiJ9.eyJqb2JJZCI6IjgzMTIxIiwiY29tcElkIjoiMSIsImNpdHlDb2RlIjoiMTEwMTAwIiwidHlwZSI6IkFQUCIsInVzZXJJZCI6IjE1MDc3Iiwib3JnSWQiOiIxMTgiLCJ1c2VybmFtZSI6IjE1MDc3IiwidG9rZW4iOiI0MjY4YzRkNDYyYzc0MGVhODRmZGQ4OGExZWMwNzFkMyJ9.GjeyWZ4bgt2tTnqbdiI5zY_3H5CmC0dRG3OsiHzEwM3Qm6FSUilAvEU5RJvdshpcgZPNA_0EiPL7V7ezJRyjvp5NmAjLSx7X2k33wik0QK63q0euuO37ZKDVc2w3jQdRGC8hszTLIy5M8wxZjjdqvk--AL1JCaSkVyEoLFFPGp4; clid=cd946ee5-631c-4d22-9864-c9143beb8432"
        }

        resp = self.go(headers=headers)
        print(resp.text)


if __name__ == '__main__':
    print("哈"*100)