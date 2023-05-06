from flask_restful import Resource
from App.CaseController import caseBP
from Comment.myResponse import MyResponse
from Models.ProjectModel.projectModel import Project
from flask_restful import Api
from App import auth, UID
from Models.CaseModel.variableModel import VariableModel
from Utils.myRequestParseUtil import MyRequestParseUtil

"""
api 运行全局环境变量
:type constant , List, random
"""


class VariableController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        添加或者修改全局变量
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="key", T=str, required=True)
        parse.add(name="val", T=str, required=True)
        parse.add(name="desc", T=str, required=False)
        parse.add(name="projectID", T=int, required=True, isExist=Project)
        key = {"key": parse.parse_args.get("key")}
        variable: VariableModel = VariableModel.get_by_field(**key)
        if variable:
            variable.val = parse.parse_args.get("val")
            variable.save()
        else:

            VariableModel(**parse.parse_args).save()
        return MyResponse.success()

    @auth.login_required
    def get(self) -> MyResponse:
        parse: MyRequestParseUtil = MyRequestParseUtil("values")
        parse.add(name=UID, required=True, isExist=Project)
        return MyResponse.success(VariableModel.get_by_uid(**parse.parse_args))

    @auth.login_required
    def delete(self) -> MyResponse:
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name=UID, T=int, required=True)
        VariableModel.delete_by_id(**parse.parse_args)
        return MyResponse.success()


api_script = Api(caseBP)
api_script.add_resource(VariableController, "/variable/opt")
