# @Time : 2022/7/16 17:26 
# @Author : cyq
# @File : __init__.py.py 
# @Software: PyCharm
# @Desc: caseBP

from flask import Blueprint
from flask_restx import Api

caseBP = Blueprint("caseBP", __name__, url_prefix="/api/case")
apiBP = Api(caseBP)

from .case import casePartNamespace, caseNamespace
from .bug import bugNamespace

apiBP.add_namespace(caseNamespace)
apiBP.add_namespace(casePartNamespace)
apiBP.add_namespace(bugNamespace)
