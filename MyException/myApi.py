# @Time : 2022/8/21 13:08 
# @Author : cyq
# @File : myApi.py 
# @Software: PyCharm
# @Desc:
from flask_limiter import RateLimitExceeded
from flask_restful import Api as _Api
from werkzeug.exceptions import HTTPException
from Comment.myException import MyException, AuthException, ParamException
from Utils import MyLog

log = MyLog.get_log(__file__)


class Api(_Api):

    def handle_error(self, e: Exception) -> HTTPException:
        """
        捕获全局异常
        :param e: the raised Exception object
        :return:MyException
        """
        log.error(e)
        if isinstance(e, AuthException | ParamException):
            return e
        if isinstance(e, RateLimitExceeded):
            return MyException("too manny request! be wait ..")
        return MyException()
