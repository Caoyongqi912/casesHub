# @Time : 2022/7/11 22:08 
# @Author : cyq
# @File : department.py 
# @Software: PyCharm
# @Desc: 部门controller

from flask_restful import Resource, Api
from App import auth
from App.DepartController import userBP
from App.myAuth import is_admin
from Comment.myResponse import MyResponse
from Utils.myRequestParseUtil import MyRequestParseUtil
from Models.DepartModel.departModel import Department


class DepartmentController(Resource):

    @auth.login_required
    @is_admin
    def post(self) -> MyResponse:
        """
        添加一个部门
        :return: MyResponse
        """
        from Models.DepartModel.userModel import User
        parse = MyRequestParseUtil()
        parse.add(name="name", type=str, unique=Department, required=True)
        parse.add(name="desc", type=str, required=False)
        parse.add(name="adminID", type=int, isExist=User, required=False)
        Department(**parse.parse_args()).save()
        return MyResponse.success()

    @auth.login_required
    def put(self) -> MyResponse:
        """
        更新部门
        :return:MyResponse
        """
        from Models.DepartModel.userModel import User
        parse = MyRequestParseUtil()
        parse.add(name="id", type=int, required=True)
        parse.add(name="name", type=str, required=False)
        parse.add(name="desc", type=str, required=False)
        parse.add(name="adminID", type=int, isExist=User, required=False)
        Department.update(**parse.parse_args())
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
        res = Department.page(**parse.parse_args())
        return MyResponse.success(res)

    @auth.login_required
    @is_admin
    def delete(self) -> MyResponse:
        """
        根据departID删除数据
        :return: MyResponse
        """
        parse = MyRequestParseUtil()
        parse.add(name="id", type=int, required=True)
        Department.delete_by_id(parse.parse_args().get("id"))
        return MyResponse.success()


api_script = Api(userBP)
api_script.add_resource(DepartmentController, "/department")
