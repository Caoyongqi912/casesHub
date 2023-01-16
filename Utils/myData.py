#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023-01-16
# @Author : cyq
# @File : casesHub
# @Software: PyCharm
# @Desc:
import random

import requests
from faker import Faker

f = Faker(locale="zh_CN")

HOST = "http://localhost:5000"
auth = ('admin', 'admin')


def addAdmin():
    body = {"username": "admin", "password": "admin", 'phone': f.phone_number()}
    url = "/api/user/admin"
    requests.post(HOST + url, json=body)


def addDepartMent():
    n = ["产品", "质量", "开发"]
    url = "/api/user/department/opt"
    for _ in n:
        body = {
            "name": _ + "部门",
            "desc": _ + "__" + f.pystr(),
            "adminID": 1,
            "tags": [
                "高级" + _,
                "中级" + _,
                "初级" + _
            ]
        }
        requests.post(HOST + url, json=body, auth=auth)


def addUser(n):
    url = '/api/user/opt'
    for i in range(n):
        body = {
            "username": f.name(),
            "phone": f.phone_number(),
            "gender": random.choice(["FEMALE", "MALE"]),
        }
        requests.post(HOST + url, json=body, auth=auth)


if __name__ == '__main__':
    addUser(10)
