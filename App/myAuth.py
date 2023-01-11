# @Time : 2022/7/10 13:28 
# @Author : cyq
# @File : myAuth.py
# @Software: PyCharm
# @Desc: 登录与权限
from functools import wraps
from typing import AnyStr
from flask import g
from App import auth
from Comment import MyRedis
from Comment.myException import AuthException
from Models.UserModel.userModel import User


# @auth.verify_token
# def verify_token(token: str = None) -> bool:
#     if token:
#         g.user = User.verify_token(token)
#         return True
#     return False


@auth.verify_password
def verify_password_or_token(username_or_token: AnyStr, password: AnyStr) -> bool:
    """
    登录 密码 or token 校验
    :param password: 密码
    :param username_or_token: 密钥 或者用户名
    :return: bool
    """
    # 使用了用户名密码尝试登陆
    if username_or_token and password:
        user = User.query.filter(User.username == username_or_token).first()
        if not user or not user.verify_password(password):
            raise AuthException()
    else:
        # 使用token
        user = User.verify_token(token=username_or_token)
    g.user = user
    return True


def is_admin(func):
    """判断登录用户是否是admin"""

    @wraps(func)
    def wrap_func(*args, **kwargs):
        if not g.user.isAdmin:
            raise AuthException()
        return func(*args, **kwargs)

    return wrap_func


def is_DepartAdmin(func):
    """
    判断是部门ADMIN
    :param func:
    :return:
    """

    @wraps(func)
    def wrap_func(*args, **kwargs):
        print(args)
        print(kwargs)
        uid = g.user.id
        if g.user.isAdmin:
            pass
        return func(*args, **kwargs)

    return wrap_func
