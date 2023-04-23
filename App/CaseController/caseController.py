# @Time : 2022/7/16 17:27 
# @Author : cyq
# @File : caseController.py
# @Software: PyCharm
# @Desc: case view

from flask_restful import Resource
from flask_restful import Api
from App import auth, limiter, UID, auth
from App.CaseController import caseBP
from Comment.myException import MyResponse
from Models.CaseModel.caseModel import CaseModel
from Models.CaseModel.casePartModel import CasePart
from Models.ProjectModel.projectModel import Project
from Utils.myRequestParseUtil import MyRequestParseUtil
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
        parse.add(name="case_title", type=str, required=True)
        parse.add(name="case_level", type=str, required=True)
        parse.add(name="case_desc", type=str, required=True)
        parse.add(name="case_type", type=str, required=False)
        parse.add(name="case_info", type=list, required=True)
        parse.add(name="projectID", type=int, isExist=Project, required=True)
        parse.add(name="casePartID", type=int, isExist=CasePart, required=True)
        CaseModel(**parse.parse_args).save()
        return MyResponse.success()

    @auth.login_required
    def put(self) -> MyResponse:
        """
        用例修改
        :return: MyResponse
        """

        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name=UID, type=int, required=True, isExist=CaseModel)
        parse.add(name="case_title", type=str, required=False)
        parse.add(name="case_level", type=str, required=False)
        parse.add(name="case_desc", type=str, required=False)
        parse.add(name="case_type", type=str, required=False)
        parse.add(name="case_info", type=list, required=False)
        parse.add(name="projectID", type=int, isExist=Project, required=False)
        parse.add(name="casePartID", type=int, isExist=CasePart, required=False)
        CaseModel.update(**parse.parse_args)
        return MyResponse.success()

    @auth.login_required
    def delete(self) -> MyResponse:
        """
        通过uid删除
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name=UID, required=True)
        CaseModel.delete_by_id(**parse.parse_args)
        return MyResponse.success()

    @auth.login_required
    def get(self) -> MyResponse:
        """
        uid查询
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name=UID, required=True, type=str)
        return MyResponse.success(CaseModel.get_by_uid(**parse.parse_args))


# class UpdateExcel2CaseController(Resource):
#
#     @auth.login_required
#     @limiter.limit("1/minute")  # 一分钟一次
#     def post(self) -> MyResponse:
#         """
#         excel文件录入sql
#         :return:
#         """
#         parse: MyRequestParseUtil = MyRequestParseUtil()
#         parse.add(name="projectID", type=int, required=True, isExist=Project)
#         parse.add(name="fileID", type=str, required=True)
#         fileID: str = parse.parse_args.get("fileID")
#         file = CaseExcel.get_by_uid(fileID)
#         projectID: int = parse.parse_args.get("projectID")
#         filePath: str = file.filePath
#         # from celery_task.tasks import caseExcelWrite2Sql
#         # caseExcelWrite2Sql.delay(projectID, g.user.id, filePath)
#         from Utils.myExcel import MyExcel
#         MyExcel(filePath).sheetReader(projectID, g.user.id)
#         return MyResponse.success()


class PageCaseController(Resource):

    @auth.login_required
    def get(self) -> MyResponse:
        """
        用例分页
        :return:
        """
        parse = MyRequestParseUtil("values")
        return MyResponse.success(CaseModel.page(**parse.page(CaseModel)))


api_script = Api(caseBP)
api_script.add_resource(CaseController, "/opt")
api_script.add_resource(PageCaseController, "/page")
