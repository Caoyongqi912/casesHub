# @Time : 2022/7/16 18:01 
# @Author : cyq
# @File : __init__.py.py 
# @Software: PyCharm
# @Desc: platform bp

from flask import Blueprint

platformBP = Blueprint("platform", __name__, url_prefix="/api/platform")

from . import platform
