from flask_restx import fields

from ..baseSwagger import BaseSwagger


class CaseSwagger(BaseSwagger):

    @property
    def post(self):
        return self.ns.model("casePost", {
            "title": fields.String(required=True, description="用例标题"),
            "tag": fields.String(enum=['常规', '冒烟'], required=False, description="用例标签"),
            "desc": fields.String(description="用例描述", required=True),

        })

    @property
    def get(self):
        pass

    @property
    def put(self):
        pass

    @property
    def delete(self):
        pass
