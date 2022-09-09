from flask_restful import Resource

from App.NewHome import newHomeBP
from Comment.myResponse import MyResponse
from MyException import Api
from Utils.myRequestParseUtil import MyRequestParseUtil





class NewPan(Resource):

    def post(self):
        parse = MyRequestParseUtil()
        parse.add(name="creator", type=str, required=True)
        parse.add(name="name", type=str, required=True)
        from Comment.newhome import addPan
        addPan(*parse.parse_args())
        return MyResponse.success()


api = Api(newHomeBP)
api.add_resource(NewPan, "/newPan")
