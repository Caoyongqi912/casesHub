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

from Models.CaseModel.interfaceModel import InterfaceModel, InterfaceResultModel
from Models.CaseModel.hostModel import HostModel
from Models.UserModel.userModel import User
from Utils import MyLog, MyTools, AuthTypes, QueryParamTypes, HeaderTypes, RequestData, FileTypes
from Utils.myAssert import MyAssert
from Utils.myBaseRequests import MyBaseRequest
from Utils.myJsonpath import MyJsonPath

log = MyLog.get_log(__file__)


class MyRequest:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response: Response = None

    def __init__(self, HOST: HostModel, variable: Mapping[str, Any] = None, starter: User = None):
        """
        :param HOST:      host
        :param variable:  使用得环境变量
        :param starter:   运行人
        """
        self.extract = []
        self.responseInfo = []
        self.starter = starter
        self.worker = MyBaseRequest(host=HOST.host + ":" + HOST.port)
        if variable:
            self.extract.append(variable)
        self.LOG = []
        log.info(f"starter ====== {self.starter.username}")
        self.LOG.append(f"starter ====== {self.starter.username}\n")

    def runAPI(self, interface: InterfaceModel) -> str:
        """
        运行api
        进行校验与结果入库
        :param interface:
        """
        STATUS = 'SUCCESS'
        useTime = 0
        for step in interface.steps:
            log.info(f"========================= request step-{step['step']} start ================================")
            self.LOG.append(
                f"========================= request step-{step['step']} start ================================\n")
            response = self.run(interface.http, **step)
            # 如果响应报错
            if isinstance(response, Exception):
                self._writeError(step.get("step"), repr(response))
                break
            else:
                useTime += response.elapsed.total_seconds()
                status_code = response.status_code
                log.info(f"step-{step['step']}:status_code  ====== {status_code}")
                log.info(f"step-{step['step']}:response     ====== {response.text}")
                log.info(f"step-{step['step']}:useTime      ====== {response.elapsed.total_seconds()}s")
                self.LOG.append(f"step-{step['step']}:status_code  ====== {status_code}\n")
                self.LOG.append(f"step-{step['step']}:response     ====== {response.text}\n")
                self.LOG.append(f"step-{step['step']}:useTime      ====== {response.elapsed.total_seconds()}s \n")
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

        return self._writeResult(interface.id, interface.title, len(interface.steps), self.responseInfo, STATUS,
                                 useTime)

    def runDemo(self, **kwargs):
        """
        运行demo
        :param name:
        :param kwargs:
        :return:
        """
        STATUS = 'SUCCESS'
        USETIME = 0
        name = kwargs.pop("name")
        log.info(kwargs)
        response = self.run(**kwargs)
        USETIME += response.elapsed.total_seconds()
        info = {
            "name": name,
            "status": STATUS,
            "method": response.request.method,
            "status_code": response.status_code,
            "body": json.loads(response.request.body) if response.request.body else None,
            "cost": MyTools.to_ms(USETIME),
            "headers": dict(response.headers),
            "cookies": response.cookies.items(),
            "response": response.text
        }
        return info

    def run(self, *args, **kwargs):

        response = self.worker.todo(url=kwargs['url'],
                                    method=kwargs['method'],
                                    http=args[0],
                                    headers=MyTools.list2Dict(self.extract, kwargs.get("headers")),
                                    params=MyTools.list2Dict(self.extract, kwargs.get("params")),
                                    json=kwargs.get('body'),
                                    auth=MyTools.auth(self.extract, kwargs.get("auth")))
        return response

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

    def _writeError(self, stepID: int, response: Any):
        info = {
            "step": stepID,
            "response": {
                "status_code": None,
                "response": response,
                "elapsed": None
            },
            "verify": None
        }
        self.responseInfo.append(info)

    def _writeResponse(self, stepID: int, response: Response = None,
                       verifyInfo: Any = None) -> NoReturn:
        """
        记录人每步请求结果信息
        :param stepID: 步骤
        :param response: 相应
        :param verifyInfo: 断言结果
        """
        info = {
            "step": stepID,
            "request": {
                "method": response.request.method,
                "headers": dict(response.request.headers),

            },
            "response": {
                "status_code": response.status_code,
                "response": response.text,
                "headers": dict(response.headers),
                "cookie": response.cookies.items(),
                "elapsed": MyTools.to_ms(response.elapsed.total_seconds())
            },
            "verify": verifyInfo
        }
        self.responseInfo.append(info)

    def _writeResult(self, interfaceID: int, interfaceName: str, interfaceSteps: int,
                     responseInfo: List[Dict[str, Any]], status: str,
                     useTime: Union[str, float, int]) -> InterfaceModel.uid:
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
        interfaceResult.interfaceName = interfaceName
        interfaceResult.interfaceSteps = interfaceSteps
        interfaceResult.resultInfo = responseInfo
        interfaceResult.interfaceLog = "".join(self.LOG)
        interfaceResult.status = status
        interfaceResult.useTime = MyTools.to_ms(useTime)
        interfaceResult.starterID = self.starter.id
        interfaceResult.starterName = self.starter.username
        interfaceResult.save()
        return interfaceResult.uid


if __name__ == '__main__':
    from App import create_app

    create_app().app_context().push()
    from Models.CaseModel.hostModel import HostModel

    # v: VariableModel = VariableModel.get(1)
    u = User.get(1)
    inter = InterfaceModel.get_by_uid("wpjhYVlxIXrXgaRRVoHv")
    Host = HostModel.get_by_uid("FmOSZlPBfBgwNNwPLJOh")
    MyRequest(HOST=Host, starter=u).runAPI(inter)
