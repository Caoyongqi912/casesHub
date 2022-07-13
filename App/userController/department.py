# @Time : 2022/7/11 22:08 
# @Author : cyq
# @File : department.py 
# @Software: PyCharm
# @Desc: 部门controller
from flask_restful import Resource, Api
from App import auth
from App.userController import userBP
from App.auth import is_admin


class DepartmentController(Resource):

    @auth.login_required
    @is_admin
    def post(self):
        pass


api_script = Api(userBP)
api_script.add_resource(DepartmentController, "/department/new")
