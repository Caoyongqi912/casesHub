from flask_restful import Resource

from App.CaseController import caseBP
from Comment.myResponse import MyResponse
from flask_restful import Api
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
        parse.add(name="name", T=str, required=True)
        parse.add(name="host", T=str, required=True)
        parse.add(name="port", T=str, required=False)
        parse.add(name="desc")
        HostModel(**parse.parse_args).save()
        return MyResponse.success()

    @auth.login_required
    def get(self) -> MyResponse:
        """
        分页
        :return:
        """
        parse: MyRequestParseUtil = MyRequestParseUtil("values")
        return MyResponse.success(HostModel.page(**parse.page(HostModel)))

    @auth.login_required
    def put(self) -> MyResponse:
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name=UID, required=True)
        parse.add(name="name", T=str)
        parse.add(name="host", T=str)
        parse.add(name="desc", T=str)
        HostModel.update(**parse.parse_args)
        return MyResponse.success()

    @auth.login_required
    def delete(self) -> MyResponse:
        """
        id 删除
        :return:
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name=UID, required=True)
        HostModel.delete_by_id(**parse.parse_args)
        return MyResponse.success()


class QueryHost(Resource):

    @auth.login_required
    def get(self) -> MyResponse:
        """
        获取hosts
        :return:
        """
        return MyResponse.success(HostModel.all())


api_script = Api(caseBP)
api_script.add_resource(HostController, "/host/opt")
api_script.add_resource(QueryHost, "/host/query")
