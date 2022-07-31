# @Time : 2022/7/14 20:04 
# @Author : cyq
# @File : __init__.py.py 
# @Software: PyCharm
# @Desc:

from flask import Blueprint

proBP = Blueprint("pro", __name__, url_prefix="/api/pro")

from . import project, product
