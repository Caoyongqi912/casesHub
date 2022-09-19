from flask_restful import Resource
from App.CaseController import caseBP
from Comment.myResponse import MyResponse
from Models.ProjectModel.project import Project
from MyException import Api
from App import auth
from Models.CaseModel.variableModel import VariableModel
from Utils.myRequestParseUtil import MyRequestParseUtil

"""
:type constant , List,random
"""


class VariableController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        添加全局变量
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="key", type=str, required=True)
        parse.add(name="val", type=str, required=True)
        parse.add(name="projectID", type=int, required=True, isExist=Project)
        VariableModel(**parse.parse_args()).save()
        return MyResponse.success()

    @auth.login_required
    def get(self) -> MyResponse:
        parse: MyRequestParseUtil = MyRequestParseUtil("values")
        parse.add(name="variableID", required=True, isExist=Project)
        return MyResponse.success(VariableModel.get(parse.parse_args().get("envID")))

    @auth.login_required
    def delete(self) -> MyResponse:
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="variableID", type=int, required=True)
        VariableModel.delete_by_id(parse.parse_args().get("envID"))
        return MyResponse.success()


api_script = Api(caseBP)
api_script.add_resource(VariableController, "/variable/opt")
