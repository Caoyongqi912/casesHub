# -*- coding: utf-8 -*-
# @Time    : 2022/9/15 下午2:46
# @Author  : cyq
# @File    : myRequest.py
import json
from typing import Dict, Any, List, Optional, NoReturn, Union, Mapping
import requests
import urllib3
from requests import Response, exceptions
from requests.auth import HTTPBasicAuth

from Comment.myException import ParamException
from Enums import ResponseMsg
from Models.CaseModel.interfaceModel import InterfaceModel, InterfaceResultModel
from Models.UserModel.userModel import User
from Utils import MyLog, MyTools, AuthTypes, QueryParamTypes, HeaderTypes, RequestData, FileTypes
from Utils.myAssert import MyAssert
from Utils.myJsonpath import MyJsonPath

log = MyLog.get_log(__file__)


class MyRequest:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response: Response = None

    def __init__(self, HOST: str, variable: Mapping[str, Any] = None, starter: User = None):
        """
        :param HOST:      host
        :param variable:  使用得环境变量
        :param starter:   运行人
        """
        self.host = HOST
        self.extract = []
        self.responseInfo = []
        self.starter = starter
        self.worker = requests.session()
        if variable:
            self.extract.append(variable)
        log.info(f"host    ====== {self.host}")
        log.info(f"starter ====== {self.starter.username}")

    def runAPI(self, interface: InterfaceModel) -> NoReturn:
        """
        运行api
        进行校验与结果入库
        :param interface:
        """
        STATUS = 'SUCCESS'
        useTime = 0
        for step in interface.steps:
            log.info(f"========================= request step-{step['step']} start ================================")
            response = self.todo(url=step['url'],
                                 method=step['method'],
                                 headers=MyTools.list2Dict(self.extract, step.get("headers")),
                                 params=MyTools.list2Dict(self.extract, step.get("params")),
                                 body=step.get('body'),
                                 auth=MyTools.auth(self.extract, step.get("auth")))
            useTime += response.elapsed.total_seconds()
            status_code = response.status_code
            log.info(f"step-{step['step']}:status_code  ====== {status_code}")
            log.info(f"step-{step['step']}:response     ====== {response.text}")
            log.info(f"step-{step['step']}:useTime      ====== {response.elapsed.total_seconds()}s")
            # 如果响应非200
            if status_code != 200:
                pass
            # 如果存在校验
            verifyInfo, flag = MyAssert(response).doAssert(step.get("asserts"))
            self._writeResponse(step.get("step"), response, verifyInfo)
            if flag is True:
                # 如果需要提取参数
                self._get_extract(response, step.get("extracts"))
            else:
                STATUS = 'FAIL'
                break

        self._writeResult(interface.id, self.responseInfo, STATUS, useTime)

    def runDemo(self, **kwargs):
        """
        运行demo
        :param name:
        :param kwargs:
        :return:
        """
        STATUS = 'SUCCESS'
        name = kwargs.pop("name")
        useTime = 0
        response = self.todo(**kwargs)
        useTime += response.elapsed.total_seconds()
        info = {
            "name": name,
            "status": STATUS,
            "method": response.request.method,
            "status_code": response.status_code,
            "body": json.loads(response.request.body) if response.request.body else None,
            "cost": useTime,
            "headers": dict(response.headers),
            "cookies": response.cookies.items(),
            "response": response.text
        }
        return info

    def todo(self, url: str,
             method: str,
             body: Optional[Any] = None,
             params: Optional[QueryParamTypes] = None,
             file: Optional[FileTypes] = None,
             headers: Optional[HeaderTypes] = None,
             data: Optional[RequestData] = None,
             auth: Optional[AuthTypes] = None,
             allow_redirects: bool = False,
             **kwargs
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
        log.info(f'auth   ====== {auth}')
        if auth:
            auth = HTTPBasicAuth(**auth)
        try:
            if method == "GET":
                self.response = self.worker.get(self.host + url, params=params, headers=headers,
                                                allow_redirects=allow_redirects, auth=auth)
            elif method == "POST":
                self.response = self.worker.post(self.host + url, json=body, headers=headers,
                                                 files=file,
                                                 data=data, allow_redirects=allow_redirects, auth=auth)
            elif method == "PUT":
                self.response = self.worker.put(self.host + url, json=body, params=params, headers=headers,
                                                files=file,
                                                data=data, allow_redirects=allow_redirects, auth=auth)
            elif method == "DELETE":
                self.response = self.worker.delete(self.host + url, json=body, params=params, headers=headers,
                                                   files=file, allow_redirects=allow_redirects,
                                                   auth=auth)
            else:
                raise ParamException(ResponseMsg.error_param(method))
            return self.response
        except exceptions.Timeout as e:
            log.error(repr(e))
        except exceptions.InvalidURL as e:
            log.error(repr(e))
        except exceptions.HTTPError as e:
            log.error(repr(e))
        except exceptions.ConnectionError as e:
            log.error(repr(e))
        except Exception as e:
            log.error(repr(e))
            log.error(self.response.text)
            raise

    def _get_extract(self, response: Response, extract: List[Dict[str, str]] | None = None):
        """
        1、提取上个接口变量变成参数
        2、提取全局变量变成参数
        :param response:
        :param extract:[{"key":"token","val":"$.data.token"}] -> self.extract = [{"token":"xxxx"}]
        """
        if extract:
            for ext in extract:
                value = MyJsonPath(response, ext.get("val")).value
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

    def _writeResult(self, interfaceID: int, responseInfo: List[Dict[str, Any]], status: str,
                     useTime: Union[str, float, int]) -> NoReturn:
        """
        测试结果入库
        :param interfaceID: 接口id
        :param responseInfo: 测试结果信息
        :param status: 测试结果
        :param useTime:用时
        :return:NoReturn
        """
        interfaceResult = InterfaceResultModel()
        interfaceResult.interfaceID = interfaceID
        interfaceResult.resultInfo = responseInfo
        interfaceResult.status = status
        interfaceResult.useTime = useTime
        interfaceResult.starterID = self.starter.id
        interfaceResult.starterName = self.starter.username
        interfaceResult.save()


if __name__ == '__main__':
    from App import create_app

    create_app().app_context().push()
    from Models.CaseModel.hostModel import HostModel

    # v: VariableModel = VariableModel.get(1)
    u = User.get(1)
    inter = InterfaceModel.get(28)
    Host = "http://127.0.0.1:8080"
    MyRequest(HOST=Host, starter=u).runAPI(inter)
