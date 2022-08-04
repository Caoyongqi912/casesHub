# @Time : 2022/7/5 21:48 
# @Author : cyq
# @File : userModel.py
# @Software: PyCharm
# @Desc: 用户模型类

from typing import Dict
from Models.base import Base
from App import db
from typing import AnyStr, Union
import time
import jwt  # py3.10+ 需要修改   from collections.abc  import Mappin
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from Comment.myException import ParamException
from Enums import ResponseMsg
from Utils import MyLog

log = MyLog().get_log(__file__)


class User(Base):
    mail = "@caseHub.com"
    __tablename__ = "user"
    username = db.Column(db.String(20), unique=True, comment="用户名")
    phone = db.Column(db.String(12), unique=True, comment="手机")
    password = db.Column(db.String(200), comment="密码")
    email = db.Column(db.String(40), unique=True, comment="邮箱")
    gender = db.Column(db.Enum("MALE", "FEMALE"), comment="性别")
    avatar = db.Column(db.String(400), nullable=True, comment="头像")
    isAdmin = db.Column(db.Boolean, default=False, comment="管理")
    tag = db.Column(db.Enum("QA", "PR", "DEV", "ADMIN"), comment="标签")
    departmentID = db.Column(db.INTEGER, db.ForeignKey("department.id"), nullable=True, comment="所属部门")

    def __init__(self, username: AnyStr, phone: AnyStr, gender: AnyStr,
                 tag: AnyStr = None, isAdmin: bool = False,
                 departmentID: int = None,
                 password: AnyStr = None):
        self.username = username
        self.email = self.username + self.mail
        self.gender = gender
        self.phone = phone
        self.tag = tag
        self.isAdmin = isAdmin
        if password:
            self.hash_password(password)
        else:
            self.hash_password(username)

        self.departmentID = departmentID

    def addAdmin(self):
        """
        添加管理员
        isAdmin = True
        tag = ADMIN
        """
        self.isAdmin = True
        self.tag = "ADMIN"
        self.save()

    def addUser(self):
        """
        管理员添加用户
        password = username
        email = username + self.mail
        isAdmin = False
        """
        self.isAdmin = False
        self.hash_password(self.username)
        self.email = self.username + self.mail
        self.save()

    def hash_password(self, password: AnyStr):
        """
        密码加密
        :param password:  password
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

    @classmethod
    def query_by_tag(cls, tag: AnyStr):
        if tag not in ["QA", "PR", "DEV", "ADMIN"]:
            raise ParamException(ResponseMsg.error_val(tag, ["QA", "PR", "DEV", "ADMIN"]))

        return cls.query.filter(User.tag == tag).all()

    @staticmethod
    def verify_token(token: AnyStr) -> Union[None,]:
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
        :return: bool
        """
        return self.isAdmin

    @classmethod
    def login(cls, username: AnyStr, password: AnyStr):
        user = cls.query.filter(User.username == username).first()
        if user:
            if user.verify_password(password):
                token = user.generate_token().decode("utf-8")
                return token
            raise ParamException("password err!")
        else:
            raise ParamException("username err!")

    @staticmethod
    def to_json(obj) -> Dict:
        """
        序列化 删除密码字段
        :param obj: User
        :return: user serializer
        """
        res = super(User, User).to_json(obj)
        res.pop("password")
        return res

    def __repr__(self):
        return f"<{User.__name__} {self.username}>"
