# -*- coding: utf-8 -*-

# @Time    : 2022/9/15 下午2:46
# @Author  : cyq
# @File    : myRequest.py

from typing import Dict, Any, List
import requests
import urllib3
from requests import Response, exceptions

from Enums import APIMethodEnum
from Utils import MyLog

log = MyLog.get_log(__file__)


class MyRequest:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response: Response = None

    def __init__(self, HOST: str):
        """

        :param HOST:
        """
        self.host = HOST
        self.worker = requests.session()

    def runAPI(self):



    def todo(self, url: str, method: APIMethodEnum, body: Dict[str, Any] | List = None, params: Dict[str, Any] = None,
             file: Dict[str, Any] = None, headers: Dict[str, Any] = None, data: Dict[str, Any] = None,
             allow_redirects: bool = True
             ) -> Dict | List:
        """
        :param url: 路由
        :param method: 请求方法
        :param body: 请求体
        :param params: 请求参数
        :param file: 上传文件
        :param headers: 请求头
        :param data: 请求数据
        :param allow_redirects 是否开启重定向
        :return: response
        """
        try:
            if method.name == "GET":
                self.response = self.worker.get(self.host + url, json=body, params=params, headers=headers,
                                                files=file,
                                                data=data, allow_redirects=allow_redirects,
                                                verify=False)
            elif method.name == "POST":
                self.response = self.worker.post(self.host + url, json=body, params=params, headers=headers,
                                                 files=file,
                                                 data=data, allow_redirects=allow_redirects,
                                                 verify=False)
            elif method.name == "PUT":
                self.response = self.worker.put(self.host + url, json=body, params=params, headers=headers,
                                                files=file,
                                                data=data, allow_redirects=allow_redirects,
                                                verify=False)
            else:
                self.response = self.worker.delete(self.host + url, json=body, params=params, headers=headers,
                                                   files=file, allow_redirects=allow_redirects,
                                                   data=data,
                                                   verify=False)
            return self.response.json()
        except exceptions.Timeout as e:
            log.error(e)
        except exceptions.InvalidURL as e:
            log.error(e)
        except exceptions.HTTPError as e:
            log.error(e)
        except Exception as e:
            log.error(e)
            log.error(self.response.text)
            raise
