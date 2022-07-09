# @Time : 2022/7/7 23:30 
# @Author : cyq
# @File : index.py 
# @Software: PyCharm
# @Desc:
from flask_restful import Resource, Api
from App.indexController import indexPB
from Utils.log import MyLog
from Comment.myException import MyException

log = MyLog.get_log(__file__)


class Index(Resource):

    def get(self):
        log.info("sdfsfsdfsdfsdfsdfsd")
        raise MyException()


api_script = Api(indexPB)
api_script.add_resource(Index, "/")
