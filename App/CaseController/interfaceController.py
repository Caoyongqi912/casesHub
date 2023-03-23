"""
接口用例
1、crud done
1.1 、 结果入库、 调试历史
1.2 、 添加status、requestNum responseTIME、
2、运行结果校验 done
3、与结果持久化
4、快速创建接口、title part、、method 、url  、creator、desc
5、补全

"""
import time
from datetime import datetime
from typing import List

from Models.UserModel.userModel import User
from Utils.myHttpx import MyHttpx
import asyncio

from flask import g, current_app
from flask_restful import Resource
from App import auth, UID, create_app
from App.CaseController import caseBP
from Comment.myResponse import MyResponse
from Enums import CaseLevel
from Enums.myEnum import CaseAPIStatus
from Models.CaseModel.casePartModel import CasePart
from Models.CaseModel.hostModel import HostModel
from flask_restful import Api
from Utils.myRequestParseUtil import MyRequestParseUtil
from Models.CaseModel.interfaceModel import InterfaceModel, InterfaceResultModel
from Utils import MyLog
from Utils.myRequests import MyRequest

log = MyLog.get_log(__file__)


class InterfaceController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        添加接口
        :return:MyResponse
        """
        pare: MyRequestParseUtil = MyRequestParseUtil()
        pare.add(name="title", type=str, required=True)
        pare.add(name="desc", type=str)
        pare.add(name="http", default="HTTP", type=str)
        pare.add(name="level", enum=CaseLevel, required=True)
        pare.add(name="status", enum=CaseAPIStatus, required=True)

        pare.add(name="projectID", required=True, type=int)
        pare.add(name="casePartID", type=int)

        pare.add(name="steps", type=list)
        pare.add(name="connectTimeout", type=int)
        pare.add(name="responseTimeout", type=int)
        pare.add(name="creator", type=int)
        InterfaceModel(**pare.parse_args).save()
        return MyResponse.success()

    @auth.login_required
    def get(self) -> MyResponse:
        """
        by id
        :return:
        """
        pare: MyRequestParseUtil = MyRequestParseUtil("values")
        pare.add(name=UID, required=True)
        return MyResponse.success(InterfaceModel.get_by_uid(**pare.parse_args))

    @auth.login_required
    def put(self) -> MyResponse:
        """
        更新
        :return:
        """
        pare: MyRequestParseUtil = MyRequestParseUtil()
        pare.add(name=UID, required=True)
        pare.add(name="title")
        pare.add(name="desc")
        pare.add(name="http")
        pare.add(name="level", enum=CaseLevel)
        pare.add(name="status", enum=CaseAPIStatus)

        pare.add(name="steps", type=list)
        pare.add(name="connectTimeout", type=int)
        pare.add(name="responseTimeout", type=int)
        InterfaceModel.update(**pare.parse_args)
        return MyResponse.success()

    @auth.login_required
    def delete(self) -> MyResponse:
        """
        :return:
        """
        pare: MyRequestParseUtil = MyRequestParseUtil()
        pare.add(name=UID, required=True)
        InterfaceModel.delete_by_id(**pare.parse_args)
        return MyResponse.success()


class RunController(Resource):

    @auth.login_required
    def post(self):
        """
        运行
        :return:
        """
        pare: MyRequestParseUtil = MyRequestParseUtil()
        pare.add(name=UID)
        pare.add(name="HostID")
        Host = HostModel.get_by_uid(pare.parse_args.get("HostID"))
        inter = InterfaceModel.get_by_uid(pare.parse_args.get(UID))
        uid = MyRequest(HOST=Host, starter=g.user).runAPI(inter)
        return MyResponse.success(uid)


class InterfaceHistoryController(Resource):

    @auth.login_required
    def get(self) -> MyResponse:
        """
        by id
        :return:
        """
        pare: MyRequestParseUtil = MyRequestParseUtil("values")
        pare.add(name=UID)
        return MyResponse.success(InterfaceModel.get_by_uid(**pare.parse_args).query_results)


class PageInterfaceController(Resource):

    @auth.login_required
    def get(self) -> MyResponse:
        pare: MyRequestParseUtil = MyRequestParseUtil("values")
        info = InterfaceModel.page(**pare.page(InterfaceModel))
        return MyResponse.success(info)


class RunInterfaceDemo(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        pare: MyRequestParseUtil = MyRequestParseUtil()
        pare.add(name="HostID", required=True)
        pare.add(name="step", type=dict, required=False)
        from Utils.myRequests import MyRequest
        reqData = pare.parse_args
        host = HostModel.get_by_uid(uid=reqData.pop("HostID"))
        response = MyRequest(HOST=host, starter=g.user).runText(reqData.get("step"))
        return MyResponse.success(response)


class GetInterResponse(Resource):

    @auth.login_required
    def get(self):
        pare: MyRequestParseUtil = MyRequestParseUtil("values")
        pare.add(name=UID, required=True)
        return MyResponse.success(InterfaceResultModel.get_by_uid(**pare.parse_args))


async def execute_task(myHttpx: MyHttpx):
    await myHttpx.master()


class InterfaceGroupController(Resource):

    def __init__(self):
        pare: MyRequestParseUtil = MyRequestParseUtil()
        pare.add(name="hostID", required=True)
        pare.add(name="partUID", required=False)
        pare.add(name="interfaceIDs", type=list, required=False)
        self.host = HostModel.get_by_uid(pare.parse_args.get("hostID"))
        self.interfaceIDs: List[str] = pare.parse_args.get("interfaceIDs")

    @auth.login_required
    async def post(self) -> MyResponse:
        loop = asyncio.get_event_loop()
        if self.interfaceIDs:
            # interfaces = [InterfaceModel.get_by_uid(uid) for uid in self.interfaceIDs]
            interfaces = InterfaceModel.all()
            httpx = MyHttpx(interfaces, g.user, self.host)
            task = loop.create_task(httpx.master())
            resp = MyResponse.success()
            await task
            return resp
        else:
            return MyResponse.success("err")


class AsyncDemo(Resource):
    def get(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.ensure_future(self.sleep1(10)))
        loop.close()
        return MyResponse.success()

    async def sleep1(self, n):
        print(f'[sleep start]{datetime.now().strftime("%Y/%m/%d %H:%M:%S")}')
        time.sleep(n)
        print('slept!!')
        print(f'[sleep   end]{datetime.now().strftime("%Y/%m/%d %H:%M:%S")}')

    @auth.login_required
    def post(self):
        from gevent import spawn
        spawn(self.todo)
        return MyResponse.success()

    def todo(self):
        create_app().app_context().push()
        host = HostModel.get_by_uid("KcyzFXXCMFepXWIVAlat")
        interfaces = InterfaceModel.all()
        user = User.get_by_uid("vSOATEHmnwVQfeYfVaqt")
        my = MyHttpx(interfaces, user, host)
        asyncio.run(my.master())


api_script = Api(caseBP)
api_script.add_resource(InterfaceController, "/interface/opt")
api_script.add_resource(PageInterfaceController, "/interface/page")
api_script.add_resource(InterfaceHistoryController, "/interface/history")
api_script.add_resource(InterfaceGroupController, "/interface/group/run")
api_script.add_resource(RunController, "/interface/run")
api_script.add_resource(GetInterResponse, "/interface/response")
api_script.add_resource(RunInterfaceDemo, "/interface/demo")
api_script.add_resource(AsyncDemo, "/interface/async")
