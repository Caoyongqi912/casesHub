# @Time : 2022/7/14 20:05 
# @Author : cyq
# @File : product.py 
# @Software: PyCharm
# @Desc: 产品view
from typing import AnyStr

from flask_restful import Resource, Api

from App import auth
from App.proController import proBP
from Comment import MyResponse
from Utils import MyRequestParseUtil
from Models import Project, Product


class ProductController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        添加产品
        ADMIN or ProjectAdmin 可添加
        :return: MyResponse
        :raise ParamException | AuthException
        """
        parse = MyRequestParseUtil()
        parse.add(name="name", type=str, unique=Product, required=True)
        parse.add(name="desc", type=str, required=False)
        parse.add(name="projectID", type=int, isExist=Project, required=True)
        Product(**parse.parse_args()).save()
        return MyResponse.success()

    @auth.login_required
    def get(self) -> MyResponse:
        """
        分页查询
        :return:MyResponse
        :raise ParamException | AuthException
        """
        parse = MyRequestParseUtil("values")
        parse.add(name="page", default="1")
        parse.add(name="limit", default="20")
        parse.add(name="by", target=Product, required=False)
        res = Product.page(**parse.parse_args())
        return MyResponse.success(res)

    @auth.login_required
    def put(self) -> MyResponse:
        """
        维护
        :return: MyResponse
        :raise ParamException | AuthException
        """
        parse = MyRequestParseUtil()
        parse.add(name="id", type=int, isExist=Product, required=True)
        parse.add(name="name", type=str, required=False)
        parse.add(name="desc", type=str, required=False)
        Product.update(**parse.parse_args())
        return MyResponse.success()

    @auth.login_required
    def delete(self):
        """
        删除
        考虑是否删除 产品下所有 信息 [cases,version .....]
        :return: MyResponse
        """
        parse = MyRequestParseUtil()
        parse.add(name="id", type=int, required=True)
        Product.delete(**parse.parse_args())
        return MyResponse.success()


class QueryCaseController(Resource):

    @auth.login_required
    def get(self, productID: AnyStr) -> MyResponse:
        """
        通过MyResponse 分页查询
        :param productID: 产品ID
        :return: MyResponse
        """
        parse = MyRequestParseUtil("values")
        parse.add(name="page", default="1")
        parse.add(name="limit", default="20")
        parse.add(name="by", target=Product, required=False)
        res = Product.get(productID, "productID").page_case(**parse.parse_args())
        return MyResponse.success(res)


class QueryVersionController(Resource):

    @auth.login_required
    def get(self, productID: AnyStr) -> MyResponse:
        """
        通过MyResponse 分页查询
        :param productID: 产品ID
        :return: MyResponse
        """
        from Models.ProjectModel.versions import Version
        parse = MyRequestParseUtil("values")
        parse.add(name="page", default="1")
        parse.add(name="limit", default="20")
        parse.add(name="by", target=Version, required=False)
        res = Product.get(productID, "productID").page_version(**parse.parse_args())
        return MyResponse.success(res)


api_script = Api(proBP)
api_script.add_resource(ProductController, "/product/opt")
api_script.add_resource(QueryCaseController, "/product/<string:productID>/page_cases")
api_script.add_resource(QueryVersionController, "/product/<string:productID>/page_versions")
