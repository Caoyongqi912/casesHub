#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023-03-23
# @Author : cyq
# @File : casesHub
# @Software: PyCharm
# @Desc:

from typing import NoReturn, List, Any, Dict, Optional, Union, Mapping, Tuple
from httpx import AsyncClient, Response
import asyncio

from Models.CaseModel.hostModel import HostModel
from Models.CaseModel.interfaceModel import InterfaceModel, InterfaceGroupResultModel
from Models.UserModel.userModel import User
from Utils import MyLog, QueryParamTypes, HeaderTypes, RequestData, AuthTypes, MyTools
from Utils.myAssert import MyAssert

log = MyLog.get_log(__file__)


class MyHttpx:

    def __init__(self, interfaces: List[InterfaceModel], starter: User):
        """
        :param interfaces: 接口组
        """
        self.interfaces = interfaces
        self.interfacesDetail = []
        self.successNumber = 0
        self.failNumber = 0
        self.totalUseTime = 0
        self.interfaceGroupResultModel = InterfaceGroupResultModel()
        self.interfaceGroupResultModel.starter = starter.username
        self.interfaceGroupResultModel.save()
        log.info(f"start uid = {self.interfaceGroupResultModel.uid}")

    async def worker(self, interface: InterfaceModel, client: AsyncClient):
        """
        todo:

        1、处理interface 信息
        2、发送请求

        :param interface: 接口信息
        :param client: worker client
        :return:
        """
        STATUS = "SUCCESS"
        useTime = 0
        extracts = []
        stepsInfo = []
        LOG = []
        for step in interface.steps:
            log.info(f"========= {interface.title} step-{step['step']} start =========  ")
            LOG.append(f"========= {interface.title} step-{step['step']} start =========\n")
            response, responseLog = await self.to_sender(client, interface,
                                                         extracts,
                                                         **step)
            log.info(f"========= {interface.title} step-{step['step']} response {response.text} =========  ")
            LOG.extend(responseLog)
            if isinstance(response, Exception) or response.status_code != 200:
                STATUS = "FAIL"
                stepsInfo.append(await self._writeError(step['step'], response))
                break
            else:
                useTime += response.elapsed.total_seconds()
                verifyInfo, flag, verifyLog = MyAssert(response).doAssert(step["step"], step.get('asserts'))
                LOG.extend(verifyLog)
                if flag:  # 如果请求成功，去获取预期响应参数
                    ext = MyTools.get_extract_from_response(response, step.get("extracts"))
                    if ext:
                        extracts.extend(ext)
                else:
                    STATUS = "FAIL"
                    break
                stepsInfo.append(await self.write_interface_steps(step['step'], response, verifyInfo))
        await self.write_interface_response(interface, stepsInfo, STATUS, useTime, LOG)

    @staticmethod
    async def _writeError(stepID: int, response: Response | Exception):
        info = {
            "step": stepID,
            "response": {
                "status_code": None,
                "response": repr(response),
                "elapsed": None
            },
            "verify": None
        }

        return info

    @staticmethod
    async def write_interface_steps(stepID: int, response: Response, verifyInfo) -> Dict[str, Any]:
        """
        接口响应详情
        :param response: 响应对应
        :param stepID: 步骤ID
        :param verifyInfo: 断言详情
        :return:
        """
        step = {
            "step": stepID,
            "request": {
                "method": response.request.method,
                "headers": dict(response.request.headers),
            },
            "response": {
                "status_code": response.status_code,
                "response": response.text,
                "headers": dict(response.headers),
                "cookie": [{k: v} for k, v in response.cookies.items()],
                "elapsed": MyTools.to_ms(response.elapsed.total_seconds())
            },
            "verifyInfo": verifyInfo
        }
        return step

    async def write_interface_response(self, interface: InterfaceModel, stepsInfo: List[Dict[str, Any]],
                                       status: str,
                                       useTime: int | float,
                                       Log: List[str] = None
                                       ):
        """
        单个用例构建详情
        :param interface:
        :param useTime:
        :param Log:
        :param status:
        :param stepsInfo:
        :return:
        """
        if status == "SUCCESS":
            self.successNumber += 1
        else:
            self.failNumber += 1
        self.totalUseTime += useTime
        detail = {
            "interfaceUid": interface.uid,
            "interfaceName": interface.title,
            "interfaceLog": "".join(Log),
            "interfaceStatus": status,
            "interfaceUseTimes": MyTools.to_ms(useTime),
            "interfaceSteps": stepsInfo,
        }
        self.interfacesDetail.append(detail)

    async def write_result(self) -> InterfaceGroupResultModel.uid:
        """
        结果入库
        :return: InterfaceGroupResultModel.uid
        """

        self.interfaceGroupResultModel.totalNumber = len(self.interfaces)
        self.interfaceGroupResultModel.successNumber = self.successNumber
        self.interfaceGroupResultModel.failNumber = self.failNumber
        self.interfaceGroupResultModel.totalUseTime = MyTools.to_ms(self.totalUseTime)
        self.interfaceGroupResultModel.detail = self.interfacesDetail
        self.interfaceGroupResultModel.result_status = "DONE"
        self.interfaceGroupResultModel.save(new=False)

    async def to_sender(self, client: AsyncClient,
                        interface: InterfaceModel,
                        extract: Optional[List[Mapping[str, str]]] = None,
                        **kwargs
                        ):
        """
        :todo
        数据处理， 提取数据写入
        :param client:
        :param interface
        :param extract

        :return:
        """
        headers = MyTools.list2Dict(extract, kwargs.get("headers"))
        params = MyTools.list2Dict(extract, kwargs.get("params"))
        auth = MyTools.auth(extract, kwargs.get("auth"))
        url = interface.http.lower() + "://" + kwargs.get("host") + kwargs.get("url").split("?")[0]
        method = kwargs.get("method").lower()
        body = kwargs.get("body")
        data = kwargs.get("data")
        return await self.sender(client=client,
                                 method=method,
                                 headers=headers,
                                 params=params,
                                 auth=auth,
                                 url=url,
                                 json=body,
                                 data=data)

    @staticmethod
    async def sender(client: AsyncClient, method: str, **kwargs) -> Tuple[Response, List[str]] | Tuple[
        Exception, List[str]]:
        """
        发送请求
        :param client: worker client
        :param method: 请求方法
        :param kwargs: 请求信息
        :return: Response
        """
        kwargs = MyTools.delKey(**kwargs)
        log.info(kwargs)
        LOG = [f"{k} : {v} \n" for k, v in kwargs.items()]
        try:
            response = await getattr(client, method)(**kwargs)
            LOG.append(f"response : {response.text}")
            return response, LOG
        except Exception as e:
            log.error(repr(e))
            LOG.append(f"response : {repr(e)}")
            return e, LOG

    async def master(self) -> NoReturn:
        """
        master 入口
        创建任务、分发给worker
        """
        taskList = []
        async with AsyncClient() as client:
            client.timeout = 60 * 60
            for interface in self.interfaces:
                task = asyncio.create_task(
                    self.worker(interface=interface, client=client)
                )
                taskList.append(task)
            await asyncio.gather(*taskList)
            await self.write_result()


if __name__ == '__main__':
    from App import create_app

    create_app().app_context().push()
