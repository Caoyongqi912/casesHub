import traceback
from typing import Union, NoReturn

import sqlalchemy
from flask import request, Response
from flask_limiter import RateLimitExceeded
from werkzeug.exceptions import HTTPException, MethodNotAllowed

from App import io
from Comment.myException import AuthException, ParamException, MyException
from Comment.myResponse import MyResponse
from Utils import MyLog

log = MyLog.get_log(__file__)


def logWrite() -> NoReturn:
    """
    请求钩子  日志写入请求参数
    :return:
    """
    # log.info(
    #     f"request ip = {request.remote_addr} \n"
    #     f"request url = {request.url} \n"
    #     f"request Host = {request.host} \n"
    #     f"request Method = {request.method} ")
    # log.info(request.headers)
    pass


def resp(response: Response) -> Union[MyResponse, Response]:
    """
    response 钩子
    因为使用了工厂模式 无法使用errorhandler
    只能随便处理几个code 返回
    """
    log.info(
        f"[ response status_code = {response.status_code}]")
    log.info(
        f"[ response body = {response.json} ]"
    )
    return response


def register_errors(app):
    @app.errorhandler(Exception)
    def framework_error(e):
        tb = traceback.format_exc()
        log.error(f"{repr(e)}\n{tb}")
        if isinstance(e, AuthException | ParamException | MethodNotAllowed):
            return e
        if isinstance(e, RateLimitExceeded):
            return MyException("too manny request! be wait ..")
        if isinstance(e, sqlalchemy.exc.OperationalError):
            return MyException("MySQL server error")
        return MyException()


@io.on('connect')
def handle_connect():
    from flask_socketio import join_room
    join_room(room=request.args.get("room"))
    log.info("WebSocket connected join room")


@io.on("disconnect")
def handle_disconnect():
    from flask_socketio import close_room
    close_room(room=request.args.get("room"))
    log.info("WebSocket disconnect close room")
