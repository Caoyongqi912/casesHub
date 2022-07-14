# @Time : 2022/7/14 20:05 
# @Author : cyq
# @File : product.py 
# @Software: PyCharm
# @Desc: 产品view
from flask_restful import Resource, Api

from App import auth
from App.myAuth import is_admin
from App.proController import proBP
from Comment.myResponse import MyResponse
from Utils.myRequestParseUtil import MyRequestParseUtil
from Models.ProjectModel.pro import Project, Product


class ProductController(Resource):

    @auth.login_required
    @is_admin
    def post(self) -> MyResponse:
        """
        添加产品
        :return: MyResponse
        """
        parse = MyRequestParseUtil()
        parse.add(name="name", type=str, required=True)
        parse.add(name="desc", type=str)
        parse.add(name="projectID", type=int, required=True)
        parse.add(name="adminID", type=int, required=True)
        from Models.UserModel.users import User
        product = parse.parse_args()
        Project.get(product.get("projectID"), "projectID")
        User.get(product.get("adminID"), "userID")
        Product(**product).save()
        return MyResponse.success()

    @auth.login_required
    def get(self):
        """
         分页查询
         :return:
         """
        parse = MyRequestParseUtil("values")
        parse.add(name="page", default="1")
        parse.add(name="limit", default="20")
        pages = parse.parse_args()
        res = Product.page(**pages)
        return MyResponse.success(res)

    @auth.login_required
    def put(self):
        pass

    @auth.login_required
    def delete(self):
        pass


api_script = Api(proBP)
api_script.add_resource(ProductController, "product")
