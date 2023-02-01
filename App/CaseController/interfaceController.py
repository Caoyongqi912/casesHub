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
from Models.CaseModel.interfaceModel import InterfaceModel


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
        pare.add(name=UID)
        return MyResponse.success(InterfaceModel.get_by_uid(**pare.parse_args))

    @auth.login_required
    def put(self) -> MyResponse:
        """
        更新
        :return:
        """
        pare: MyRequestParseUtil = MyRequestParseUtil()
        pare.add(name=UID, type=int, required=True)
        pare.add(name="title")
        pare.add(name="desc")
        pare.add(name="http")
        pare.add(name="level", enum=CaseLevel)
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
        pare.add(name="interfaceID", type=int)
        return MyResponse.success()


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


api_script = Api(caseBP)
api_script.add_resource(InterfaceController, "/interface/opt")
api_script.add_resource(InterfaceHistoryController, "/interface/history")
api_script.add_resource(RunController, "/interface/run")
