# @Time : 2022/7/13 20:44 
# @Author : cyq
# @File : myAvatarPath.py 
# @Software: PyCharm
# @Desc: 头像路径
import os
import time
from typing import AnyStr


def get_cwd(target: AnyStr):
    """获得根路径"""
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), target)
    return path


def getAvatarPath(file: str) -> str:
    filePath = get_cwd("resource")
    print(filePath)
    # 获取本地时间，转为年-月-日格式
    local_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    avatar_path = os.path.join(filePath, "Avatar")
    # 日期文件夹路径
    date_file_path = os.path.join(avatar_path, local_date)
    # 如果没有日期文件夹，创建该文件夹
    if not os.path.exists(date_file_path):
        os.makedirs(date_file_path)
    return os.path.join(os.path.join(filePath, date_file_path), file)


if __name__ == '__main__':
    print(getAvatarPath("ASD"))
