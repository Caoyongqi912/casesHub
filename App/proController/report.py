# @Time : 2022/7/19 19:47 
# @Author : cyq
# @File : report.py 
# @Software: PyCharm
# @Desc:

from flask_restful import Resource, Api

from App import auth
from App.proController import proBP
from Comment import MyResponse
from Utils import MyRequestParseUtil
from Models import Report


class ReportController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        添加报告
        :return:
        """
        parse = MyRequestParseUtil()
        parse.add(name="title", type=str, unique=Report, required=True)
        parse.add(name="version", type=str, required=True)
        parse.add(name="online", type=str, required=True)
        parse.add(name="desc", type=str, required=True)
        parse.add(name="status", type=str, choices=["RELEASE", "UNRELEASE"], required=True)
        parse.add(name='demands', type=list, required=False)
        parse.add(name="bugs", type=list, required=False)
        parse.add(name="players", type=list, required=False)
        rep = parse.parse_args()
        Report(**rep).save()
        return MyResponse.success()

    @auth.login_required
    def put(self) -> MyResponse:
        """
        修改
        :return: MyResponse
        """
        parse = MyRequestParseUtil()
        parse.add(name="id", type=int, isExcist=Report, required=True)
        parse.add(name="title", type=str, required=False)
        parse.add(name="version", type=str, required=False)
        parse.add(name="online", type=str, required=False)
        parse.add(name="desc", type=str, required=False)
        parse.add(name="status", type=str, choices=["RELEASE", "UNRELEASE"], required=False)
        parse.add(name='demands', type=list, required=False)
        parse.add(name="bugs", type=list, required=False)
        parse.add(name="players", type=list, required=False)
        Report.update(**parse.parse_args())
        return MyResponse.success()

    @auth.login_required
    def get(self) -> MyResponse:
        """
        get
        :return: MyResponse
        """
        parse = MyRequestParseUtil("values")
        parse.add(name="id", type=str, required=True)
        return MyResponse.success(Report.get(parse.parse_args().get("id"), "id"))

    @auth.login_required
    def delete(self) -> MyResponse:
        """
        删除
        :return: MyResponse
        """
        parse = MyRequestParseUtil()
        parse.add(name="id", type=int, required=True)
        Report.delete_by_id(**parse.parse_args())
        return MyResponse.success()


class SendReport(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        from Utils.myMail import SendMail

        parse = MyRequestParseUtil()
        parse.add(name="id", type=int, required=True)
        report = Report.get(parse.parse_args().get("id"), "id")
        SendMail().sendReport(report)
        return MyResponse.success()


api_script = Api(proBP)
api_script.add_resource(ReportController, "/report")
