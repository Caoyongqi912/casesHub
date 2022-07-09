# @Time : 2022/7/7 23:30 
# @Author : cyq
# @File : __init__.py.py 
# @Software: PyCharm
# @Desc:


from flask import Blueprint

indexPB = Blueprint("index", __name__)

from . import index
