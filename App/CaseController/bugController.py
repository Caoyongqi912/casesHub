# @Time : 2022/7/16 19:45 
# @Author : cyq
# @File : bugController.py
# @Software: PyCharm
# @Desc:bugView
from flask_restful import Resource
from flask_restful import Api
from App import auth
from App.CaseController import caseBP
from Comment.myException import MyResponse
from Enums import BugLevel, BugStatus
from Models.CaseModel.bugs import Bug
from Utils.myRequestParseUtil import MyRequestParseUtil


class BugController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        添加bug
        :return: MyResponse
        """
        from Models.CaseModel.cases import Cases
        parse: MyRequestParseUtil = MyRequestParseUtil()
        parse.add(name="caseID", type=int, required=True, isExist=Cases)
        parse.add(name="title", type=str, required=True, unique=Bug)
        parse.add(name="desc", type=str, required=True)
        parse.add(name="tester", type=str, required=True)
        parse.add(name="developer", type=str, required=True)
        parse.add(name="pr", type=str, required=True)
        parse.add(name="level", type=str, required=True, enum=BugLevel)
        parse.add(name="status", type=str, required=True, enum=BugStatus)
        Bug(**parse.parse_args()).save()
        return MyResponse.success()


class FindBug(Resource):
    @auth.login_required
    def get(self, bugID) -> MyResponse:
        """
        获取case下的所有bug
        :return: MyResponse
        """
        bug = Bug.get(bugID, "bugID")
        return MyResponse.success(bug)


#
api_script = Api(caseBP)
api_script.add_resource(BugController, "/bug")
api_script.add_resource(FindBug, "/bug/<string:bugID>")
