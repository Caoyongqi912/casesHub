# @Time : 2022/7/16 17:26 
# @Author : cyq
# @File : __init__.py.py 
# @Software: PyCharm
# @Desc: caseBP

from flask import Blueprint

caseBP = Blueprint("caseBP", __name__, url_prefix="/api/case")

from . import bugController, caseController, casePartController, apiHostController, apiEnvValueController,interfaceController
