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
from MyException import Api
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
        parse.add(name="partName", type=str, required=True)
        parse.add(name="projectID", type=int, isExist=Project, required=True)
        parse.add(name="parentID", type=int)
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
        parse.add(name="id", required=True, type=int)
        parse.add(name="partName")
        CasePart.update_by_id(**parse.parse_args)
        return MyResponse.success()

    @auth.login_required
    def delete(self) -> MyResponse:
        """
        删除
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="id", required=True, type=int)
        part: CasePart = CasePart.get(**parse.parse_args)
        childrens: List[CasePart] = CasePart.get_by_field(parentID=part.id)
        for c in childrens:
            c.delete()
        part.delete()
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
        parse.add(name="partName", type=str, required=True)
        parse.add(name="projectID", type=str, required=True)
        return MyResponse.success(CasePart.getOrCreate(**parse.parse_args))


api_script = Api(caseBP)
api_script.add_resource(CasePartController, "/part/opt")
api_script.add_resource(QueryCasePartController, "/part/query")
api_script.add_resource(CasePartOrCreateController, "/part/getOrCreate")
