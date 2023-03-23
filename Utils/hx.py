# @Time : 2022/12/1 20:11 
# @Author : cyq
# @File : hx.py
# @Software: PyCharm
# @Desc:
from typing import Dict, Any, List, Coroutine, Optional, Mapping, Union, NoReturn
from requests.auth import HTTPBasicAuth
from httpx import AsyncClient, Response
import asyncio
from sqlalchemy import Column
from Models.CaseModel.hostModel import HostModel
from Models.CaseModel.interfaceModel import InterfaceModel, InterfaceResultModel
from Models.CaseModel.variableModel import VariableModel
from Models.UserModel.userModel import User
from Utils import MyLog, MyTools, QueryParamTypes, FileTypes, HeaderTypes, RequestData, AuthTypes
from Utils.myAssert import MyAssert
from Utils.myJsonpath import MyJsonPath

log = MyLog.get_log(__file__)


def _writeResponse(stepID: int, response: Response = None,
                   verifyInfo: Any = None) -> Mapping[str, Any]:
    info = {
        "step": stepID,
        "response": {
            "status_code": response.status_code,
            "response": response.text,
            "elapsed": round(response.elapsed.total_seconds(), 2)
        },
        "verify": verifyInfo
    }
    return info


def _get_extract(response: Response, extract: List[Dict[str, str]] | None = None):
    """
    1、提取上个接口变量变成参数
    2、提取全局变量变成参数
    :param response:
    :param extract:[{"key":"token","val":"$.data.token"}] -> self.extract = [{"token":"xxxx"}]
    """
    ex = []
    if extract:
        for ext in extract:
            value = MyJsonPath(response.json(), ext.get("val")).value
            _ = {ext["key"]: value}
            ex.append(_)
    return ex


class MyHttpx:

    def __init__(self, HOST: HostModel, jobList: List[InterfaceModel], variable: Mapping[str, Any] = None,
                 starter: User = None):
        self.HOST = HOST.host + ":" + HOST.port
        self.jobList = jobList
        self.taskList = []
        self.variable = variable
        self.starter = starter

    async def todo(self,
                   client: AsyncClient,
                   method: str,
                   url: str,
                   http: str,
                   body: Optional[Any] = None,
                   params: Optional[QueryParamTypes] = None,
                   file: Optional[FileTypes] = None,
                   headers: Optional[HeaderTypes] = None,
                   data: Optional[RequestData] = None,
                   auth: Optional[AuthTypes] = None,
                   follow_redirects: bool = False
                   ) -> Response:
        """
                :param client: AsyncClient
                :param url: 路由
                :param http: http or https
                :param method: 请求方法
                :param body: 请求体
                :param params: 请求参数
                :param file: 上传文件
                :param headers: 请求头
                :param data: 请求数据
                :param auth: auth
                :param follow_redirects 是否开启重定向
                :return: response
        """
        headers = MyTools.list2Dict(self.variable, headers)
        params = MyTools.list2Dict(self.variable, params)
        auth = MyTools.auth(self.variable, auth)
        url = url.split("?")[0]

        log.info(f"url    ====== {url}")
        log.info(f"method ====== {method}")
        log.info(f"header ====== {headers}")
        log.info(f"body   ====== {body}")
        log.info(f"params ====== {params}")
        log.info(f'auth   ====== {auth}')
        response = await self.cli(
            client=client,
            http=http,
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=body,
            auth=auth)
        return response

    async def cli(self, client: AsyncClient, method: str, http: str, **kwargs) -> Response:
        log.info(kwargs)
        if kwargs.get("auth", None):
            kwargs['auth'] = HTTPBasicAuth(**kwargs['auth'])
        kwargs["url"] = http.lower() + "://" + self.HOST + kwargs['url']
        method = method.lower()
        try:
            response = getattr(client, method)(**kwargs)
            return response
        except Exception as e:
            log.error(repr(e))
            raise e

    async def worker(self, interface: InterfaceModel, client: AsyncClient):
        """
        运行api
        进行校验与结果入库
        :param interface:InterfaceModel
        :param client:
        :return:
        """
        responseInfo = []
        extract = []
        if self.variable:
            extract.append(self.variable)
        STATUS = 'SUCCESS'
        useTime = 0
        for step in interface.steps:
            log.info(
                f"========================= request  step-{step['step']}  start ================================")
            response = await self.todo(client, interface.http, **step)
            useTime += response.elapsed.total_seconds()
            log.info(f"-{interface.title}- step-{step['step']}:status_code  ====== {response.status_code}")
            log.info(f"-{interface.title}- step-{step['step']}:response     ====== {response.text}")
            log.info(f"-{interface.title}- step-{step['step']}:useTime      ====== {response.elapsed.total_seconds()}s")
            # 如果存在校验
            verifyInfo, flag = MyAssert(response).jpAssert(step.get("jsonpath"))
            responseInfo.append(_writeResponse(step.get("step"), response, verifyInfo))
            if flag is True:
                # 如果需要提取参数
                extract.extend(_get_extract(response, step.get("extract")))
            else:
                STATUS = 'FAIL'
                break
        self._writeResult(interface.id, responseInfo, STATUS, useTime)

    def _writeResult(self, interfaceID: Column, responseInfo: List[Mapping[str, Any]], status: str,
                     useTime: Union[float]) -> NoReturn:
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
        log.info(f"save {interfaceID} success")

    async def master(self):
        async with AsyncClient() as client:
            for inter in self.jobList:
                worker = self.worker(inter, client)
                task = asyncio.create_task(worker)  # 创建任务
                self.taskList.append(task)
            await asyncio.gather(*self.taskList)  # 收集任务


if __name__ == '__main__':
    from App import create_app

    create_app().app_context().push()
    from Models.CaseModel.hostModel import HostModel

    v: VariableModel = VariableModel.get(1)
    u = User.get(1)
    inters = InterfaceModel.query_by_field(partID=1)
    hostName = HostModel.get(6).host
    h = MyHttpx(hostName, inters, v.to_Dict, u)
    asyncio.run(h.master())
