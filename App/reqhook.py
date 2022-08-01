from typing import Union, NoReturn
from flask import request, Response, jsonify

from Comment.myResponse import MyResponse, AuthError
from Enums.errorCode import ResponseCode
from Utils.myLog import MyLog

log = MyLog().get_log(__file__)


def logWrite() -> NoReturn:
    """
    请求钩子  日志写入请求参数
    :return:
    """
    log.info(
        f"[request ip = {request.remote_addr} \n| request url = {request.url} \n| request Host = {request.host} \n| request Method = {request.method} \n| headers = {request.headers}]")


def resp(response: Response) -> Union[MyResponse, Response]:
    """
    response 钩子
    因为使用了工厂模式 无法使用errorhandler
    只能随便处理几个code 返回
    """
    log.info(
        f"[ response status_code = {response.status_code}]")
    # if response.status_code == 404:
    #     return jsonify(MyResponse.not_find())
    # elif response.status_code == 500:
    #     return jsonify(MyResponse.error(ResponseCode.SERVER_ERROR))
    # elif response.status_code == 403:
    #     return jsonify(AuthError.error())
    return response
