# -*- coding: utf-8 -*-
# @Time    : 2022/9/15 下午2:46
# @Author  : cyq
# @File    : myRequest.py
import json

from typing import Dict, Any, List, NoReturn, Union, Mapping, AnyStr
from requests import Response

from Models.CaseModel.interfaceModel import InterfaceModel, InterfaceResultModel
from Models.CaseModel.hostModel import HostModel
from Models.UserModel.userModel import User
from Utils import MyLog, MyTools
from Utils.myAssert import MyAssert
from Utils.myBaseRequests import MyBaseRequest
from Utils.myJsonpath import MyJsonPath

log = MyLog.get_log(__file__)


class MyRequest:
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
        :param interface: InterfaceModel
        """
        STATUS = 'SUCCESS'
        useTime = 0
        for step in interface.steps:
            self.LOG.append(
                f"========================= request step-{step['step']} start ================================\n")
            response = self.run(interface.http, **step)
            # 如果响应报错
            if isinstance(response, Exception) or response.status_code != 200:
                STATUS = "FAIL"
                self._writeError(step.get("step"), repr(response))
                self.LOG.append(f"step-{step['step']}:response     ====== {repr(response)}\n")
                break

            else:
                useTime += response.elapsed.total_seconds()
                status_code = response.status_code
                self.LOG.append(f"step-{step['step']}:status_code  ====== {status_code}\n")
                self.LOG.append(f"step-{step['step']}:response     ====== {response.text}")
                self.LOG.append(f"step-{step['step']}:useTime      ====== {response.elapsed.total_seconds()}s \n")
                # 如果存在校验
                verifyInfo, flag, verifyLog = MyAssert(response).doAssert(step.get("step"), step.get("asserts"))
                self.LOG.extend(verifyLog)
                self._writeResponse(step.get("step"), response, verifyInfo)
                if flag is True:
                    # 如果需要提取参数
                    self._get_extract(response, step.get("extracts"))
                else:
                    STATUS = 'FAIL'
                    break
        self.LOG.append(f"\n case {interface.title} 结束 . 共用时{useTime}s \n")
        return self._writeResult(interface.id, interface.title, len(interface.steps), self.responseInfo, STATUS,
                                 useTime)

    def runText(self, step: dict, http: str = "http"):

        """
        单步骤调试
        :param http: default http
        :param step: 步骤入参
        :return:
        """
        STATUS = 'SUCCESS'
        USETIME = 0
        response: Response = self.run(http, **step)

        if step.get("extracts"):
            self._get_extract(response, step.get("extracts"))
        verifyInfo, flag, verifyLog = MyAssert(response).doAssert(step.get("step"), step.get("asserts"))
        USETIME += response.elapsed.total_seconds()

        info = {
            "status": STATUS,
            "method": response.request.method,
            "status_code": response.status_code,
            "body": json.loads(response.request.body) if response.request.body else None,
            "cost": MyTools.to_ms(USETIME),
            "headers": dict(response.headers),
            "cookies": response.cookies.items(),
            "response": response.text,
            "extracts": self.extract,
            "asserts": verifyInfo
        }
        return info

    def run(self, http, **kwargs):
        headers = MyTools.list2Dict(self.extract, kwargs.get("headers"))
        params = MyTools.list2Dict(self.extract, kwargs.get("params"))
        auth = MyTools.auth(self.extract, kwargs.get("auth"))
        body = kwargs.get('body')
        method = kwargs['method']
        url = kwargs["url"].split("?")[0]

        self.LOG.append(f"step-{kwargs['step']}:url     ====== {url}\n")
        self.LOG.append(f"step-{kwargs['step']}:method  ====== {method}\n")
        self.LOG.append(f"step-{kwargs['step']}:headers ====== {headers}\n")
        self.LOG.append(f"step-{kwargs['step']}:params  ====== {params}\n")
        self.LOG.append(f"step-{kwargs['step']}:body    ====== {body}\n")

        response = self.worker.todo(url=url,
                                    http=http,
                                    method=method,
                                    headers=headers,
                                    params=params,
                                    json=body,
                                    auth=auth)
        return response

    def _get_extract(self, response: Response, extract: List[Dict[str, str]] | None = None):
        """
        1、提取上个接口变量变成参数
        2、提取全局变量变成参数
        :param response:
        :param extract:[{"key":"token","val":"$.data.token"}] -> self.extract = [{"token":"xxxx"}]
        """
        if extract and response.status_code == 200:
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
