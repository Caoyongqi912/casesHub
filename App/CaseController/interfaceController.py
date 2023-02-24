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
from typing import Dict, Any

from flask import g
from flask_restful import Resource
from App import auth, UID
from App.CaseController import caseBP
from Comment.myResponse import MyResponse
from Enums import CaseLevel
from Enums.myEnum import CaseAPIStatus
from MyException import Api
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
        Host = "http://127.0.0.1:8080"
        inter = InterfaceModel.get_by_uid(**pare.parse_args)
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
        pare.add(name="method", required=True)
        pare.add(name="name", required=True)
        pare.add(name="url", required=True)
        pare.add(name="headers", required=False, type=list)
        pare.add(name="body", type=dict, required=False)
        from Utils.myRequests import MyRequest
        log.info(pare.parse_args)
        response = MyRequest(HOST="http://127.0.0.1:8080", starter=g.user).runDemo(**pare.parse_args)
        log.info(response)
        return MyResponse.success(response)


class GetInterResponse(Resource):

    @auth.login_required
    def get(self):
        pare: MyRequestParseUtil = MyRequestParseUtil("values")
        pare.add(name=UID, required=True)
        return MyResponse.success(InterfaceResultModel.get_by_uid(**pare.parse_args))


api_script = Api(caseBP)
api_script.add_resource(InterfaceController, "/interface/opt")
api_script.add_resource(PageInterfaceController, "/interface/page")
api_script.add_resource(InterfaceHistoryController, "/interface/history")
api_script.add_resource(RunController, "/interface/run")
api_script.add_resource(GetInterResponse, "/interface/response")
api_script.add_resource(RunInterfaceDemo, "/interface/demo")
