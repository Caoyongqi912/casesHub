# @Time : 2022/12/13 14:59 
# @Author : cyq
# @File : fileController.py 
# @Software: PyCharm
# @Desc:
import asyncio
from flask import request, Response, g
from flask_restful import Resource
from App import auth, UID, limiter
from App.FileController import fileBp
from Comment.myResponse import MyResponse
from Enums.myEnum import FileEnum
from Models.CaseModel.fileModel import FileModel
from Models.FileModel.fileDB import FileDB
from Models.ProjectModel.projectModel import Project
from flask_restful import Api
from Utils.myFile import MyFile
from Utils.myRequestParseUtil import MyRequestParseUtil
from werkzeug.datastructures import FileStorage


class AvatarController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        上传用户头像
        :return:MyResponse
        """
        from werkzeug.datastructures import FileStorage
        file: FileStorage = request.files.get("file")
        if not file:
            return MyResponse.req_err()
        # 先校验是否有头像 存在删除历史头像
        user = g.user
        if g.user.avatar:
            f: FileModel = FileModel.get_by_uid(g.user.avatar)
            if f:
                MyFile.delAvatar(f.filePath)
                f.delete()  # 数据库删除
        file: FileModel = MyFile.writer(file, FileEnum.AVATAR)
        g.user.avatar = file.uid
        return MyResponse.success(file.uid)

    def get(self) -> Response:
        """
        返回用户头像
        :return: Response
        """
        parse: MyRequestParseUtil = MyRequestParseUtil("values")
        parse.add(name=UID, required=True)
        f: FileModel = FileModel.get_by_uid(**parse.parse_args)
        return Response(MyFile.reader(f), mimetype=f.fileType)


class BugController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        上传bug 附件
        :return:MyResponse
        """
        file: FileStorage = request.files.get("file")
        file: FileModel = MyFile.writer(file, FileEnum.BUG)
        return MyResponse.success(file.uid)

    def get(self) -> Response:
        """
        返回用户头像
        :return: Response
        """
        parse: MyRequestParseUtil = MyRequestParseUtil("values")
        parse.add(name=UID, required=True)
        f: FileModel = FileModel.get_by_uid(**parse.parse_args)
        return Response(MyFile.reader(f), mimetype=f.fileType)


class Excel2CaseController(Resource):

    @auth.login_required
    @limiter.limit("1/minute")  # 一分钟一次
    def post(self) -> MyResponse:
        """
        excel文件录入sql
        :return:
        """
        file: FileStorage = request.files.get("file")
        pid = request.form.get("projectID")
        file: FileModel = MyFile.writer(file, FileEnum.Excel, pid)
        return MyResponse.success()


class AsyncClass(Resource):

    def post(self):
        file: FileStorage = request.files.get("file")
        f = FileDB()
        f.file = file
        f.name = file.name
        f.type = file.mimetype
        f.save()
        return MyResponse.success()

    def get(self):
        parse: MyRequestParseUtil = MyRequestParseUtil("values")
        parse.add(name="id", required=True)
        f = FileDB.objects(**parse.parse_args).first()

        return Response(MyFile.reader(f.file), mimetype=f.fileType)


api_script = Api(fileBp)
api_script.add_resource(AvatarController, "/avatar")
api_script.add_resource(BugController, "/bug")
api_script.add_resource(Excel2CaseController, "/excel")
api_script.add_resource(AsyncClass, "/todo")
