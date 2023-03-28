#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023-03-27
# @Author : cyq
# @File : casesHub
# @Software: PyCharm
# @Desc:
import re

import requests
import hashlib



def login():
    req = requests.session()
    url = 'https://uat.cbs.bacic5i5j.com/cas/login?service=https://uat-beijing.cbs.bacic5i5j.com/base/cas'
    login_info = {
        "username": "705499",
        "password": hashlib.md5("1q2w3e4r".encode("utf-8")).hexdigest()[8:24]
    }
    info = getHiddenInfo(url,req)
    info["encrypted"] = True
    info["_eventId"] = "submit"
    login_info.update(info)
    login_base_url = 'https://uat.cbs.bacic5i5j.com'
    headers = {
        "Referer": url
    }
    login_url = login_base_url + login_info.pop("action")
    print(login_url)
    print(login_info)

    response = req.post(login_url, data=login_info, headers=headers)
    resp = req.get("https://uat-beijing.cbs.bacic5i5j.com/sales/house/scmHouseTab/getPrivateHouseTabByBusinessType?_timeStamp=1679901924759&businessType=2&houseCustomerFlag=1")

    print(resp.request.headers)



def getHiddenInfo(url,req):
    response = req.get(url)
    lt = re.findall(r'name="lt" value="(.*?)"/>', response.text)[0]
    execution = re.findall(r'name="execution" value="(.*?)"/>', response.text)[0]
    action = re.findall(r'action="(.*?)" ', response.text)[0]
    return {"lt": lt, "execution": execution, "action": action}


if __name__ == '__main__':
    login()
