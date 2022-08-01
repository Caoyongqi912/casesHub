from typing import Union, NoReturn
from flask import request, Response
from Comment.myResponse import MyResponse
from Utils.myLog import MyLog

log = MyLog().get_log(__file__)


def logWrite() -> NoReturn:
    log.info(
        f"[ request url = {request.url} | request Host = {request.host} | request Method = {request.method} | headers = {request.headers}]")


def resp(response: Response) -> Union[MyResponse, Response]:
    log.info(
        f"[ response status_code = {response.status_code}]")
    if response.status_code == 404:
        return MyResponse.not_find()

    return response
