from typing import AnyStr

from flask_restful import Resource
from flask import request, Response
from App import auth
from Comment.myResponse import MyResponse
from flask_restful import Api
from App.UploadController import fileBP
from faker import Faker
from werkzeug.utils import secure_filename
from Models.CaseModel.caseExcel import CaseExcel

from Utils import getExcelPath, getCaseXlsx


class UploadController(Resource):

    @auth.login_required
    def post(self) -> MyResponse:
        """
        上传附件
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


api_script = Api(fileBP)
api_script.add_resource(UploadController, "/")
