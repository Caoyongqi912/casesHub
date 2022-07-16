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
        case = parse.parse_args()
        Cases(**case).save()
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


api_script = Api(caseBP)
api_script.add_resource(NewCaseController, "/new")
api_script.add_resource(FindCase, "/find/<string:caseID>")
