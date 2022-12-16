# @Time : 2022/7/13 20:44 
# @Author : cyq
# @File : myFile.py
# @Software: PyCharm
# @Desc: 头像路径
import os
from typing import AnyStr, NoReturn

from flask import g
from werkzeug.datastructures import FileStorage

from Enums.myEnum import FileEnum
from Models.CaseModel.fileModel import FileModel
from Utils import UUID
from Utils.myExcel import MyExcel


def get_cwd(target: AnyStr) -> AnyStr:
    """
    获得 target 根路径
    :param target: str
    """
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), target)


def verify_dir(_path: str):
    if not os.path.exists(_path):
        os.makedirs(_path)


ROOT = get_cwd("Files")


class MyFile:
    """
    :todo
    上传文件。生成路径、入库
    文件读写
    """
    AVATAR = os.path.join(ROOT, "Avatar")
    BUG = os.path.join(ROOT, "Bug")
    EXCEL = os.path.join(ROOT, "Excel")

    @staticmethod
    def writer(file: FileStorage, T: FileEnum, pid: str = None) -> FileModel:
        """
        写入文件
        :param file: FileStorage
        :param T: 类型
        :param pid: 项目id
        :return:
        """
        fileName = UUID().getUId
        if T == FileEnum.AVATAR:
            verify_dir(MyFile.AVATAR)
            target = os.path.join(MyFile.AVATAR, fileName)
        elif T == FileEnum.Excel:
            verify_dir(MyFile.EXCEL)
            target = os.path.join(MyFile.EXCEL, fileName)
        elif T == FileEnum.BUG:
            verify_dir(MyFile.BUG)
            target = os.path.join(MyFile.BUG, fileName)
            MyExcel(target).sheetReader(pid, g.user.id)
        else:
            raise Exception
        file.save(target)
        f = FileModel(fileName, file.mimetype, target)
        f.save()
        return f

    @staticmethod
    def delAvatar(avatarPath: AnyStr) -> NoReturn:
        """
        delAvatar
        :param avatarPath: 绝对路径
        :return:
        """
        os.remove(avatarPath)

    @staticmethod
    def reader(f: FileModel):
        with open(f.filePath, "rb") as f:
            return f.read()


if __name__ == '__main__':
    m = MyFile()
    m.writer("avatar")
