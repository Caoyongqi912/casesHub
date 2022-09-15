from flask_restful import Resource
from App.CaseController import caseBP
from Comment.myResponse import MyResponse
from Models.ProjectModel.project import Project
from MyException import Api
from App import auth
from Models.CaseModel.envValueModel import EnvValueModel
from Utils.myRequestParseUtil import MyRequestParseUtil


class EnvValueController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        添加全局变量
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="name", type=str, required=True)
        parse.add(name="value", type=str, required=True)
        parse.add(name="projectID", type=int, required=True, isExist=Project)
        EnvValueModel(**parse.parse_args()).save()
        return MyResponse.success()

    @auth.login_required
    def get(self) -> MyResponse:
        parse: MyRequestParseUtil = MyRequestParseUtil("values")
        parse.add(name="envID", required=True, isExist=Project)
        return MyResponse.success(EnvValueModel.get(parse.parse_args().get("envID")))

    @auth.login_required
    def delete(self) -> MyResponse:
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="envID", type=int, required=True)
        EnvValueModel.delete_by_id(parse.parse_args().get("envID"))
        return MyResponse.success()


api_script = Api(caseBP)
api_script.add_resource(EnvValueController, "/env/opt")
