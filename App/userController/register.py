# @Time : 2022/7/6 22:24 
# @Author : cyq
# @File : register.py
# @Software: PyCharm
# @Desc: 注册
from flask import jsonify, g
from flask_restful import Resource, Api

from App import auth
from App.userController import userBP
from Comment.myResponse import MyResponse
from Utils.requestParseUtil import MyRequestParseUtil
from Models.UserModel.users import User
from Utils.log import MyLog
from App.auth import is_admin

log = MyLog.get_log(__file__)


class RegisterController(Resource):

    def post(self) -> jsonify:
        """
        注册
        :return: jsonify
        """
        parse = MyRequestParseUtil()
        parse.add(name="username", type=str, required=True)
        parse.add(name="phone", type=str, required=True)
        parse.add(name="password", type=str, required=True)
        parse.add(name="email", type=str, required=True)
        parse.add(name="gender", type=str, choices=["MALE", "FEMALE"], required=False)
        parse.add(name="isAdmin", type=bool, required=False)
        parse.add(name="departmentID", type=int, required=True)
        body = parse.parse_args()
        User(**body).save()
        return MyResponse.success()


class GetTokenController(Resource):

    @auth.login_required
    def post(self) -> jsonify:
        """
        get token
        """
        t = {"token": g.user.generate_token().decode("utf-8")}
        return MyResponse.success(t)

    def get(self):
        User.verify_unique(username="cyq")
        return "ok"

api_script = Api(userBP)
api_script.add_resource(RegisterController, "/register")
api_script.add_resource(GetTokenController, "/getToken")
