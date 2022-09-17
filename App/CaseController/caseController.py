# @Time : 2022/7/16 17:27 
# @Author : cyq
# @File : caseController.py
# @Software: PyCharm
# @Desc: case view

from flask import g
from flask_restful import Resource
from Models.CaseModel.caseExcel import CaseExcel
from MyException import Api
from App import auth, siwa, limiter
from App.CaseController import caseBP
from Comment.myException import MyResponse, ParamError
from Enums import CaseTag, CaseLevel, CaseType
from Models.CaseModel.caseModel import Cases
from Models.CaseModel.partModel import CasePart
from Models.CaseModel.platforms import Platform
from Models.ProjectModel.project import Project
from Models.ProjectModel.versions import Version
from Utils.myRequestParseUtil import MyRequestParseUtil
from Swagger import CaseSwagger, BaseResponseSwagger
from Utils import MyLog

log = MyLog.get_log(__file__)


class CaseController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        新增用例
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="title", type=str, required=True)
        parse.add(name="desc", type=str, required=True)
        parse.add(name="setup", type=str, required=False)

        parse.add(name="tag", enum=CaseTag, required=True)
        parse.add(name="case_level", enum=CaseLevel, required=True)
        parse.add(name="case_type", enum=CaseType, required=False)

        parse.add(name="platformID", type=int, isExist=Platform, required=False)
        parse.add(name="projectID", type=int, isExist=Project, required=False)
        parse.add(name="partID", type=int, isExist=CasePart, required=False)
        parse.add(name="versionID", type=int, isExist=Version, required=False)
        parse.add(name="info", type=list, required=True)
        Cases(**parse.parse_args()).save()
        return MyResponse.success()

    @auth.login_required
    def put(self) -> MyResponse:
        """
        用例修改
        :return: MyResponse
        """

        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="id", type=int, required=True, isExist=Cases)
        parse.add(name="part", type=str, required=False)
        parse.add(name="title", type=str, required=False)
        parse.add(name="desc", type=str, required=False)
        parse.add(name="case_level", type=str, enum=CaseLevel, required=False)
        parse.add(name="case_type", type=str, enum=CaseType, required=False)
        parse.add(name="platformID", type=int, required=False)
        parse.add(name="projectID", type=int, required=False)
        parse.add(name="versionID", type=int, required=False)
        parse.add(name="steps", type=list, required=False)
        Cases.update(**parse.parse_args())
        return MyResponse.success()

    @auth.login_required
    def delete(self) -> MyResponse:
        """
        通过id删除
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
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
        parse.add(name="caseID", required=True, isExist=Cases)
        return MyResponse.success(Cases.get(parse.parse_args().get("caseID"), "caseID"))


class QueryBugs(Resource):
    @auth.login_required
    def get(self, caseID) -> MyResponse:
        """
        获取单个case下的所有bug
        :return: MyResponse
        """
        case = Cases.get(caseID, "caseID")
        return MyResponse.success(case.bugs)


class UpdateExcel2CaseController(Resource):

    @auth.login_required
    @limiter.limit("1/minute")  # 一分钟一次
    def post(self) -> MyResponse:
        """
        excel文件录入sql
        :return:
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="projectID", type=int, required=True, isExist=Project)
        parse.add(name="fileID", type=str, required=True)
        fileID: str = parse.parse_args().get("fileID")
        file = CaseExcel.get_by_uid(fileID)
        projectID: int = parse.parse_args().get("projectID")
        filePath: str = file.filePath
        # from celery_task.tasks import caseExcelWrite2Sql
        # caseExcelWrite2Sql.delay(projectID, g.user.id, filePath)
        from Utils.myExcel import MyExcel
        MyExcel(filePath).sheetReader(projectID, g.user.id)
        return MyResponse.success()


api_script = Api(caseBP)
api_script.add_resource(CaseController, "/opt")
api_script.add_resource(QueryBugs, "/<string:caseID>/bugs")
api_script.add_resource(UpdateExcel2CaseController, "/upload/excel")
