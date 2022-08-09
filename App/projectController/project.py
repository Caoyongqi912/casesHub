# @Time : 2022/7/14 20:05 
# @Author : cyq
# @File : project.py 
# @Software: PyCharm
# @Desc: 项目view
from typing import AnyStr

from flask_restful import Resource, Api
from App.projectController import proBP
from App import auth
from App.myAuth import is_admin
from Comment.myException import MyResponse
from Models.CaseModel.cases import CasePart
from Models.ProjectModel.project import Project
from Models.ProjectModel.versions import Version
from Utils.myRequestParseUtil import MyRequestParseUtil


class ProjectController(Resource):

    @auth.login_required
    @is_admin
    def post(self) -> MyResponse:
        """
        添加项目
        :return: MyResponse
        """
        from Models.DepartModel.userModel import User
        parse = MyRequestParseUtil()
        parse.add(name="name", type=str, unique=Project, required=True)
        parse.add(name="desc", type=str, required=False)
        parse.add(name="adminID", type=int, isExist=User, required=True)
        Project(**parse.parse_args()).save()
        return MyResponse.success()

    @auth.login_required
    def get(self) -> MyResponse:
        """
        分页查询
        :return:
        """
        parse = MyRequestParseUtil("values")
        parse.add(name="page", default="1")
        parse.add(name="limit", default="20")
        parse.add(name="by", target=Project, required=False)
        res = Project.page(**parse.parse_args())
        return MyResponse.success(res)

    @auth.login_required
    def put(self) -> MyResponse:
        """
        维护
        :return: MyResponse
        """
        parse = MyRequestParseUtil()
        parse.add(name="id", type=int, required=True)
        parse.add(name="name", type=str, required=False)
        parse.add(name="desc", type=str, required=False)
        Project.update(**parse.parse_args())
        return MyResponse.success()

    @auth.login_required
    @is_admin
    def delete(self) -> MyResponse:
        """
        删除
        :return: MyResponse
        """
        parse = MyRequestParseUtil()
        parse.add(name="id", type=int, required=True)
        Project.delete_by_id(parse.parse_args().get("id"))
        return MyResponse.success()


class QueryCaseController(Resource):

    @auth.login_required
    def get(self, projectID: AnyStr) -> MyResponse:
        """
        通过MyResponse 分页查询
        :param projectID: 产品ID
        :return: MyResponse
        """
        parse = MyRequestParseUtil("values")
        parse.add(name="page", default="1")
        parse.add(name="limit", default="20")
        parse.add(name="by", target=Project, required=False)
        return MyResponse.success(Project.get(projectID, "projectID").page_case(**parse.parse_args()))


class QueryVersionController(Resource):

    @auth.login_required
    def get(self, projectID: AnyStr) -> MyResponse:
        """
        通过MyResponse 分页查询
        :param projectID: 产品ID
        :return: MyResponse
        """
        parse = MyRequestParseUtil("values")
        parse.add(name="page", default="1")
        parse.add(name="limit", default="20")
        parse.add(name="by", target=Version, required=False)
        return MyResponse.success(Project.get(projectID, "projectID").page_version(**parse.parse_args()))


class QueryCasePartController(Resource):

    @auth.login_required
    def get(self, projectID: AnyStr) -> MyResponse:
        """
        查询casePart by projectID
        :return: MyResponse
        """
        parse = MyRequestParseUtil("values")
        parse.add(name="page", default="1")
        parse.add(name="limit", default="20")
        parse.add(name="by", target=CasePart, required=False)
        return MyResponse.success(Project.get(projectID, "projectID").page_casePart(**parse.parse_args()))


class QueryUserController(Resource):
    @auth.login_required
    def get(self, projectID: AnyStr) -> MyResponse:
        """
        查询casePart by projectID
        :return: MyResponse
        """
        from Models.DepartModel.userModel import User
        parse = MyRequestParseUtil("values")
        parse.add(name="page", default="1")
        parse.add(name="limit", default="20")
        parse.add(name="by", target=User, required=False)
        return MyResponse.success(Project.get(projectID, "projectID").page_user(**parse.parse_args()))


class AddUser(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        添加用户
        :return:MyResponse
        """
        parse = MyRequestParseUtil()
        parse.add(name="projectID", type=int, required=True)
        parse.add(name="userIds", type=list, required=True)
        info = parse.parse_args()
        Project.get(info['projectID'], "projectID").addUsers(info['userIds'])
        return MyResponse.success()


api_script = Api(proBP)
api_script.add_resource(ProjectController, "/opt")
api_script.add_resource(QueryCaseController, "/<string:projectID>/page_cases")
api_script.add_resource(QueryVersionController, "/<string:projectID>/page_versions")
api_script.add_resource(QueryCasePartController, '/<string:projectID>/page_casePart')
api_script.add_resource(QueryUserController, '/<string:projectID>/page_user')
api_script.add_resource(AddUser, "/addUser")
