from typing import AnyStr

from flask_restful import Resource
from flask import request, Response
from App import auth
from Comment.myResponse import MyResponse
from Models.CaseModel.fileModel import FileModel
from MyException import Api
from App.CaseController import caseBP
from faker import Faker
from werkzeug.utils import secure_filename
from Models.CaseModel.caseExcel import CaseExcel

from Utils import getExcelPath, getCaseXlsx, getBugFilePath


class UploadExcelController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        上传excel 附件
        :return:
        """
        f = Faker()
        file = request.files.get("file")
        fileName = f.pystr() + '.' + secure_filename(file.filename)  # excel名称
        filePath = getExcelPath(fileName)  # excel路径
        file.save(filePath)
        caseExcel = CaseExcel(fileName, filePath)
        caseExcel.save()
        return MyResponse.success(caseExcel.uid)

    # @auth.login_required
    def get(self) -> Response:
        """
        获取模板
        :return:
        """
        path: AnyStr = getCaseXlsx()
        with open(path, "rb") as f:
            file: AnyStr = f.read()
        return Response(file, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


class UploadBugFileController(Resource):

    @auth.login_required
    def post(self, bugID: str) -> MyResponse:
        """
        上传bug 附件
        :return:
        """
        f = FileModel()
        a = f.todo(bugID, request.files.get("file"))
        return MyResponse.success(a)


class GetBugFileController(Resource):

    @auth.login_required
    def get(self, fileName: str) -> Response:
        """
        返回bug 附件
        :param fileName: 附件名称
        :return: Response
        """
        b: FileModel = FileModel.get_by_field(fileName=fileName)

        path: AnyStr = getExcelPath(b.fileName)
        with open(path, "rb") as f:
            bugFIle: AnyStr = f.read()
        return Response(bugFIle, mimetype=b.fileType)


api_script = Api(caseBP)
api_script.add_resource(UploadExcelController, "/excel")
api_script.add_resource(UploadBugFileController, "/bug/<string:bugID>/bug_file")
api_script.add_resource(GetBugFileController, "/bug/bug_file/<string:fileName>")
