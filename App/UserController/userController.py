# @Time : 2022/7/6 22:24 
# @Author : cyq
# @File : userController.py
# @Software: PyCharm
# @Desc: 注册controller
from flask import g
from flask_restful import Resource, Api
from App import auth, UID
from App.UserController import userBP
from Comment.myException import MyResponse
from Models.UserModel.departModel import Department, UserTag
from Models.UserModel.userModel import User
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
        parse.add(name="username", T=str, unique=User, required=True)
        parse.add(name="password", T=str, required=True)
        parse.add(name="phone", T=str, unique=User, required=True)
        User(**parse.parse_args).addAdmin()
        return MyResponse.success()


class UserOptController(Resource):

    @auth.login_required
    @is_admin
    def get(self) -> MyResponse:
        """
        通UID 获取info
        :return:
        """
        parse = MyRequestParseUtil("values")
        parse.add(name=UID, required=True)
        info = User.get_by_uid(**parse.parse_args)
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
        parse.add(name="username", unique=User, required=True)
        parse.add(name="phone", unique=User, required=True)
        parse.add(name="gender", enum=Gender, required=True)
        parse.add(name="tagName", required=False)
        parse.add(name="departmentID", T=int, isExist=Department, required=False)
        User(**parse.parse_args).addUser()
        return MyResponse.success()

    @auth.login_required
    @is_admin
    def put(self) -> MyResponse:
        """
        管理員维护用戶
        :return: jsonify
        """

        from Enums.myEnum import Gender, UserTag
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name=UID, required=True)
        parse.add(name="username", required=False)
        parse.add(name="phone", required=False)
        parse.add(name="gender", enum=Gender, required=False)
        parse.add(name="tagName", required=False)
        parse.add(name="departmentID", T=int, required=False)
        User.update(**parse.parse_args)
        return MyResponse.success()

    @auth.login_required
    @is_admin
    def delete(self) -> MyResponse:
        """
        删除
        :return:
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name=UID, required=True)
        User.delete_by_id(**parse.parse_args)
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
        return MyResponse.success(User.page(**parse.page(cls=User)))


class LoginController(Resource):

    def post(self) -> MyResponse:
        """
        登录
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="username", T=str, required=True)
        parse.add(name="password", T=str, required=True)
        return MyResponse.success(User.login(**parse.parse_args))


# class UserController(Resource):
#
#     @auth.login_required
#     def get(self) -> MyResponse:
#         """
#         :return: MyResponse
#         """
#         parse: MyRequestParseUtil = MyRequestParseUtil("values")
#         parse.add(name=UID, required=True)
#         user: User = User.get_by_uid(**parse.parse_args)
#         userProject = user.project
#         cases = Cases.query_by_field(creator=user.id)
#
#         return MyResponse.success(
#             {
#                 "user": user,
#                 "project": userProject,
#                 "case": cases
#             }
#         )


class SetPasswordController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        用户修改密码
        :return: MyResponse
        """
        user: User = g.user
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="old_password", T=str, required=True)
        parse.add(name="new_password", T=str, required=True)
        user.set_password(**parse.parse_args)
        return MyResponse.success()


class CurrentUserController(Resource):
    @auth.login_required
    def get(self) -> MyResponse:
        """
        CurrentUserInfo
        :return: MyResponse
        """
        from flask import g
        return MyResponse.success(User.get_by_uid(g.user.uid))


class MoHuSearch(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        用户模糊查询
        :return:MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="target")
        parse.add(name="value")
        if parse.parse_args.get("value"):
            info = User.search_like(**parse.parse_args)
            return MyResponse.success(info)
        return MyResponse.success()


class UserTagController(Resource):

    @auth.login_required
    @is_admin
    def post(self) -> MyResponse:
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="name", unique=UserTag, required=True)
        UserTag(**parse.parse_args).save()
        return MyResponse.success()

    @auth.login_required
    @is_admin
    def get(self) -> MyResponse:
        return MyResponse.success(UserTag.all())

    @auth.login_required
    @is_admin
    def put(self):
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="name", required=False)
        UserTag.update(**parse.parse_args)
        return MyResponse.success()

    @auth.login_required
    @is_admin
    def delete(self):
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name=UID, required=True)
        UserTag.delete_by_id(**parse.parse_args)
        return MyResponse.success()


api_script = Api(userBP)
api_script.add_resource(MoHuSearch, "/search")
api_script.add_resource(AddAdminController, "/admin")
api_script.add_resource(UserTagController, "/tag/opt")
# api_script.add_resource(UserController, "/detail")
api_script.add_resource(UserOptController, "/opt")
api_script.add_resource(SetPasswordController, "/setpassword")
api_script.add_resource(CurrentUserController, '/current')
api_script.add_resource(PageUserController, "/query")
api_script.add_resource(GetTokenController, "/getToken")
api_script.add_resource(LoginController, "/login")
