# @Time : 2022/7/6 22:24 
# @Author : cyq
# @File : user.py
# @Software: PyCharm
# @Desc: 注册controller
from typing import AnyStr
from flask import g, request, Response
from flask_restful import Resource, Api
from App import auth
from App.DepartController import userBP
from Comment.myException import MyResponse
from Models.DepartModel.departModel import Department
from Models.DepartModel.userModel import User
from Utils import getAvatarPath
from Utils.myRequestParseUtil import MyRequestParseUtil
from App.myAuth import is_admin


class AddAdminController(Resource):

    def post(self) -> MyResponse:
        """
        添加管理员
        :return: MyResponse
        :raise: ParamException
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="username", type=str, unique=User, required=True)
        parse.add(name="password", type=str, required=True)
        parse.add(name="phone", type=str, unique=User, required=True)
        User(**parse.parse_args()).addAdmin()
        return MyResponse.success()


class UserOptController(Resource):

    @auth.login_required
    @is_admin
    def get(self) -> MyResponse:
        """
        通userID 获取info
        :return:
        """
        parse = MyRequestParseUtil("values")
        parse.add(name="userID", required=True)
        info = User.get(parse.parse_args().get("userID"), "userID")
        return MyResponse.success(info)

    @auth.login_required
    @is_admin
    def post(self) -> MyResponse:
        """
        管理員添加用戶
        :return: jsonify
        """

        from Enums.myEnum import Gender, UserTag
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="username", type=str, unique=User, required=True)
        parse.add(name="phone", type=str, unique=User, required=True)
        parse.add(name="gender", type=int, enum=Gender, required=True)
        parse.add(name="tag", type=int, enum=UserTag, required=True)
        parse.add(name="departmentID", type=int, isExist=Department, required=True)
        User(**parse.parse_args()).addUser()
        return MyResponse.success()

    @auth.login_required
    @is_admin
    def delete(self) -> MyResponse:
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="id", type=str, required=True)
        User.delete_by_id(**parse.parse_args())
        return MyResponse.success()


class GetTokenController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        get token
        """
        t = {"token": g.user.generate_token().decode("utf-8")}
        return MyResponse.success(t)


class PageUserController(Resource):

    @auth.login_required
    @is_admin
    def get(self) -> MyResponse:
        """
        分页查询用户
        :return:MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil("values")
        return MyResponse.success(User.page(**parse.page(User)))


class LoginController(Resource):

    def post(self) -> MyResponse:
        """
        登录
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
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
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="userID", type=int, required=True)
        return MyResponse.success(User.get(parse.parse_args().get("userID")))

    @auth.login_required
    def put(self) -> MyResponse:
        """
        修改密码
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="password", type=str, required=True)
        u = User.get(g.user.id, "")
        u.hash_password(parse.parse_args().get("password"))
        return MyResponse.success()


class AvatarController(Resource):

    @auth.login_required
    async def post(self) -> MyResponse:
        """
        上传头像
        :return:
        """
        from werkzeug.datastructures import FileStorage
        file: FileStorage = request.files.get("file")
        await User.save_or_update_avatar(file)
        return MyResponse.success()


class GetAvatarController(Resource):
    @auth.login_required
    def get(self, filename: AnyStr) -> Response:
        """
        返回头像
        :param filename: 头像名
        :return: Response
        """
        path: AnyStr = getAvatarPath(filename)
        with open(path, "rb") as f:
            avatar: AnyStr = f.read()
        return Response(avatar, mimetype="image/jpeg")


class SetPasswordController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        用户修改密码
        :return: MyResponse
        """
        user: User = g.user
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="password", type=str, required=True)
        user.hash_password(**parse.parse_args()).save()
        return MyResponse.success()


class CurrentUserController(Resource):
    @auth.login_required
    def get(self) -> MyResponse:
        """
        CurrentUserInfo
        :return: MyResponse
        """
        from flask import g
        return MyResponse.success(User.get(g.user.id))


class MoHuSearch(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        模糊查询
        :return:MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="target", type=str, required=True)
        parse.add(name="value", type=str, required=True)
        info = User.search_like(**parse.parse_args())
        return MyResponse.success(info)


api_script = Api(userBP)
api_script.add_resource(MoHuSearch, "/search")
api_script.add_resource(AddAdminController, "/admin")
api_script.add_resource(UserOptController, "/opt")
api_script.add_resource(SetPasswordController, "/setpassword")
api_script.add_resource(CurrentUserController, '/current')
api_script.add_resource(PageUserController, "/page")
api_script.add_resource(GetTokenController, "/getToken")
api_script.add_resource(LoginController, "/login")
api_script.add_resource(AvatarController, "/avatar")
api_script.add_resource(GetAvatarController, "/avatar/<string:filename>")
