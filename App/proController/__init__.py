# @Time : 2022/7/14 20:04 
# @Author : cyq
# @File : __init__.py.py 
# @Software: PyCharm
# @Desc:

from flask import Blueprint

proBP = Blueprint("pro", __name__, url_prefix="/v1/api/pro")

from . import product, project,version,report
