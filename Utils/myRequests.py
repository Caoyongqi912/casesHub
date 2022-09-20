# -*- coding: utf-8 -*-

# @Time    : 2022/9/15 下午2:46
# @Author  : cyq
# @File    : myRequest.py

from typing import Dict, Any, List
import requests
import urllib3
from requests import Response, exceptions
from requests.auth import HTTPBasicAuth

from Models.CaseModel.interfaceModel import InterfaceModel, InterfaceResultModel
from Utils import MyLog, MyTools
from Utils.myAssert import MyAssert
from Utils.myJsonpath import MyJsonPath

log = MyLog.get_log(__file__)


class MyRequest:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response: Response = None

    def __init__(self, HOST: str, variable: Dict[str, Any] = None):
        """
        :param HOST:HOST
        """
        self.host = HOST
        self.extract = []
        self.responseInfo = []
        log.info(f"host   ====== {self.host}")
        self.worker = requests.session()
        if variable:
            self.extract.append(variable)

    def runAPI(self, interface: InterfaceModel):
        """
        运行
        :param interface:
        :return:
        """
        STATUS = 'SUCCESS'
        interfaceResult = InterfaceResultModel()
        interfaceResult.interfaceID = interface.id
        for step in interface.steps:

            log.info(f"========================= request {step['step']} start ================================")
            response = self.todo(url=step['url'],
                                 method=step['method'],
                                 headers=MyTools.list2Dict(self.extract, step.get("headers")),
                                 params=MyTools.list2Dict(self.extract, step.get("params")),
                                 body=MyTools.list2Dict(self.extract, step.get("body")),
                                 auth=MyTools.auth(self.extract, step.get("auth")))

            log.info(f"response  ====== {response.json()}")
            # 如果存在校验
            verifyInfo, flag = MyAssert(response).jpAssert(step.get("jsonpath"))
            if flag is True:
                # 如果需要提取参数
                self._get_extract(response, step.get("extract"))
                self._writeResponse(step.get("step"), response, verifyInfo)
            else:
                STATUS = 'FAIL'
                break
        interfaceResult.resultInfo = self.responseInfo
        interfaceResult.status = STATUS
        interfaceResult.save()

    def todo(self, url: str,
             method: str,
             body: Dict[str, Any] | List = None,
             params: Dict[str, Any] = None,
             file: Dict[str, Any] = None,
             headers: Dict[str, Any] = None,
             data: Dict[str, Any] = None,
             auth=None,
             allow_redirects: bool = False
             ) -> Response:
        """
        :param url: 路由
        :param method: 请求方法
        :param body: 请求体
        :param params: 请求参数
        :param file: 上传文件
        :param headers: 请求头
        :param data: 请求数据
        :param auth: auth
        :param allow_redirects 是否开启重定向
        :return: response
        """
        log.info(f"url    ====== {url}")
        log.info(f"method ====== {method}")
        log.info(f"header ====== {headers}")
        log.info(f"body   ====== {body}")
        log.info(f"params ====== {params}")
        if auth:
            auth = HTTPBasicAuth(**auth)
        try:
            if method == "GET":
                self.response = self.worker.get(self.host + url, json=body, params=params, headers=headers,
                                                files=file,
                                                data=data, allow_redirects=allow_redirects, auth=auth)
            elif method == "POST":
                self.response = self.worker.post(self.host + url, json=body, params=params, headers=headers,
                                                 files=file,
                                                 data=data, allow_redirects=allow_redirects, auth=auth)
            elif method == "PUT":
                self.response = self.worker.put(self.host + url, json=body, params=params, headers=headers,
                                                files=file,
                                                data=data, allow_redirects=allow_redirects, auth=auth)
            else:
                self.response = self.worker.delete(self.host + url, json=body, params=params, headers=headers,
                                                   files=file, allow_redirects=allow_redirects,
                                                   data=data, auth=auth)
            return self.response
        except exceptions.Timeout as e:
            log.error(e)
        except exceptions.InvalidURL as e:
            log.error(e)
        except exceptions.HTTPError as e:
            log.error(e)
        except exceptions.ConnectionError as e:
            log.error(e)
        except Exception as e:
            log.error(e)
            log.error(self.response.text)
            raise

    def _get_extract(self, response: Response, extract: List[Dict[str, str]] | None = None):
        """
        提取
        :param response:
        :param extract:[{"key":"token","val":"$.data.token"}] -> self.extract = [{"token":"xxxx"}]
        """
        if extract:
            for ext in extract:
                value = MyJsonPath(response.json(), ext.get("val")).value
                _ = {ext["key"]: value}
                self.extract.append(_)

    def _writeResponse(self, stepID: int, response: Response = None,
                       verifyInfo: Any = None):

        info = {
            "step": stepID,
            "response": {
                "status_code": response.status_code,
                "response": response.text,
                "elapsed": response.elapsed.total_seconds()
            },
            "verify": verifyInfo
        }
        self.responseInfo.append(info)


if __name__ == '__main__':
    from App import create_app

    create_app().app_context().push()
    from Models.CaseModel.hostModel import HostModel
    from Models.ProjectModel.project import Project

    p = Project.get(1)
    var = p.query_variables2dict()
    inter = InterfaceModel.get(1)
    hostName = HostModel.get(6).host
    worker = MyRequest(hostName, var).runAPI(inter)
    # print(var)
    # print(inter)
