# @Time : 2022/7/11 22:08 
# @Author : cyq
# @File : departmentController.py
# @Software: PyCharm
# @Desc: 部门controller

from flask_restful import Resource,Api
from App import auth, UID
from App.UserController import userBP
from App.myAuth import is_admin
from Comment.myException import MyResponse
from Utils.myRequestParseUtil import MyRequestParseUtil
from Models.UserModel.departModel import Department, UserTag
from Utils.myLog import MyLog

log = MyLog.get_log(__file__)


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
        parse.add(name="adminID", type=int, required=False)
        parse.add(name="tags", type=list, required=False)
        info = parse.parse_args
        department = Department(**info)
        department.save()

        if info.get("adminID"):
            user = User.get(info.get("adminID"))
            user.departmentID = department.id
            user.save()
        return MyResponse.success()

    @auth.login_required
    def put(self) -> MyResponse:
        """
        更新部门
        :return:MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name=UID, required=True)
        parse.add(name="name", required=False)
        parse.add(name="desc", required=False)
        parse.add(name="adminID", type=int, required=False)
        Department.update(**parse.parse_args)
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
        Department.delete_by_id(**parse.parse_args)
        return MyResponse.success()


class PageDepartmentController(Resource):

    @auth.login_required
    def get(self) -> MyResponse:
        parse = MyRequestParseUtil("values")
        departPage = Department.page(**parse.page(Department))

        return MyResponse.success(departPage)


class QueryDepartmentTagController(Resource):

    @auth.login_required
    @is_admin
    def get(self) -> MyResponse:
        """
        获取部门下标签
        :return: MyResponse
        """
        parse = MyRequestParseUtil("values")
        parse.add(name="id", required=True)
        log.info(parse.parse_args)
        depart: Department = Department.get(**parse.parse_args)
        return MyResponse.success(depart.query_tags)


api_script = Api(userBP)
api_script.add_resource(DepartmentController, "/department/opt")
api_script.add_resource(QueryDepartmentTagController, "/department/tags")
api_script.add_resource(PageDepartmentController, "/department/page")
