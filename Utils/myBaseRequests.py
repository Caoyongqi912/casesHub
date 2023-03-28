#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023-02-23
# @Author : cyq
# @File : casesHub
# @Software: PyCharm
# @Desc:
import gevent
from typing import List

import requests
import urllib3
from requests import Response, exceptions

from Models.CaseModel.hostModel import HostModel
from Utils import MyLog, MyTools
from requests.auth import HTTPBasicAuth

log = MyLog.get_log(__file__)


def getHost(host: HostModel):
    if host.port:
        return host.host + ":" + host.port
    return host.host


class MyBaseRequest:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response: Response = None

    def __init__(self, host: HostModel):
        self.host = getHost(host)
        self.request_obj = requests.session()
        self.LOG = []

    def run(self, http, extract: List, **kwargs) -> Response | Exception:
        """
        请求接口前参数处理
        :param http: HTTP / HTTPS
        :param extract:
        :param kwargs:
        :return:
        """
        headers = MyTools.list2Dict(extract, kwargs.get("headers"))
        params = MyTools.list2Dict(extract, kwargs.get("params"))
        auth = MyTools.auth(extract, kwargs.get("auth"))
        body = kwargs.get('body')
        method = kwargs['method']
        url = kwargs["url"].split("?")[0]


        self.LOG.append(f"step-{kwargs['step']}:url     ====== {url}\n")
        self.LOG.append(f"step-{kwargs['step']}:method  ====== {method}\n")
        self.LOG.append(f"step-{kwargs['step']}:headers ====== {headers}\n")
        self.LOG.append(f"step-{kwargs['step']}:params  ====== {params}\n")
        self.LOG.append(f"step-{kwargs['step']}:body    ====== {body}\n")

        response = self.todo(url=url,
                             http=http,
                             method=method,
                             headers=headers,
                             params=params,
                             json=body,
                             auth=auth)
        return response

    def todo(self,
             method: str,
             http: str,
             **kwargs
             ) -> Response | Exception:
        """
        :param http: http
        :param method : 请求方法
        :return: response
        """
        kwargs = MyTools.delKey(**kwargs)
        if kwargs.get("auth", None):
            kwargs['auth'] = HTTPBasicAuth(**kwargs['auth'])
        kwargs["url"] = http.lower() + "://" + self.host + kwargs['url']
        method = method.lower()
        try:
            self.response = getattr(self.request_obj, method)(**kwargs)
            return self.response
        except Exception as e:
            log.error(e)
            return e
