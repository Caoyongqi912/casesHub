# @Time : 2022/8/5 22:58 
# @Author : cyq
# @File : casePartSwagger.py 
# @Software: PyCharm
# @Desc:
from flask_restx import fields

from ..baseSwagger import BaseSwagger


class CasePartSwagger(BaseSwagger):

    @property
    def post(self):
        return self.ns.model("casePartPost", {
            "partName": fields.String( required=True),
            "projectID": fields.Integer
        })

    @property
    def get(self):
        return {
            "casePartID": ""
        }

    @property
    def put(self):
        return self.ns.model("casePartPut", {
            "id": fields.Integer,
            "partName": fields.String
        })

    @property
    def delete(self):
        return self.ns.model("casePartDelete", {
            "id": fields.Integer

        })
