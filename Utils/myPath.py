# @Time : 2022/7/13 20:44 
# @Author : cyq
# @File : myPath.py
# @Software: PyCharm
# @Desc: 头像路径
import os
from typing import AnyStr, NoReturn
from .myLog import MyLog

log = MyLog.get_log(__file__)


def get_cwd(target: AnyStr) -> AnyStr:
    """
    获得 target 根路径
    :param target: str
    """
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), target)


def getAvatarPath(avatarName: AnyStr) -> AnyStr:
    """
    getAvatarPath
    :param avatarName: avatarName
    :return: avatarPath
    """
    filePath = get_cwd("resource")
    # 获取本地时间，转为年-月-日格式
    avatar_path = os.path.join(filePath, "Avatar")
    # 日期文件夹路径
    # 如果没有日期文件夹，创建该文件夹
    if not os.path.exists(avatar_path):
        os.makedirs(avatar_path)
    return os.path.join(os.path.join(filePath, avatar_path), avatarName)


def delAvatar(avatarName: AnyStr) -> NoReturn:
    """
    delAvatar
    :param avatarName:/api/user/avatar/WZrDttjEPwafFwLvjFiS_casesHub.png
    :return:
    """
    try:
        filename = getAvatarPath(avatarName.split("/")[-1])
        os.remove(filename)
    except FileNotFoundError as e:
        log.error(e)


def getExcelPath(file: AnyStr) -> AnyStr:
    filePath = get_cwd("resource")
    # 获取本地时间，转为年-月-日格式
    excel_path = os.path.join(filePath, "Excel")
    # 日期文件夹路径
    # 如果没有日期文件夹，创建该文件夹
    if not os.path.exists(excel_path):
        os.makedirs(excel_path)
    return os.path.join(os.path.join(filePath, excel_path), file)


if __name__ == '__main__':
    delAvatar("/api/user/avatar/WZrDttjEPwafFwLvjFiS_casesHub.png")
