# @Time : 2022/7/16 18:02 
# @Author : cyq
# @File : platform.py 
# @Software: PyCharm
# @Desc:
from flask_restful import Resource, Api

from App import auth
from Comment import MyResponse
from App.platformController import platformBP
from Utils import MyRequestParseUtil
from Models import Platform


class PlatformController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        添加平台
        :return:MyResponse
        """
        parse = MyRequestParseUtil()
        parse.add(name="name", required=True, type=str)
        Platform(**parse.parse_args()).save()
        return MyResponse.success()

    @auth.login_required
    def get(self) -> MyResponse:
        """
        get
        :return: MyResponse
        """
        return MyResponse.success(Platform.all())


api_script = Api(platformBP)
api_script.add_resource(PlatformController, "/opt")
