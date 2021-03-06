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

    def __init__(self):
        pass

    def go(self, method, url, params=None, headers=None, body=None, files=None, auth=("cyq", "123")):

        if method == "GET":
            return requests.get(url=self.Host + url, params=params, json=body, auth=auth)

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


if __name__ == '__main__':
    m = MyRequest()
    m.addExcel()
