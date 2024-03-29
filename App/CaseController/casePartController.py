# @Time : 2022/9/14 20:28 
# @Author : cyq
# @File : casePartController.py 
# @Software: PyCharm
# @Desc:
from typing import List

from flask_restful import Resource

from App import auth, UID, auth
from App.CaseController import caseBP
from Comment.myResponse import MyResponse
from Models.CaseModel.casePartModel import CasePart
from Models.ProjectModel.projectModel import Project
from flask_restful import Api
from Utils import MyTools
from Utils.myRequestParseUtil import MyRequestParseUtil


class CasePartController(Resource):
    @auth.login_required
    def post(self) -> MyResponse:
        """
        添加用例模块
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="partName", T=str, required=True)
        parse.add(name="projectID", T=int, isExist=Project, required=True)
        parse.add(name="parentID", T=int)
        CasePart(**parse.parse_args).save_()
        return MyResponse.success()

    @auth.login_required
    def get(self) -> MyResponse:
        """
        通过casePartID 获取用例集
        :return:MyResponse
        """
        parse = MyRequestParseUtil("values")
        parse.add(name=UID, required=True)
        return MyResponse.success(CasePart.get_by_uid(**parse.parse_args))

    @auth.login_required
    def put(self) -> MyResponse:
        """
        更新
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="id", required=True, T=int)
        parse.add(name="partName")
        CasePart.update(**parse.parse_args)
        return MyResponse.success()

    @auth.login_required
    def delete(self) -> MyResponse:
        """
        删除
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="id", required=True, T=int)
        CasePart.part_delete(**parse.parse_args)
        return MyResponse.success()


class QueryCasePartController(Resource):

    @auth.login_required
    def get(self) -> MyResponse:
        parse = MyRequestParseUtil("values")
        parse.add(name="projectID", required=True)
        pro: Project = Project.get(id=parse.parse_args.get("projectID"))

        return MyResponse.success(MyTools.list2Tree(pro.tree_casePart))


class CasePartOrCreateController(Resource):

    @auth.login_required
    def get(self) -> MyResponse:
        """
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil("values")
        parse.add(name="partName", T=str, required=True)
        parse.add(name="projectID", T=str, required=True)
        return MyResponse.success(CasePart.getOrCreate(**parse.parse_args))


class QueryInterfaceController(Resource):

    @auth.login_required
    def get(self) -> MyResponse:
        parse: MyRequestParseUtil = MyRequestParseUtil("values")
        parse.add(name='casePartID', required=True)
        part: CasePart = CasePart.get(id=parse.parse_args.get("casePartID"))

        return MyResponse.success(part.query_interfaces)


api_script = Api(caseBP)
api_script.add_resource(CasePartController, "/part/opt")
api_script.add_resource(QueryInterfaceController, "/part/interfaces")
api_script.add_resource(QueryCasePartController, "/part/query")
api_script.add_resource(CasePartOrCreateController, "/part/getOrCreate")
