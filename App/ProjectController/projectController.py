# @Time : 2022/7/14 20:05 
# @Author : cyq
# @File : projectController.py
# @Software: PyCharm
# @Desc: 项目view
from typing import AnyStr

from flask_restful import Resource

from Models.CaseModel.hostModel import HostModel
from MyException import Api
from App.ProjectController import proBP
from App import auth, siwa
from App.myAuth import is_admin
from Comment.myException import MyResponse
from Models.CaseModel.caseModel import CasePart, Cases
from Models.DepartModel.userModel import User
from Models.ProjectModel.project import Project
from Models.ProjectModel.versions import Version
from Utils.myRequestParseUtil import MyRequestParseUtil
from Swagger import AddProjectSwagger, BaseResponseSwagger, PageSwagger, UpdateProjectSwagger, \
    DeleteProjectSwagger


class ProjectController(Resource):

    @auth.login_required
    @is_admin
    @siwa.doc(body=AddProjectSwagger, tags=['ProjectController'], resp=BaseResponseSwagger)
    def post(self) -> MyResponse:
        """
        添加项目
        :return: MyResponse
        """
        from Models.DepartModel.userModel import User
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="name", type=str, unique=Project, required=True)
        parse.add(name="desc", type=str, required=False)
        parse.add(name="adminID", type=int, isExist=User, required=True)
        Project(**parse.parse_args()).save()
        return MyResponse.success()

    @auth.login_required
    @siwa.doc(query=PageSwagger, tags=['ProjectController'], resp=BaseResponseSwagger)
    def get(self) -> MyResponse:
        """
        分页查询
        :return: MyResponse
        """

        parse = MyRequestParseUtil("values")
        return MyResponse.success(Project.page(**parse.page(cls=Project)))

    @auth.login_required
    @siwa.doc(body=UpdateProjectSwagger, tags=['ProjectController'], resp=BaseResponseSwagger)
    def put(self) -> MyResponse:
        """
        维护
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="id", type=int, required=True)
        parse.add(name="name", type=str, required=False)
        parse.add(name="desc", type=str, required=False)
        Project.update(**parse.parse_args())
        return MyResponse.success()

    @auth.login_required
    @is_admin
    @siwa.doc(body=DeleteProjectSwagger, tags=['ProjectController'], resp=BaseResponseSwagger)
    def delete(self) -> MyResponse:
        """
        删除
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="id", type=int, required=True)
        Project.delete_by_id(parse.parse_args().get("id"))
        return MyResponse.success()


class PageCaseController(Resource):

    @auth.login_required
    @siwa.doc(query=PageSwagger, tags=['PageCaseController'], resp=BaseResponseSwagger)
    def get(self, projectID: AnyStr) -> MyResponse:
        """
        通过MyResponse 分页查询
        :param projectID: 产品ID
        :return: MyResponse
        """
        parse = MyRequestParseUtil("values")
        return MyResponse.success(Project.get(projectID, "projectID").page_case(**parse.page(Cases)))


class QueryVersionController(Resource):

    @auth.login_required
    def get(self, projectID: AnyStr) -> MyResponse:
        """
        通过MyResponse 分页查询
        :param projectID: 产品ID
        :return: MyResponse
        """
        return MyResponse.success(Project.get(projectID, "projectID").query_version)


class PageVersionController(Resource):

    @auth.login_required
    def get(self, projectID: AnyStr) -> MyResponse:
        """
        通过projectID 分页查询
        :param projectID: 产品ID
        :return: MyResponse
        """
        parse = MyRequestParseUtil("values")
        return MyResponse.success(Project.get(projectID, "projectID").page_version(**parse.page(Version)))


class PageCasePartController(Resource):

    @auth.login_required
    def get(self, projectID: AnyStr) -> MyResponse:
        """
        通过casePart 分页查询
        :return: MyResponse
        """
        parse = MyRequestParseUtil("values")
        return MyResponse.success(Project.get(projectID, "projectID").page_casePart(**parse.page(CasePart)))


class PageUserController(Resource):
    @auth.login_required
    @is_admin
    def get(self, projectID: AnyStr) -> MyResponse:
        """
        查询user by projectID
        :return: MyResponse
        """
        parse = MyRequestParseUtil("values")
        return MyResponse.success(Project.get(projectID, "projectID").page_user(**parse.page(User)))


class QueryHostController(Resource):
    @auth.login_required
    def get(self, projectID: AnyStr) -> MyResponse:
        """
        查询host by projectID
        :return: MyResponse
        """
        return MyResponse.success(Project.get(projectID, "projectID").query_host)


class QueryEnvController(Resource):
    @auth.login_required
    def get(self, projectID: AnyStr) -> MyResponse:
        """
        查询env by projectID
        :return: MyResponse
        """
        return MyResponse.success(Project.get(projectID, "projectID").query_env)


class AddUser2ProjectController(Resource):

    @auth.login_required
    @is_admin
    def post(self) -> MyResponse:
        """
        添加用户 到项目要
        :return:MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="projectID", type=int, required=True)
        parse.add(name="userIds", type=list, required=True)
        info = parse.parse_args()
        Project.get(info['projectID'], "projectID").addUsers(info['userIds'])
        return MyResponse.success()


api_script = Api(proBP)
api_script.add_resource(ProjectController, "/opt")
api_script.add_resource(PageCaseController, "/<string:projectID>/page_cases")
api_script.add_resource(QueryVersionController, "/<string:projectID>/query_versions")
api_script.add_resource(PageVersionController, "/<string:projectID>/page_versions")
api_script.add_resource(PageCasePartController, '/<string:projectID>/page_casePart')
api_script.add_resource(PageUserController, '/<string:projectID>/page_user')
api_script.add_resource(QueryHostController, '/<string:projectID>/query_host')
api_script.add_resource(QueryEnvController, '/<string:projectID>/query_env')
api_script.add_resource(AddUser2ProjectController, "/addUser")
