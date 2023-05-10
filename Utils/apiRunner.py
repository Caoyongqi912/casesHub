# -*- coding: utf-8 -*-
# @Time    : 2022/9/15 下午2:46
# @Author  : cyq
# @File    : myRequest.py
import json
from datetime import datetime

from typing import Dict, Any, List, NoReturn, Union, Mapping, AnyStr

from requests import Response

from Models.CaseModel.interfaceModel import InterfaceModel, InterfaceResultModel, \
    InterfaceGroupResultModel
from Models.UserModel.userModel import User
from Models.base import Base
from Utils import MyLog, MyTools, UUID
from Utils.myAssert import MyAssert
from Utils.myBaseRequests import MyBaseRequest
from Utils.myJsonpath import MyJsonPath

log = MyLog.get_log(__file__)


class ApiRunner:
    response: Response = None

    def __init__(self, starter: User, variable: Mapping[str, Any] = None, ):
        """
        :param variable:  使用得环境变量
        :param starter:   运行人
        """
        self.extract = []
        self.responseInfo = []
        self.starter = starter
        self.worker = MyBaseRequest()
        if variable:
            self.extract.append(variable)
        self.LOG = []
        self.LOG.append(f"starter ====== {self.starter.username}\n")

    def runAPI(self, inter: InterfaceModel, entity: bool = False) -> Union[
        InterfaceResultModel.uid, InterfaceResultModel]:
        """
        运行api
        进行校验与结果入库
        :param inter: InterfaceModel
        :param entity: 是否返回实体类
        """
        STATUS = 'SUCCESS'
        useTime = 0
        log.info(f" === {inter.title} === 开始")

        for step in inter.steps:
            self.LOG.append(
                f"========================= request step-{step['step']} start ================================\n")
            response: Union[Response, Exception] = self.worker.run(inter.http, self.extract, **step)
            self.LOG.extend(self.worker.LOG)
            # 如果响应报错
            if isinstance(response, Exception):
                STATUS = "FAIL"
                self._writeError(step.get("step"), response)
                self.LOG.append(f"step-{step['step']}:response      ====== {repr(response)}\n")
                break

            # 如果相应非200
            elif response.status_code != 200:
                STATUS = "FAIL"
                self.LOG.append(f"step-{step['step']}:response.text            ====== {response.text}\n")
                self.LOG.append(f"step-{step['step']}:response.status_code     ====== {response.status_code}\n")
                break
            else:
                useTime += response.elapsed.total_seconds()
                status_code = response.status_code
                self.LOG.append(f"step-{step['step']}:response.text            ====== {response.text}\n")
                self.LOG.append(f"step-{step['step']}:response.status_code     ====== {status_code}\n")
                self.LOG.append(
                    f"step-{step['step']}:response.useTime         ====== {MyTools.to_ms(response.elapsed.total_seconds())}\n")
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
        self.LOG.append(f"case {inter.title} 结束 . 共用时{MyTools.to_ms(useTime)}\n")
        return self._writeResult(inter.id, inter.title, len(inter.steps), self.responseInfo, STATUS,
                                 useTime, entity)

    def runApis(self, interfaces: List[InterfaceModel]):
        """
        接口顺序批量运行
        :param interfaces: List[InterfaceModel]
        :return:
        """
        apis_report = []
        groupModel = InterfaceGroupResultModel()
        groupModel.totalNumber = len(interfaces)
        groupModel.successNumber = 0
        groupModel.failNumber = 0
        totalUseTime = 0
        groupModel.starterID = self.starter.id
        groupModel.starterName = self.starter.username
        interfacesDetail = []
        for inter in interfaces:
            restfulModel: InterfaceResultModel = self.runAPI(inter, True)
            groupModel.successNumber += 1 if restfulModel.status == "SUCCESS" else 0
            groupModel.failNumber += 1 if restfulModel.status == "FAIL" else 0
            totalUseTime += float(restfulModel.useTime) / 1000
            interfacesDetail.append(Base.to_json(restfulModel))
            groupModel.totalUseTime = MyTools.to_ms(totalUseTime)
            groupModel.detail = interfacesDetail
            groupModel.save()
        groupModel.status = "DONE"
        groupModel.end_time = datetime.now()
        groupModel.rateNumber = round(groupModel.successNumber / groupModel.totalNumber * 100, 2)
        groupModel.save()

    def runTest(self, step: Dict[str, Any], http: str = "http") -> Dict[str, Any]:
        """
        单步骤调试
        :param http: default http
        :param step: 步骤入参
        :return: info
        """
        STATUS = 'SUCCESS'
        USETIME = 0
        response: Response = self.worker.run(http, self.extract, **step)

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
            "extracts": [i for i in self.extract] if self.extract else [],
            "asserts": verifyInfo
        }
        return info

    def _get_extract(self, response: Response, extract: List[Dict[str, str]] | None = None):
        """
        1、提取上个接口变量变成参数
        2、提取全局变量变成参数
        :param response: Response
        :param extract:[{"key":"token","val":"$.data.token",target:"1"}] -> self.extract = [{"token":"xxxx"}]
        """
        from Enums import ExtractTargetEnum

        if extract and response.status_code == 200:
            for ext in extract:
                target = ext.get("target")
                mjp = MyJsonPath(response, ext.get("val"))
                value = None
                if target == ExtractTargetEnum.JSON.value:
                    value = mjp.value
                elif target == ExtractTargetEnum.HEADER.value:
                    value = mjp.getHeaderValue
                ext["val"] = value
                self.extract.append(ext)

    def _writeError(self, stepID: int, response: Exception):
        """
        请求存在报错、写入报错信息
        :param stepID:
        :param response:
        :return:
        """
        info = {
            "step": stepID,
            "response": {
                "status_code": 500,
                "response": repr(response),
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
                     useTime: Union[str, float, int], entity: bool) -> Union[InterfaceModel.uid, InterfaceModel]:
        """
        测试结果入库
        :param interfaceID: 接口id
        :param responseInfo: 测试结果信息
        :param status: 测试结果
        :param useTime:用时
        :param entity: 是否返回实体类
        :return:NoReturn
        """
        interfaceResult = InterfaceResultModel()
        interfaceResult.interfaceID = interfaceID
        interfaceResult.interfaceName = interfaceName
        interfaceResult.interfaceSteps = interfaceSteps
        interfaceResult.resultInfo = responseInfo
        interfaceResult.interfaceLog = "".join(self.LOG)
        interfaceResult.status = status
        interfaceResult.useTime = MyTools.to_ms(number=useTime, toStr=False) if entity else MyTools.to_ms(
            number=useTime)
        interfaceResult.starterID = self.starter.id
        interfaceResult.starterName = self.starter.username
        interfaceResult.save()
        log.info(f"=== {interfaceName} === 结束")
        if entity:
            return interfaceResult
        return interfaceResult.uid
