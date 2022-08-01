# @Time : 2022/7/14 20:05 
# @Author : cyq
# @File : project.py 
# @Software: PyCharm
# @Desc: 项目view

from flask_restful import Resource, Api
from App.proController import proBP
from App import auth
from App.myAuth import is_admin
from Comment.myResponse import MyResponse
from Utils.myRequestParseUtil import MyRequestParseUtil
from Models.ProjectModel import Project


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


class QueryProductController(Resource):
    @auth.login_required
    def get(self, projectID: Project.id) -> MyResponse:
        """
        查询产品列表 分页
        :param projectID: Project.id
        :return:
        """
        from Models.ProjectModel import Product
        parse = MyRequestParseUtil("values")
        parse.add(name="page", default="1")
        parse.add(name="limit", default="20")
        parse.add(name="by", target=Product, required=False)
        info = parse.parse_args()
        info = Project.get(projectID, "projectID").page_product(**info)
        return MyResponse.success(info)


api_script = Api(proBP)
api_script.add_resource(ProjectController, "/project/opt")
api_script.add_resource(QueryProductController, "/project/<string:projectID>/page_product")
