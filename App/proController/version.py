# @Time : 2022/7/16 18:09 
# @Author : cyq
# @File : version.py 
# @Software: PyCharm
# @Desc: version view
from flask_restful import Resource, Api
from App.proController import proBP
from Comment.myResponse import MyResponse
from Utils.myRequestParseUtil import MyRequestParseUtil
from Models.ProjectModel.versions import Version
from Models.ProjectModel.pro import Product


class VersionController(Resource):

    def post(self) -> MyResponse:
        parse = MyRequestParseUtil()
        parse.add(name='name', required=True, unique=Version, type=str)
        parse.add(name="desc", required=False, type=str)
        parse.add(name="productID", required=True, type=int, isExist=Product)
        Version(**parse.parse_args()).save()
        return MyResponse.success()

    def get(self):
        pass

    def delete(self):
        pass

    def put(self):
        pass


api_script = Api(proBP)
api_script.add_resource(VersionController, "/version")
