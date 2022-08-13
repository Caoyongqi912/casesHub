from typing import Union, NoReturn
from flask import request, Response
from Comment.myResponse import MyResponse
from Utils import MyLog

log = MyLog.get_log(__file__)


def logWrite() -> NoReturn:
    """
    请求钩子  日志写入请求参数
    :return:
    """
    log.info(
        f"[\n| request ip = {request.remote_addr} \n| request url = {request.url} \n| request Host = {request.host} \n| request Method = {request.method} ")


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
    # if response.status_code == 404:
    #     return jsonify(MyResponse.not_find())
    # elif response.status_code == 500:
    #     return jsonify(MyResponse.error(ResponseCode.SERVER_ERROR))
    # elif response.status_code == 403:
    #     return jsonify(AuthError.error())
    return response
