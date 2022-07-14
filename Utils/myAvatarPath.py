# @Time : 2022/7/13 20:44 
# @Author : cyq
# @File : myAvatarPath.py 
# @Software: PyCharm
# @Desc: 头像路径
import os
import time
from typing import AnyStr


def get_cwd(target: AnyStr) ->AnyStr:
    """获得根路径"""
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), target)
    return path


def getAvatarPath(file: AnyStr) -> AnyStr:
    filePath = get_cwd("resource")
    # 获取本地时间，转为年-月-日格式
    avatar_path = os.path.join(filePath, "Avatar")
    # 日期文件夹路径
    # 如果没有日期文件夹，创建该文件夹
    if not os.path.exists(avatar_path):
        os.makedirs(avatar_path)
    return os.path.join(os.path.join(filePath, avatar_path), file)


