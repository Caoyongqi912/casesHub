# @Time : 2022/7/16 17:27 
# @Author : cyq
# @File : case.py 
# @Software: PyCharm
# @Desc: case view
import json
from typing import AnyStr

from flask_restful import Resource, Api

from App import auth
from Comment.myResponse import MyResponse
from App.caseController import caseBP
from Utils.myRequestParseUtil import MyRequestParseUtil
from Models.CaseModel.cases import Cases
from Models.ProjectModel.pro import Product
from Models.ProjectModel.versions import Version
from Models.CaseModel.platforms import Platform


class NewCaseController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        新增用例
        :return: MyResponse
        """
        parse = MyRequestParseUtil()
        parse.add(name="title", type=str, required=True, unique=Cases)
        parse.add(name="desc", type=str, required=True)
        parse.add(name="case_level", type=str, choices=["P1", "P2", "P3", "P4"], required=True)
        parse.add(name="case_type", type=str, choices=["功能", "接口", "性能"], required=False)
        parse.add(name="prd", type=str, required=True)
        parse.add(name="productID", type=int, isExist=Product, required=True)
        parse.add(name="platformID", type=int, isExist=Platform, required=True)
        parse.add(name="versionID", type=int, isExist=Version, required=True)
        parse.add(name="steps", type=list, required=True)
        Cases(**parse.parse_args()).save()
        return MyResponse.success()

    @auth.login_required
    def put(self) -> MyResponse:
        """
        用例修改
        :return: MyResponse
        """

        parse = MyRequestParseUtil()
        parse.add(name="id", type=int, required=True, isExist=Cases)
        parse.add(name="title", type=str, required=False)
        parse.add(name="desc", type=str, required=False)
        parse.add(name="case_level", type=str, choices=["P1", "P2", "P3", "P4"], required=False)
        parse.add(name="case_type", type=str, choices=["功能", "接口", "性能"], required=False)
        parse.add(name="prd", type=str, required=False)
        parse.add(name="productID", type=int, isExist=Product, required=False)
        parse.add(name="platformID", type=int, isExist=Platform, required=False)
        parse.add(name="versionID", type=int, isExist=Version, required=False)
        parse.add(name="steps", type=list, required=False)
        Cases.update(**parse.parse_args())
        return MyResponse.success()

    @auth.login_required
    def delete(self) -> MyResponse:
        """
        通过id删除
        :return: MyResponse
        """
        parse = MyRequestParseUtil()
        parse.add(name="id", type=int, required=True, isExist=Cases)
        Cases.delete_by_id(parse.parse_args().get("id"))
        return MyResponse.success()


class FindCase(Resource):

    @auth.login_required
    def get(self, caseID: AnyStr) -> MyResponse:
        """
        通过ID
        :param caseID: caseID
        :return: MyResponse
        """
        return MyResponse.success(Cases.get(int(caseID), "caseID"))


class QueryBugs(Resource):

    @auth.login_required
    def get(self, caseID) -> MyResponse:
        """
        获取case下的所有bug
        :return: MyResponse
        """
        case = Cases.get(caseID, "caseID")
        return MyResponse.success(case.bugs)


api_script = Api(caseBP)
api_script.add_resource(NewCaseController, "")
api_script.add_resource(FindCase, "/<string:caseID>")
api_script.add_resource(QueryBugs, "/<string:caseID>/bugs")
