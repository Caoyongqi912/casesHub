# @Time : 2022/7/6 22:19 
# @Author : cyq
# @File : __init__.py.py 
# @Software: PyCharm
# @Desc: 蓝本注册


from flask import Blueprint

userBP = Blueprint("user", __name__, url_prefix="/api/user")

from . import userController, departmentController
