# @Time : 2022/9/14 20:28 
# @Author : cyq
# @File : casePartController.py 
# @Software: PyCharm
# @Desc:
from flask_restful import Resource

from App import auth
from App.CaseController import caseBP
from Comment.myResponse import MyResponse
from Models.CaseModel.partModel import CasePart
from Models.ProjectModel.project import Project
from MyException import Api
from Utils.myRequestParseUtil import MyRequestParseUtil


class CasePartController(Resource):
    @auth.login_required
    def post(self) -> MyResponse:
        """
        添加用例模块
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="partName", type=str, unique=CasePart, required=True)
        parse.add(name="projectID", type=int, isExist=Project, required=True)
        CasePart(**parse.parse_args()).save()
        return MyResponse.success()

    @auth.login_required
    def get(self) -> MyResponse:
        """
        通过casePartID 获取用例集
        :return:MyResponse
        """
        target = "casePartID"
        parse = MyRequestParseUtil("values")
        parse.add(name=target, isExist=CasePart, required=True)
        return MyResponse.success(CasePart.get(parse.parse_args().get(target), target))

    @auth.login_required
    def put(self) -> MyResponse:
        """
        更新
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name='id', type=int, required=True)
        parse.add(name="partName", type=str, required=False)
        CasePart.update(**parse.parse_args())
        return MyResponse.success()

    @auth.login_required
    def delete(self) -> MyResponse:
        """
        删除
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="id", type=int, required=True)
        CasePart.delete_by_id(**parse.parse_args())
        return MyResponse.success()


class PageCasePartController(Resource):

    @auth.login_required
    def get(self) -> MyResponse:
        parse = MyRequestParseUtil("values")
        return MyResponse.success(CasePart.page(parse.page(CasePart)))


class CasePartOrCreateController(Resource):

    @auth.login_required
    def get(self) -> MyResponse:
        """
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil("values")
        parse.add(name="partName", type=str, required=True)
        parse.add(name="projectID", type=str, required=True)
        return MyResponse.success(CasePart.getOrCreate(**parse.parse_args()))


api_script = Api(caseBP)
api_script.add_resource(CasePartController, "/part/opt")
api_script.add_resource(PageCasePartController, "/part/page")
api_script.add_resource(CasePartOrCreateController, "/part/getOrCreate")
