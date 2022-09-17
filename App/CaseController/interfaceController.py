"""
接口用例
1、crud
2、运行结果校验与结果持久化
"""

from flask_restful import Resource
from App import auth
from App.CaseController import caseBP
from Comment.myResponse import MyResponse
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
        pare.add(name="projectID", required=True, type=int)
        pare.add(name="desc", type=str)
        pare.add(name="steps", type=list)
        pare.add(name="mark", type=str)
        pare.add(name="partID", type=int)
        pare.add(name="versionID", type=int)
        pare.add(name="connectTimeout", type=int)
        pare.add(name="responseTimeout", type=int)
        pare.add(name="creator", type=int)
        pare.add(name="updater", type=int)
        InterfaceModel(**pare.parse_args()).save()
        return MyResponse.success()

    @auth.login_required
    def get(self) -> MyResponse:
        """
        by id
        :return:
        """
        pare: MyRequestParseUtil = MyRequestParseUtil("values")
        pare.add(name="interfaceID")
        return MyResponse.success(InterfaceModel.get_by_uid(pare.parse_args().get("interfaceID")))


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


api_script = Api(caseBP)
api_script.add_resource(InterfaceController, "/interface/opt")
api_script.add_resource(RunController, "/interface/run")
