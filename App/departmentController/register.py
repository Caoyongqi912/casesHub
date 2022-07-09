# @Time : 2022/7/6 22:24 
# @Author : cyq
# @File : register.py
# @Software: PyCharm
# @Desc: 注册
from flask import jsonify
from flask_restful import Resource, Api,reqparse
from App.departmentController import userBP
from Utils.requestParseUtil import MyRequestParseUtil


class RegisterController(Resource):

    def post(self) -> jsonify:
        """
        注册
        :return: jsonify
        """
        parse = MyRequestParseUtil()
        parse.add(name="username", type=str, required=True)


        return jsonify({"hello": "world"})


api_script = Api(userBP)
api_script.add_resource(RegisterController, "/register")
