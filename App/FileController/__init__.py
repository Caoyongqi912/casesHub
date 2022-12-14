# @Time : 2022/12/13 14:56 
# @Author : cyq
# @File : __init__.py.py 
# @Software: PyCharm
# @Desc:


from flask import Blueprint

fileBp = Blueprint("fileBp", __name__, url_prefix="/api/file")

from . import fileController
