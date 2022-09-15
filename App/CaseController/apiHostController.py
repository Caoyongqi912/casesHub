from flask_restful import Resource

from App.CaseController import caseBP
from Comment.myResponse import MyResponse
from MyException import Api
from App import auth


class HostController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        return MyResponse.success()

    @auth.login_required
    def get(self) -> MyResponse:
        return MyResponse.success()

    @auth.login_required
    def delete(self) -> MyResponse:
        return MyResponse.success()


api_script = Api(caseBP)
api_script.add_resource(HostController, "/host/opt")
