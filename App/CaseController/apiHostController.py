from flask_restful import Resource

from App.CaseController import caseBP
from Comment.myResponse import MyResponse
from Models.ProjectModel.project import Project
from MyException import Api
from App import auth
from Models.CaseModel.hostModel import HostModel
from Utils.myRequestParseUtil import MyRequestParseUtil


class HostController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        添加host
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="name", type=str, required=True)
        parse.add(name="host", type=str, required=True)
        parse.add(name="projectID", type=int, required=True, isExist=Project)
        HostModel(**parse.parse_args()).save()
        return MyResponse.success()

    @auth.login_required
    def get(self) -> MyResponse:
        """
        get by Host ID
        :return:
        """
        parse: MyRequestParseUtil = MyRequestParseUtil("values")
        parse.add(name="hostID", required=True, isExist=Project)
        return MyResponse.success(HostModel.get(parse.parse_args().get("hostID")))

    @auth.login_required
    def delete(self) -> MyResponse:
        """
        id 删除
        :return:
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="hostID", type=int, required=True)
        HostModel.delete_by_id(parse.parse_args().get("hostID"))
        return MyResponse.success()


api_script = Api(caseBP)
api_script.add_resource(HostController, "/host/opt")
