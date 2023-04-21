# @Time : 2022/7/16 18:09 
# @Author : cyq
# @File : versionController.py
# @Software: PyCharm
# @Desc: version view
from flask_restful import Resource
from flask_restful import Api
from App import auth
from App.CaseController import caseBP
from Comment.myException import MyResponse
from Models.CaseModel.bugModel import Bug
from Models.CaseModel.caseOldModel import Cases
from Models.ProjectModel.projectModel import Project
from Utils.myRequestParseUtil import MyRequestParseUtil
from Models.ProjectModel.versions import Version
from App.myAuth import is_admin


class VersionController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        新建版本
        不打算做权限校验
        :return:
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name='name', required=True, type=str)
        parse.add(name="projectID", required=True, type=int, isExist=Project)
        parse.add(name="desc", required=False, type=str)
        Version(**parse.parse_args).save()
        return MyResponse.success()

    @auth.login_required
    @is_admin
    def delete(self) -> MyResponse:
        """
        delete
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="id", type=int, required=True)
        Version.delete_by_id(**parse.parse_args)
        return MyResponse.success()

    @auth.login_required
    def put(self) -> MyResponse:
        """
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="id", type=int, required=True)
        parse.add(name='name', required=False, type=str)
        parse.add(name="desc", required=False, type=str)
        Version.update(**parse.parse_args)
        return MyResponse.success()

    @auth.login_required
    def get(self) -> MyResponse:
        """
        get
        :return: MyResponse
        """
        parse = MyRequestParseUtil("values")
        parse.add(name="versionID", type=str, required=True)
        return MyResponse.success(Version.get(parse.parse_args.get("versionID"), "versionID"))


class PageCases(Resource):

    @auth.login_required
    def get(self, versionID: Version.id) -> MyResponse:
        """
        查询版本用例分页
        :param versionID:Version.id
        :return:MyResponse
        """
        parse = MyRequestParseUtil("values")
        return MyResponse.success(Version.get(versionID, "versionID").page_cases(**parse.page(Cases)))


class PageBugs(Resource):

    @auth.login_required
    def get(self, versionID: Version) -> MyResponse:
        """
        查询版本用例分页
        :param versionID:Version.id
        :return:MyResponse
        """
        parse = MyRequestParseUtil("values")
        return MyResponse.success(Version.get(versionID, "versionID").page_bugs(**parse.page(Bug)))


api_script = Api(caseBP)
api_script.add_resource(VersionController, "/version/opt")
api_script.add_resource(PageCases, "/version/<string:versionID>/page_case")
api_script.add_resource(PageBugs, "/version/<string:versionID>/page_bugs")
