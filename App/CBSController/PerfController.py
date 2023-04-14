#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023-04-11
# @Author : cyq
# @File : casesHub
# @Software: PyCharm
# @Desc:
from flask_restful import Resource, Api

from Comment.myResponse import MyResponse
from Models.CBSModel.PrefModel import RrefSettingModel
from App.CBSController import cbsBP
from Utils.myRequestParseUtil import MyRequestParseUtil


class PerfSettingController(Resource):

    def get(self):
        parse: MyRequestParseUtil = MyRequestParseUtil("values")
        parse.add(name="city", default="bj", required=False, type=str)
        data = RrefSettingModel.get_all(**parse.parse_args)
        return MyResponse.success(data)


api_script = Api(cbsBP)
api_script.add_resource(PerfSettingController, "/perf/setting")
