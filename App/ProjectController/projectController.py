# @Time : 2022/7/14 20:05 
# @Author : cyq
# @File : projectController.py
# @Software: PyCharm
# @Desc: 项目view
from typing import AnyStr

from flask_restful import Resource

from MyException import Api
from App.ProjectController import proBP
from App import auth, siwa, UID
from App.myAuth import is_admin
from Comment.myException import MyResponse
from Models.ProjectModel.projectModel import Project
from Utils.myRequestParseUtil import MyRequestParseUtil
from Swagger import AddProjectSwagger, BaseResponseSwagger, PageSwagger, UpdateProjectSwagger, \
    DeleteProjectSwagger
from Utils import MyLog

log = MyLog.get_log(__file__)


class ProjectController(Resource):

    @auth.login_required
    @is_admin
    def post(self) -> MyResponse:
        """
        添加项目
        :return: MyResponse
        """
        from Models.UserModel.userModel import User
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="name", type=str, unique=Project, required=True)
        parse.add(name="desc", type=str, required=False)
        parse.add(name="adminID", type=int, required=True)
        par = parse.parse_args
        user = User.get(par.get("adminID"))
        par['adminName'] = user.username
        Project(**par).save()
        return MyResponse.success()

    @auth.login_required
    def get(self) -> MyResponse:
        """
        分页查询
        :return: MyResponse
        """

        parse = MyRequestParseUtil("values")
        return MyResponse.success(Project.page(**parse.page(cls=Project)))

    @auth.login_required
    def put(self) -> MyResponse:
        """
        维护
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name=UID, required=True)
        parse.add(name="name", required=False)
        parse.add(name="desc", required=False)
        Project.update(**parse.parse_args)
        return MyResponse.success()

    @auth.login_required
    @is_admin
    def delete(self) -> MyResponse:
        """
        删除
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name=UID, required=True)
        Project.delete_by_id(**parse.parse_args)
        return MyResponse.success()


class QueryHostController(Resource):
    @auth.login_required
    def get(self, projectID: AnyStr) -> MyResponse:
        """
        查询host by projectID
        :return: MyResponse
        """
        return MyResponse.success(Project.get(projectID, "projectID").query_host)


class QueryVariableIDController(Resource):
    @auth.login_required
    def get(self, projectID: AnyStr) -> MyResponse:
        """
        查询env by projectID
        :return: MyResponse
        """
        return MyResponse.success(Project.get(projectID, "projectID").query_variables)


class AddUser2ProjectController(Resource):

    @auth.login_required
    @is_admin
    def post(self) -> MyResponse:
        """
        添加用户 到项目
        :return:MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name=UID, required=True)
        parse.add(name="userIds", type=list, required=True)
        info = parse.parse_args
        Project.get_by_uid(info.get(UID)).addUsers(info['userIds'])
        return MyResponse.success()


class SearchProjectController(Resource):

    @auth.login_required
    def get(self) -> MyResponse:
        """
        搜索项目
        :return:
        """
        parse: MyRequestParseUtil = MyRequestParseUtil("values")
        return MyResponse.success(Project.search_by_chemy(**parse.parse_args))


class ProjectInfoController(Resource):

    @auth.login_required
    def get(self) -> MyResponse:
        """
        获取单个项目信息
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil("values")
        parse.add(name=UID, required=True)
        project = Project.get_by_uid(**parse.parse_args)
        return MyResponse.success(project)


class QueryProjectUsers(Resource):

    @auth.login_required
    def get(self) -> MyResponse:
        parse: MyRequestParseUtil = MyRequestParseUtil("values")
        parse.add(name=UID, required=True)
        project = Project.get_by_uid(**parse.parse_args)
        return MyResponse.success(project.query_users)


class QueryProjects(Resource):

    @auth.login_required
    def get(self) -> MyResponse:
        return MyResponse.success(Project.all())


api_script = Api(proBP)
api_script.add_resource(ProjectController, "/opt")
api_script.add_resource(QueryProjects, "/queryProjects")
api_script.add_resource(ProjectInfoController, "/info")
api_script.add_resource(QueryHostController, '/<string:projectID>/query_host')
api_script.add_resource(QueryProjectUsers, '/users')
api_script.add_resource(QueryVariableIDController, '/<string:projectID>/query_variable')
api_script.add_resource(AddUser2ProjectController, "/addUser")
api_script.add_resource(SearchProjectController, "/search")
