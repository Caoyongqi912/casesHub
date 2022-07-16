# @Time : 2022/7/16 19:45 
# @Author : cyq
# @File : bug.py 
# @Software: PyCharm
# @Desc:
from flask_restful import Resource, Api

from App.caseController import caseBP
from Comment.myResponse import MyResponse
from Models.CaseModel.bugs import Bug


class BugController(Resource):

    def post(self) -> MyResponse:
        pass


api_script = Api(caseBP)
api_script.add_resource(BugController, "/bug")
