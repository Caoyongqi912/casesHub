# @Time : 2022/7/16 19:45 
# @Author : cyq
# @File : bugController.py
# @Software: PyCharm
# @Desc:bugView
from flask_restful import Resource
from MyException import Api
from App import auth
from App.CaseController import caseBP
from Comment.myException import MyResponse
from Enums import BugLevel, BugStatus
from Models.CaseModel.bugModel import Bug
from Utils.myRequestParseUtil import MyRequestParseUtil


class BugController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        添加bug
        :return: MyResponse
        """
        from Models.CaseModel.caseModel import Cases
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="title", required=True, unique=Bug)
        parse.add(name="desc", required=True)
        parse.add(name="tag")
        parse.add(name="agentID", required=True, type=int)

        parse.add(name="level", required=True, enum=BugLevel)
        parse.add(name="status", enum=BugStatus)
        parse.add(name="caseID", type=int, isExist=Cases)

        Bug(**parse.parse_args()).save()
        return MyResponse.success()


class FindBug(Resource):
    @auth.login_required
    def get(self, UID) -> MyResponse:
        """
        获取case下的所有bug
        :return: MyResponse
        """
        bug = Bug.get_by_uid(UID)
        return MyResponse.success(bug)


#
api_script = Api(caseBP)
api_script.add_resource(BugController, "/bug")
api_script.add_resource(FindBug, "/bug/<string:bugID>")
