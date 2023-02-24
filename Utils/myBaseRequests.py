#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023-02-23
# @Author : cyq
# @File : casesHub
# @Software: PyCharm
# @Desc:
import requests
import urllib3
from requests import Response, exceptions

from Utils import MyLog
from requests.auth import HTTPBasicAuth

log = MyLog.get_log(__file__)


class MyBaseRequest:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response: Response = None

    def __init__(self, host: str):
        self.host = host
        self.request_obj = requests.session()

    def todo(self,
             method: str,
             **kwargs
             ) -> Response | Exception:
        """
        :param method : 请求方法
        :return: response
        """
        log.info(kwargs)
        if kwargs.get("auth", None):
            kwargs['auth'] = HTTPBasicAuth(**kwargs['auth'])
        kwargs["url"] = self.host + kwargs['url']
        method = method.lower()
        try:
            self.response = getattr(self.request_obj, method)(**kwargs)
            return self.response
        except Exception as e:
            log.error(repr(e))
            return e
