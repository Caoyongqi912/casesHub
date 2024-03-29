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
from typing import List

import Utils
from App import io

from Models.UserModel.userModel import User
from flask import g, request, current_app
from flask_restful import Resource
from App import auth, UID, create_app
from App.CaseController import caseBP
from Comment.myResponse import MyResponse
from Enums import CaseLevel
from Enums.myEnum import CaseAPIStatus
from flask_restful import Api
from Utils.myRequestParseUtil import MyRequestParseUtil
from Models.CaseModel.interfaceModel import InterfaceModel, InterfaceResultModel, InterfaceGroupResultModel
from Utils import MyLog, UUID
from Utils.apiRunner import ApiRunner

log = MyLog.get_log(__file__)


class InterfaceController(Resource):
    """
    接口用例增删改查
    """

    @auth.login_required
    def post(self) -> MyResponse:
        """
        添加接口
        :return:MyResponse
        """
        pare: MyRequestParseUtil = MyRequestParseUtil()
        pare.add(name="title", T=str, unique=InterfaceModel, required=True)
        pare.add(name="desc", T=str)
        pare.add(name="http", default="HTTP", T=str)
        pare.add(name="level", enum=CaseLevel, required=True)
        pare.add(name="status", enum=CaseAPIStatus, required=True)
        pare.add(name="projectID", required=True, T=int)
        pare.add(name="casePartID", T=int)
        pare.add(name="steps", T=list)
        pare.add(name="connectTimeout", T=int)
        pare.add(name="responseTimeout", T=int)
        pare.add(name="creator", T=int)
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

        pare.add(name="steps", T=list)
        pare.add(name="connectTimeout", T=int)
        pare.add(name="responseTimeout", T=int)
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
        inter = InterfaceModel.get_by_uid(pare.parse_args.get(UID))
        uid = ApiRunner(starter=g.user).runAPI(inter=inter)
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

        log.info(info)
        return MyResponse.success(info)


class RunInterfaceDemo(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        pare: MyRequestParseUtil = MyRequestParseUtil()
        pare.add(name="step", T=dict, required=False)
        from Utils.apiRunner import ApiRunner
        reqData = pare.parse_args
        response = ApiRunner(starter=g.user).runTest(reqData.get("step"))
        return MyResponse.success(response)


class GetInterResponse(Resource):

    @auth.login_required
    def get(self):
        pare: MyRequestParseUtil = MyRequestParseUtil("values")
        pare.add(name=UID, required=True)
        return MyResponse.success(InterfaceResultModel.get_by_uid(**pare.parse_args))


class InterfacesController(Resource):

    def __init__(self):
        pare: MyRequestParseUtil = MyRequestParseUtil()
        pare.add(name="interfaceIDs", T=list, required=True)
        self.interfaceIDs: List[str] = pare.parse_args.get("interfaceIDs")
        self.interfaces = [InterfaceModel.get_by_uid(uid) for uid in self.interfaceIDs]

    @auth.login_required
    def post(self):
        from gevent import spawn
        user: User = g.user
        user.detach()
        spawn(self.worker, user)
        return MyResponse.success()

    def worker(self, user: User):
        create_app().app_context().push()
        interfaces = [InterfaceModel.get_by_uid(uid) for uid in self.interfaceIDs]

        ApiRunner(user).runApis(interfaces)


class QueryInterfaceGroupResult(Resource):

    @auth.login_required
    def get(self) -> MyResponse:
        pare: MyRequestParseUtil = MyRequestParseUtil("values")
        info = InterfaceGroupResultModel.page(**pare.page(InterfaceGroupResultModel))
        return MyResponse.success(info)


class PageInterfaceResultController(Resource):

    @auth.login_required
    def get(self):
        pare: MyRequestParseUtil = MyRequestParseUtil("values")
        info = InterfaceResultModel.page(**pare.page(InterfaceResultModel))
        return MyResponse.success(info)


class GetInterfacesResultInfo(Resource):

    @auth.login_required
    def get(self) -> MyResponse:
        parse: MyRequestParseUtil = MyRequestParseUtil("values")
        parse.add(name=UID, required=True, T=str)
        info = InterfaceGroupResultModel.get_by_uid(**parse.parse_args)
        return MyResponse.success(info)


class SocketIODEMO(Resource):

    def job(self, roomID):
        from flask_socketio import join_room
        from App import io
        log.info(f'=====rommid {roomID} ========')

        for i in range(10):
            # 模拟任务执行并输出日志信息
            log_msg = f"Task is running, progress: {i} \n"
            io.emit('log', {"code": 1, "msg": log_msg}, to=roomID)  # 将日志信息发送给前端
            time.sleep(1)
        io.emit("log", {"code": 0, "msg": "Done"}, to=roomID)

    def get(self):
        roomID = UUID().getUUID
        io.start_background_task(self.job, roomID)  # 启动后台任务
        return MyResponse.success(roomID)

    def post(self):
        return MyResponse.success()


api_script = Api(caseBP)
api_script.add_resource(SocketIODEMO, "/log")

api_script.add_resource(InterfaceController, "/interface/opt")
api_script.add_resource(PageInterfaceController, "/interface/page")
api_script.add_resource(GetInterfacesResultInfo, "/interfaces/report/info")
api_script.add_resource(QueryInterfaceGroupResult, "/interfaces/result/page")
api_script.add_resource(PageInterfaceResultController, "/interface/result/page")
api_script.add_resource(InterfacesController, "/interfaces/run")
api_script.add_resource(RunController, "/interface/run")
api_script.add_resource(GetInterResponse, "/interface/response")
api_script.add_resource(RunInterfaceDemo, "/interface/demo")
