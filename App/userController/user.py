# @Time : 2022/7/6 22:24 
# @Author : cyq
# @File : user.py
# @Software: PyCharm
# @Desc: 注册controller
from typing import AnyStr

from flask import jsonify, g, request, Response
from flask_restful import Resource, Api

from App import auth
from App.userController import userBP
from Comment.myResponse import MyResponse
from Utils.myAvatarPath import getAvatarPath
from Utils.myRequestParseUtil import MyRequestParseUtil
from Models.UserModel.users import User
from Utils.myLog import MyLog
from App.myAuth import is_admin

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
        parse.add(name="username", type=str, unique=User, required=True)
        parse.add(name="phone", type=str, unique=User, required=True)
        parse.add(name="password", type=str, required=True)
        parse.add(name="gender", type=str, choices=["MALE", "FEMALE"], required=True)
        parse.add(name="tag", type=str, required=True)
        User(**parse.parse_args()).save()
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
        res = User.page(**parse.parse_args())
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
        return MyResponse.success(User.login(**parse.parse_args()))


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

    @auth.login_required
    def put(self) -> MyResponse:
        """
        修改密码
        :return: MyResponse
        """
        parse = MyRequestParseUtil()
        parse.add(name="password", type=str, required=True)
        u = User.get(g.user.id, "")
        u.hash_password(parse.parse_args().get("password"))
        return MyResponse.success()


class AvatarController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        上传头像
        :return:
        """
        from werkzeug.utils import secure_filename
        from faker import Faker
        f = Faker()
        file = request.files.get("file")
        user = g.user

        fileName = f.pystr() + '_' + secure_filename(file.filename)  # 头像名称
        filePath = getAvatarPath(fileName)  # 头像路径
        file.save(filePath)  # 存储头像

        user.avatar = fileName
        user.save()  # 入库
        return MyResponse.success()


class GetAvatarController(Resource):
    def get(self, filename: AnyStr):
        """
        返回头像
        :param filename: 头像名
        :return:
        """
        path = getAvatarPath(filename)
        with open(path, "rb") as f:
            avatar = f.read()
        return Response(avatar, mimetype="image/jpeg")


class SetUserInfo(Resource):

    def post(self):
        pass

api_script = Api(userBP)
api_script.add_resource(AddUser, "/")
api_script.add_resource(QueryUserController, "/page")
api_script.add_resource(GetTokenController, "/getToken")
api_script.add_resource(LoginController, "/login")
api_script.add_resource(UserController, "/info")
api_script.add_resource(SetUserInfo, "/info")

api_script.add_resource(AvatarController, "/avatar")
api_script.add_resource(GetAvatarController, "/avatar/<string:filename>")
