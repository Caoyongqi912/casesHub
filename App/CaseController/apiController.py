"""
接口用例
1、crud
2、运行结果校验与结果持久化
"""

from flask_restful import Resource


class ApiController(Resource):
    pass



if __name__ == '__main__':
    d = {"name":"cuq","age":1,"other":"Adad"}
    d["name"] = d.get("fdds")
    print(d)