# @Time : 2022/7/11 22:08 
# @Author : cyq
# @File : departmentController.py
# @Software: PyCharm
# @Desc: 部门controller

from flask_restful import Resource
from MyException import Api
from App import auth, UID
from App.UserController import userBP
from App.myAuth import is_admin
from Comment.myException import MyResponse
from Utils.myRequestParseUtil import MyRequestParseUtil
from Models.UserModel.departModel import Department, UserTag


class DepartmentController(Resource):

    @auth.login_required
    @is_admin
    def post(self) -> MyResponse:
        """
        添加一个部门
        :return: MyResponse
        """
        from Models.UserModel.userModel import User
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="name", unique=Department, required=True)
        parse.add(name="desc", required=False)
        parse.add(name="adminID", type=int, isExist=User, required=False)
        parse.add(name="tags", type=list, required=False)
        info = parse.parse_args()
        Department(**info).save()
        return MyResponse.success()

    @auth.login_required
    def put(self) -> MyResponse:
        """
        更新部门
        :return:MyResponse
        """
        from Models.UserModel.userModel import User
        parse: MyRequestParseUtil = MyRequestParseUtil()
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
        return MyResponse.success(Department.all())

    @auth.login_required
    @is_admin
    def delete(self) -> MyResponse:
        """
        根据departID删除数据
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name=UID, required=True)
        Department.delete_by_id(**parse.parse_args())
        return MyResponse.success()


class QueryDepartmentController(Resource):

    @auth.login_required
    def get(self) -> MyResponse:
        parse = MyRequestParseUtil("values")
        return MyResponse.success(Department.page(**parse.page(Department)))


api_script = Api(userBP)
api_script.add_resource(DepartmentController, "/department/opt")
api_script.add_resource(QueryDepartmentController, "/department/query")
