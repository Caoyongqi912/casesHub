# @Time : 2022/7/16 18:02 
# @Author : cyq
# @File : platform.py 
# @Software: PyCharm
# @Desc:
from flask_restful import Resource, Api
from App import auth
from Comment.myException import MyResponse
from App.PlatformController import platformBP
from Models.CaseModel.cases import Cases
from Models.CaseModel.platforms import Platform
from Utils.myRequestParseUtil import MyRequestParseUtil


class PlatformController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        添加平台
        :return:MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="name", required=True, unique=Platform,
                  type=str)
        Platform(**parse.parse_args()).save()
        return MyResponse.success()

    @auth.login_required
    def get(self) -> MyResponse:
        """
        get
        :return: MyResponse
        """
        return MyResponse.success(Platform.all())

    @auth.login_required
    def delete(self) -> MyResponse:
        """
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="id", required=True, type=int)
        Platform.delete_by_id(**parse.parse_args())
        return MyResponse.success()

    @auth.login_required
    def put(self) -> MyResponse:
        """
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name='id', required=True, type=int)
        parse.add(name="name", required=False, type=str)
        Platform.update(**parse.parse_args())
        return MyResponse.success()


class PageCases(Resource):

    @auth.login_required
    def get(self, platformID: Platform) -> MyResponse:
        """
        查询用例分页
        :param platformID:
        :return: MyResponse
        """
        parse = MyRequestParseUtil("values")
        parse.add(name="page", default="1")
        parse.add(name="limit", default="20")
        parse.add(name="by", target=Cases, required=False)
        return MyResponse.success(Platform.get(platformID, "platformID").page_case(**parse.parse_args()))


api_script = Api(platformBP)
api_script.add_resource(PlatformController, "/opt")
api_script.add_resource(PageCases, "/<string:platformID>/page_case")
