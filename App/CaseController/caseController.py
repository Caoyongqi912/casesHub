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
        parse.add(name="case_title", T=str, required=True)
        parse.add(name="case_level", T=str, required=True)
        parse.add(name="case_desc", T=str, required=True)
        parse.add(name="case_setup", T=str, required=True)
        parse.add(name="case_type", T=str, required=False)
        parse.add(name="case_info", T=list, required=True)
        parse.add(name="projectID", T=int, isExist=Project, required=True)
        parse.add(name="casePartID", T=int, isExist=CasePart, required=True)
        CaseModel(**parse.parse_args).save()
        return MyResponse.success()

    @auth.login_required
    def put(self) -> MyResponse:
        """
        用例修改
        :return: MyResponse
        """

        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name=UID, T=str, required=True)
        parse.add(name="case_title", T=str, required=False)
        parse.add(name="case_level", T=str, required=False)
        parse.add(name="case_desc", T=str, required=False)
        parse.add(name="case_type", T=str, required=False)
        parse.add(name="case_info", T=list, required=False)
        parse.add(name="projectID", T=int, isExist=Project, required=False)
        parse.add(name="casePartID", T=int, isExist=CasePart, required=False)
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
        parse: MyRequestParseUtil = MyRequestParseUtil("values")
        parse.add(name=UID, required=True, T=str)
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
#         parse.add(name="projectID", T=int, required=True, isExist=Project)
#         parse.add(name="fileID", T=str, required=True)
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
