# @Time : 2022/7/16 18:02 
# @Author : cyq
# @File : platformController.py
# @Software: PyCharm
# @Desc:
from flask_restful import Resource

from Models.ProjectModel.projectModel import Project
from MyException import Api
from App import auth, UID, tokenAuth
from Comment.myException import MyResponse
from App.CaseController import caseBP
from Models.CaseModel.caseModel import Cases
from Models.CaseModel.platformsModel import Platform
from Utils.myRequestParseUtil import MyRequestParseUtil


class PlatformController(Resource):

    @tokenAuth.login_required
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

    @tokenAuth.login_required
    def get(self) -> MyResponse:
        """
        get
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil("values")
        parse.add(name=UID, required=True)
        return MyResponse.success(Platform.get_by_uid(**parse.parse_args()))

    @tokenAuth.login_required
    def delete(self) -> MyResponse:
        """
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name=UID, required=True)
        Platform.delete_by_id(**parse.parse_args())
        return MyResponse.success()

    @tokenAuth.login_required
    def put(self) -> MyResponse:
        """
        :return: MyResponse
        """
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name=UID, required=True)
        parse.add(name="name", required=False)
        Platform.update(**parse.parse_args())
        return MyResponse.success()


cl

api_script = Api(caseBP)
api_script.add_resource(PlatformController, "/platform/opt")
