# # @Time : 2022/7/16 19:45
# # @Author : cyq
# # @File : bugController.py
# # @Software: PyCharm
# # @Desc:bugView
# from flask_restful import Resource
#
# from Models.CaseModel.platformsModel import Platform
# from Models.ProjectModel.versions import Version
# from flask_restful import Api
# from App import auth, UID, auth
# from App.CaseController import caseBP
# from Comment.myException import MyResponse
# from Enums import BugLevel, BugType
# from Models.CaseModel.bugModel import Bug
# from Utils.myRequestParseUtil import MyRequestParseUtil
#
# from Models.CaseModel.caseModel import CaseModel
#
#
# class BugController(Resource):
#
#     @auth.login_required
#     def post(self) -> MyResponse:
#         """
#         添加bug
#         :return: MyResponse
#         """
#         parse: MyRequestParseUtil = MyRequestParseUtil()
#         parse.add(name="title", required=True, unique=Bug)
#         parse.add(name="desc", required=True)
#         parse.add(name="agentID", required=True, T=int)
#         parse.add(name="agentName", required=True)
#         parse.add(name="bug_type", required=True, enum=BugType)
#         parse.add(name="bug_level", required=True, enum=BugLevel)
#
#         parse.add(name="bug_tag")
#         parse.add(name="caseID", T=int, isExist=Cases)
#         parse.add(name="platformID", T=int, isExist=Platform)
#         parse.add(name="versionID", T=int, isExist=Version)
#         parse.add(name="files", T=list)
#
#         Bug(**parse.parse_args).save()
#         return MyResponse.success()
#
#     @auth.login_required
#     def get(self) -> MyResponse:
#         """
#         uid获取
#         :return: MyResponse
#         """
#         parse: MyRequestParseUtil = MyRequestParseUtil("values")
#         parse.add(name=UID, required=True)
#         return MyResponse.success(Bug.get_by_uid(**parse.parse_args))
#
#     @auth.login_required
#     def put(self) -> MyResponse:
#         """
#         维护
#         :return: MyResponse
#         """
#         parse: MyRequestParseUtil = MyRequestParseUtil()
#         parse.add(name=UID, required=True)
#         parse.add(name="title")
#         parse.add(name="desc")
#         parse.add(name="agentID", T=int)
#         parse.add(name="agentName")
#         parse.add(name="bug_type", enum=BugType)
#         parse.add(name="bug_level", enum=BugLevel)
#         parse.add(name="bug_tag")
#         parse.add(name="mark")
#         parse.add(name="caseID", T=int, isExist=CaseModel)
#         parse.add(name="platformID", T=int, isExist=Platform)
#         parse.add(name="versionID", T=int, isExist=Version)
#         parse.add(name="files", T=list)
#         Bug.update(**parse.parse_args)
#         return MyResponse.success()
#
#     @auth.login_required
#     def delete(self) -> MyResponse:
#         """
#         Bug 校验是否是创建人以及管理 、
#         级联附件删除
#         :return: MyResponse
#         """
#         parse: MyRequestParseUtil = MyRequestParseUtil()
#         parse.add(name=UID, required=True)
#         Bug.delete_by_id(**parse.parse_args)
#         return MyResponse.success()
#
#
# class QueryBugController(Resource):
#
#     @auth.login_required
#     def get(self) -> MyResponse:
#         parse: MyRequestParseUtil = MyRequestParseUtil("values")
#         return MyResponse.success(Bug.page(**parse.page(Bug)))
#
#
# api_script = Api(caseBP)
# api_script.add_resource(BugController, "/bug/opt")
# api_script.add_resource(QueryBugController, "/bug/query")
