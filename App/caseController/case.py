# @Time : 2022/7/16 17:27 
# @Author : cyq
# @File : case.py 
# @Software: PyCharm
# @Desc: case view
import json
from typing import AnyStr

from flask import request, g
from flask_restful import Resource, Api

from App import auth
from Comment import MyResponse, ParamError
from App.caseController import caseBP
from Enums.errorCode import ResponseMsg
from Utils import MyRequestParseUtil
from Models import Product, Platform, Version, Cases, CasePart

"""
case curd
查
    通过id查detail
    通过productID 分页 orderby
    通过casePartiD 分页 orderby
    

"""


class CasePartController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        用例模块
        :return: MyResponse
        """
        parse = MyRequestParseUtil()
        parse.add(name="partName", type=str, required=True)
        parse.add(name="productID", type=int, isExist=Product, required=True)
        CasePart(**parse.parse_args()).save()
        return MyResponse.success()

    @auth.login_required
    def get(self) -> MyResponse:
        """
        通过casePartID
        :return:MyResponse
        """
        target = "casePartID"
        parse = MyRequestParseUtil("values")
        parse.add(name=target, type=str, isExist=CasePart, required=True)
        return MyResponse.success(CasePart.get(parse.parse_args().get(target), target))

    @auth.login_required
    def put(self) -> MyResponse:
        """
        更新
        :return: MyResponse
        """
        parse = MyRequestParseUtil()
        parse.add(name="partName", type=str, required=False)
        parse.add(name="productID", type=int, required=True)
        CasePart.update(**parse.parse_args())
        return MyResponse.success()

    @auth.login_required
    def delete(self) -> MyResponse:
        """
        删除
        :return: MyResponse
        """
        parse = MyRequestParseUtil()
        parse.add(name="id", type=int, required=True)
        CasePart.delete_by_id(**parse.parse_args())
        return MyResponse.success()


class CaseController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        新增用例
        :return: MyResponse
        """
        parse = MyRequestParseUtil()
        parse.add(name="title", type=str, required=True)
        parse.add(name="tag", type=str, choices=['常规', '冒烟'], default="常规", required=False)
        parse.add(name="desc", type=str, required=True)
        parse.add(name="case_level", type=str, choices=["P1", "P2", "P3", "P4"], required=True)
        parse.add(name="case_type", type=str, choices=["功能", "接口", "性能"], default="功能", required=False)
        parse.add(name="platformID", type=int, target=Platform, required=True)
        parse.add(name="productID", type=int, isExist=Product, required=True)
        parse.add(name="partID", type=int, isExist=CasePart, required=True)
        parse.add(name="info", type=list, required=True)
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
        parse.add(name="part", type=str, required=False)
        parse.add(name="title", type=str, required=False)
        parse.add(name="desc", type=str, required=False)
        parse.add(name="case_level", type=str, choices=["P1", "P2", "P3", "P4"], required=False)
        parse.add(name="case_type", type=str, choices=["功能", "接口", "性能"], required=False)
        parse.add(name="platform", type=str, choices=["IOS", "ANDROID", "WEB", "PC", "APP"], required=False)
        parse.add(name="prd", type=str, required=False)
        parse.add(name="productID", type=int, isExist=Product, required=False)
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
        Cases.delete_by_id(**parse.parse_args())
        return MyResponse.success()

    @auth.login_required
    def get(self) -> MyResponse:
        """
        通过caseID查
        :return: MyResponse
        """
        parse = MyRequestParseUtil("values")
        parse.add(name="id", type=int, required=True, isExist=Cases)
        return MyResponse.success(Cases.get(parse.parse_args().get("id"), "caseID"))


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


class ExcelPut(Resource):

    @auth.login_required
    def post(self):
        from werkzeug.utils import secure_filename
        from faker import Faker
        from Utils.myPath import getExcelPath
        from Utils.myExcel import MyExcel
        f = Faker()
        file = request.files.get("file")
        parse = MyRequestParseUtil("values")
        parse.add(name="productID", required=True, isExist=Product)
        parse.add(name="versionID", required=True, isExist=Version)
        parse.parse_args().setdefault('creator', g.user.id)
        fileName = f.pystr() + '_' + secure_filename(file.filename)  # excel名称
        filePath = getExcelPath(fileName)  # excel路径
        file.save(filePath)  # 存储头像
        try:
            MyExcel(filePath).save(**parse.parse_args())
            return MyResponse.success()
        except Exception as e:
            return ParamError.error(ResponseMsg.ERROR_EXCEL)


api_script = Api(caseBP)
api_script.add_resource(CaseController, "/opt")
api_script.add_resource(QueryBugs, "/<string:caseID>/bugs")
api_script.add_resource(ExcelPut, "/upload/excel")
api_script.add_resource(CasePartController, "/part/opt")
