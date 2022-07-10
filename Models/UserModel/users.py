# @Time : 2022/7/5 21:48 
# @Author : cyq
# @File : users.py 
# @Software: PyCharm
# @Desc: 用户模型类
import time
import jwt  # py3.10+ 需要修改   from collections.abc  import Mapping
from typing import AnyStr, Union, Any
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from Utils.log import MyLog
from Models.base import Base
from App import db

log = MyLog.get_log(__file__)


class User(Base):
    __tablename__ = "user"
    username = db.Column(db.String(20), unique=True, comment="用户名")
    phone = db.Column(db.String(12), unique=True, comment="手机")
    password = db.Column(db.String(200), comment="密码")
    email = db.Column(db.String(40), unique=True, comment="邮箱")
    gender = db.Column(db.Enum("MALE", "FEMALE"), server_default="MALE", comment="性别")
    avatar = db.Column(db.LargeBinary, nullable=True, comment="头像")
    isAdmin = db.Column(db.Boolean, default=False, comment="管理")

    from .departments import Department  # 不同文件下需引入
    departmentID = db.Column(db.INTEGER, db.ForeignKey("department.id"), nullable=False, comment="所属部门")

    def __init__(self, username: AnyStr, password: AnyStr, phone: AnyStr, email: AnyStr,
                 gender: AnyStr, isAdmin: bool, departmentID: int):
        self.username = username
        self.hash_password(password)
        self.email = email
        self.gender = gender
        self.phone = phone
        self.isAdmin = isAdmin
        self.departmentID = departmentID

    def hash_password(self, password: AnyStr):
        """
        密码加密
        :param password:  password
        :return: hash_password
        """
        self.password = generate_password_hash(password)

    def generate_token(self, expires_time: int = 3600 * 24):
        """
        生成token
        :param expires_time: 过期时间 默认 一天
        :return: token
        """
        token = {"id": self.id, "expires_time": time.time() + expires_time}
        return jwt.encode(token, current_app.config["SECRET_KEY"], algorithm="HS256")

    @staticmethod
    def verify_token(token: AnyStr) -> Union[None, Any]:
        """
        token 解密
        :param token:
        :return: None or user
        """
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithm=["HS256"])
        except Exception as e:
            log.error(e)
            return None
        return User.query.get(data['id'])

    def verify_password(self, password: AnyStr) -> bool:
        """
        校验密码
        :param password: password
        :return: bool
        """
        return check_password_hash(self.password, password)

    @property
    def admin(self) -> bool:
        """
        :return:
        """
        return self.isAdmin

    def __repr__(self):
        return f"<{User.__name__} {self.username}>"
