# @Time : 2022/7/6 22:24 
# @Author : cyq
# @File : user.py
# @Software: PyCharm
# @Desc: 注册controller
from flask import jsonify, g
from flask_restful import Resource, Api, reqparse

from App import auth
from App.userController import userBP
from Comment.myResponse import MyResponse
from Utils.myRequestParseUtil import MyRequestParseUtil
from Models.UserModel.users import User
from Utils.myLog import MyLog
from App.auth import is_admin

log = MyLog.get_log(__file__)


class AddUser(Resource):

    @auth.login_required
    @is_admin
    def post(self) -> jsonify:
        """
        管理員添加用戶
        :return: jsonify
        """
        parse = MyRequestParseUtil()
        parse.add(name="username", type=str, required=True)
        parse.add(name="phone", type=str, required=True)
        parse.add(name="password", type=str, required=True)
        parse.add(name="gender", type=str, choices=["MALE", "FEMALE"], required=True)
        parse.add(name="tag", type=str, required=True)
        body = parse.parse_args()
        User.verify_unique(username=body.get("username"))
        User.verify_unique(phone=body.get("phone"))
        User(**body).save()
        return MyResponse.success()


class GetTokenController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        get token
        """
        t = {"token": g.user.generate_token().decode("utf-8")}
        return MyResponse.success(t)


class QueryUserController(Resource):

    @auth.login_required
    @is_admin
    def get(self) -> MyResponse:
        """
        分页查询用户
        :return:MyResponse
        """
        parse = MyRequestParseUtil("values")
        parse.add(name="page", default="1")
        parse.add(name="limit", default="20")
        pages = parse.parse_args()
        res = User.page(**pages)
        return MyResponse.success(res)


class LoginController(Resource):

    def post(self) -> MyResponse:
        """
        登录
        :return: MyResponse
        """
        parse = MyRequestParseUtil()
        parse.add(name="username", type=str, required=True)
        parse.add(name="password", type=str, required=True)
        info = parse.parse_args()
        return MyResponse.success(User.login(**info))


class UserController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        通过userID 查询单个用户Info、
        :return: MyResponse
        """
        parse = MyRequestParseUtil()
        parse.add(name="userID", type=int, required=True)
        return MyResponse.success(User.get(parse.parse_args().get("userID")))


api_script = Api(userBP)
api_script.add_resource(AddUser, "/addUser")
api_script.add_resource(QueryUserController, "/query/user/page")
api_script.add_resource(GetTokenController, "/getToken")
api_script.add_resource(LoginController, "/login")
api_script.add_resource(UserController, "/info")
