from flask_restful import Resource

from App.CaseController import caseBP
from Comment.myResponse import MyResponse
from Models.ProjectModel.projectModel import Project
from MyException import Api
from App import auth, UID, auth
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
        parse.add(name="projectID", type=int, required=True)
        HostModel(**parse.parse_args()).save_()

        return MyResponse.success()

    @auth.login_required
    def get(self) -> MyResponse:
        """
        get by Host ID
        :return:
        """
        parse: MyRequestParseUtil = MyRequestParseUtil("values")
        parse.add(name=UID, required=True)
        return MyResponse.success(HostModel.get_by_uid(**parse.parse_args()))

    @auth.login_required
    def put(self) -> MyResponse:
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name=UID, required=True)
        parse.add(name="name", type=str)
        parse.add(name="host", type=str)
        HostModel.update(**parse.parse_args())
        return MyResponse.success()

    @auth.login_required
    def delete(self) -> MyResponse:
        """
        id 删除
        :return:
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name=UID, required=True)
        HostModel.delete_by_id(**parse.parse_args())
        return MyResponse.success()


class QueryHostController(Resource):

    @auth.login_required
    def get(self) -> MyResponse:
        parse: MyRequestParseUtil = MyRequestParseUtil("values")
        parse.add(name="projectID", required=False)
        pid = parse.parse_args().get("projectID")
        if pid:
            p: Project = Project.get(pid)
            return MyResponse.success(p.query_host)

        return MyResponse.success(HostModel.all())


api_script = Api(caseBP)
api_script.add_resource(HostController, "/host/opt")
api_script.add_resource(QueryHostController, "/host/query")
