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
from App import db


class PerfSettingController(Resource):

    def get(self):
        data = RrefSettingModel.all()
        return MyResponse.success(data)


api_script = Api(cbsBP)
api_script.add_resource(PerfSettingController, "/perf/setting")
