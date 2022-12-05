# @Time : 2022/12/1 20:11 
# @Author : cyq
# @File : myHttpx.py 
# @Software: PyCharm
# @Desc:
import time
from typing import Dict, Any, List, Coroutine
from httpx import AsyncClient, Response
import asyncio
from Utils import MyLog, MyTools
from Utils.myAssert import MyAssert
from Utils.myJsonpath import MyJsonPath

log = MyLog.get_log(__file__)


class MyHttpx:

    def __init__(self, HOST: str, jobList):
        self.HOST = HOST
        self.jobList = jobList
        self.taskList = []

    async def todo(self, url: str,
                   client: AsyncClient,
                   method: str,
                   body: Dict[str, Any] | List = None,
                   params: Dict[str, Any] = None,
                   file: Dict[str, Any] = None,
                   headers: Dict[str, Any] = None,
                   data: Dict[str, Any] = None,
                   auth=None,
                   follow_redirects: bool = False
                   ):
        """
                :param client: AsyncClient
                :param url: 路由
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
        log.info(f"url    ====== {url}")
        log.info(f"method ====== {method}")
        log.info(f"header ====== {headers}")
        log.info(f"body   ====== {body}")
        log.info(f"params ====== {params}")

        if method == "GET":
            response = await client.get(self.HOST + url, params=params, headers=headers,
                                        follow_redirects=follow_redirects, auth=auth)
            log.info(response.status_code)

        elif method == "POST":
            response = await client.post(self.HOST + url, json=body, params=params, headers=headers,
                                         files=file,
                                         data=data, follow_redirects=follow_redirects, auth=auth)
        elif method == "PUT":
            response = await client.put(self.HOST + url, json=body, params=params, headers=headers,
                                        files=file,
                                        data=data, follow_redirects=follow_redirects, auth=auth)
        else:
            response = await client.delete(self.HOST + url, params=params, headers=headers,
                                           follow_redirects=follow_redirects,
                                           auth=auth)
        return response

    async def main(self):
        async with AsyncClient() as client:
            for tar in self.jobList:
                tar["client"] = client
                res = self.todo(**tar)
                task = asyncio.create_task(res)  # 创建任务
                self.taskList.append(task)
            await asyncio.gather(*self.taskList)  # 收集任务


if __name__ == '__main__':
    host = "https://www.baidu.com"
    l = [{"method": "GET", "url": ""} for i in range(100)]
    h = MyHttpx(host, l)


    start = time.time()
    asyncio.run(h.main())

    end = time.time()
    print(f'异步发送300次请求，耗时：{end - start}')
