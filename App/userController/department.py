# @Time : 2022/7/11 22:08 
# @Author : cyq
# @File : department.py 
# @Software: PyCharm
# @Desc: 部门controller

from flask_restful import Resource, Api
from App import auth
from App.userController import userBP
from App.myAuth import is_admin
from Comment.myResponse import MyResponse
from Models.UserModel.users import User
from Utils.myRequestParseUtil import MyRequestParseUtil
from Models.UserModel.departments import Department


class DepartmentController(Resource):

    @auth.login_required
    def get(self):
        parse = MyRequestParseUtil("values")
        parse.add(name="page", default="1")
        parse.add(name="limit", default="20")
        pages = parse.parse_args()
        res = Department.page(**pages)
        return MyResponse.success(res)

    @auth.login_required
    @is_admin
    def post(self) -> MyResponse:
        """
        添加一个部门
        :return: MyResponse
        """
        parse = MyRequestParseUtil()
        parse.add(name="name", type=str, required=True)
        parse.add(name="desc", type=str, required=False)
        parse.add(name="adminID", type=int, required=False)
        info = parse.parse_args()
        Department.verify_unique(name=info.get("name"))
        User.get(ident=info.get("adminID"), name="adminID")
        Department(**info).save()
        return MyResponse.success()

    @auth.login_required
    def put(self) -> MyResponse:
        """
        更新部门
        :return:
        """
        parse = MyRequestParseUtil()
        parse.add(name="departID", type=int, required=True)
        parse.add(name="name", type=str, required=False)
        parse.add(name="desc", type=str, required=False)
        parse.add(name="adminID", type=int, required=False)
        info = parse.parse_args()
        Department.update(**info)
        return MyResponse.success()

    @auth.login_required
    def get(self) -> MyResponse:
        """
       分页查询部门
       :return:MyResponse
       """
        parse = MyRequestParseUtil("values")
        parse.add(name="page", default="1")
        parse.add(name="limit", default="20")
        pages = parse.parse_args()
        res = Department.page(**pages)
        return MyResponse.success(res)

    @auth.login_required
    @is_admin
    def delete(self) -> MyResponse:
        parse = MyRequestParseUtil()
        parse.add(name="departID", type=int, required=True)
        info = parse.parse_args()
        Department.get(info.get("departID"), "departID").delete()
        return MyResponse.success()


api_script = Api(userBP)
api_script.add_resource(DepartmentController, "/department")
