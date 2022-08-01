# @Time : 2022/7/16 18:09 
# @Author : cyq
# @File : version.py 
# @Software: PyCharm
# @Desc: version view
from flask_restful import Resource, Api

from App import auth
from App.proController import proBP
from Comment.myResponse import MyResponse
from Utils.myRequestParseUtil import MyRequestParseUtil
from Models.ProjectModel.versions import Version
from Models.ProjectModel.pro import Product
from App.myAuth import is_admin


class VersionController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        新建版本
        不打算做权限校验
        :return:
        """
        parse = MyRequestParseUtil()
        parse.add(name='name', required=True, type=str)
        parse.add(name="productID", required=True, type=int, isExist=Product)
        parse.add(name="desc", required=False, type=str)
        Version(**parse.parse_args()).save()
        return MyResponse.success()

    @auth.login_required
    @is_admin
    def delete(self) -> MyResponse:
        """
        delete
        :return: MyResponse
        """
        parse = MyRequestParseUtil()
        parse.add(name="id", type=int, required=True)
        Version.delete_by_id(**parse.parse_args())
        return MyResponse.success()

    @auth.login_required
    def put(self) -> MyResponse:
        """
        :return: MyResponse
        """
        parse = MyRequestParseUtil()
        parse.add(name="id", type=int, required=True)
        parse.add(name='name', required=False, type=str)
        parse.add(name="desc", required=False, type=str)
        Version.update(**parse.parse_args())
        return MyResponse.success()

    @auth.login_required
    def get(self) -> MyResponse:
        """
        get
        :return: MyResponse
        """
        parse = MyRequestParseUtil("value")
        parse.add(name="id", type=str, required=True)
        return MyResponse.success(Version.get(parse.parse_args().get("id"), "id"))


api_script = Api(proBP)
api_script.add_resource(VersionController, "/version")
