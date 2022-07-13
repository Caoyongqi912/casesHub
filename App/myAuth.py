# @Time : 2022/7/10 13:28 
# @Author : cyq
# @File : myAuth.py
# @Software: PyCharm
# @Desc: 登录与权限
from functools import wraps
from typing import AnyStr
from flask import g
from App import auth
from Comment.myException import AuthException
from Models.UserModel.users import User


@auth.verify_password
def verify_password_or_token(username_or_token: AnyStr, password: AnyStr, ) -> bool:
    """
    登录 密码 or token 校验
    :param password: 密码
    :param username_or_token: 密钥 或者用户名
    :return: bool
    """

    user = User.verify_token(token=username_or_token)
    if not user:
        user = User.query.filter(User.username == username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


def is_admin(func):
    """判断登录用户是否是admin"""

    @wraps(func)
    def wrap_func(*args, **kwargs):
        if not g.user.admin:
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
        if g.user.admin:
            pass

        return func(*args, **kwargs)

    return wrap_func
