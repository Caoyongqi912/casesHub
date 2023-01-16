# @Time : 2022/7/5 21:48 
# @Author : cyq
# @File : userModel.py
# @Software: PyCharm
# @Desc: 用户模型类

from typing import Dict, NoReturn, TypeVar

from Models.base import Base
from App import db
from typing import AnyStr
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from Comment.myException import ParamException, AuthException
from Enums import Gender, IntEnum, ResponseMsg
from Utils import MyLog, simpleUser, MyTools
import time
import jwt  # py3.10+ 需要修改   from collections.abc  import Mapping

log = MyLog.get_log(__file__)
UserType = TypeVar("UserType", bound=Base)


class User(Base):
    __tablename__: str = "user"
    _mail = "@caseHub.com"
    username: str = db.Column(db.String(20), comment="用户名")
    phone: str = db.Column(db.String(12), unique=True, comment="手机")
    password: str = db.Column(db.String(200), comment="密码")
    email: str = db.Column(db.String(40), unique=True, comment="邮箱")
    gender: Gender = db.Column(IntEnum(Gender), comment="性别")
    avatar: str = db.Column(db.String(400), nullable=True, comment="头像")
    isAdmin: bool = db.Column(db.Boolean, default=False, comment="管理")
    departmentID: int = db.Column(db.INTEGER, db.ForeignKey("department.id", ondelete="set null"), nullable=True,
                                  comment="所属部门")
    departmentName: str = db.Column(db.String(20), nullable=True, comment="所属部门名称")
    tagName: str = db.Column(db.String(20), nullable=True, comment="对应标签名称")

    def __init__(self, username: str, phone: str, gender: Gender = Gender.MALE,
                 tagName: str = None, isAdmin: bool = False,
                 departmentID: int = None,
                 departmentName: str = None,
                 password: str = None):
        self.username: str = username
        self.email: str = MyTools.pinyin(self.username) + self._mail
        self.gender: Gender = gender
        self.phone: str = phone
        self.tagName = tagName
        self.isAdmin: bool = isAdmin
        if password:
            self.hash_password(password)
        else:
            self.hash_password(MyTools.pinyin(self.username))
        self.departmentID: int = departmentID
        self.departmentName: str = departmentName

    def addAdmin(self) -> NoReturn:
        """
        添加管理员
        """
        self.isAdmin: bool = True
        self.save()


    def addUser(self) -> NoReturn:
        """
        管理员添加用户
        password = username
        email = username + self.mail
        isAdmin = False
        """
        self.isAdmin: bool = False
        self.hash_password(MyTools.pinyin(self.username))
        self.email: str = MyTools.pinyin(self.username + self._mail)
        self.save()

    @classmethod
    def search_like(cls, target: str, value: str) -> simpleUser:
        """
        sql执行模糊查询
        :param target: username  cls.column
        :param value:  search value
        :return: execute_sql
        """
        sql = """Select id,uid,username,create_time,update_time From user Where {} Like '{}%'""".format(target, value)
        res = cls.execute_sql(sql)
        return res


    def set_password(self, old_password: str, new_password: str) -> NoReturn:
        """
        修改密码
        :param old_password:
        :param new_password:
        :return:
        """
        if self.verify_password(old_password):
            self.hash_password(new_password)
            self.save(new=False)
        else:
            raise ParamException(ResponseMsg.error_param("old password"))

    def hash_password(self, password: AnyStr) -> NoReturn:
        """
        密码加密
        :param password:  password
        """
        self.password: str = generate_password_hash(password)

    def generate_token(self, expires_time: int = 3600 * 24) -> str:
        """
        生成token
        :param expires_time: 过期时间 默认 一天
        :return: token
        """
        token = {"id": self.id, "expires_time": time.time() + expires_time}
        return jwt.encode(token, current_app.config["SECRET_KEY"], algorithm="HS256")

    @classmethod
    def verify_token(cls, token: AnyStr) -> UserType:
        """
        token 解密
        :param token:
        :return: UserType
        """
        try:
            data: Dict[str, str | int] = jwt.decode(token, current_app.config['SECRET_KEY'], algorithm=["HS256"])
            return cls.query.get(data['id'])
        except Exception as e:
            log.error(repr(e))
            raise AuthException()

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
    def login(cls, username: AnyStr, password: AnyStr) -> Dict[str, str]:
        user = cls.query.filter(User.username == username).first()
        if user:
            if user.verify_password(password):
                token = user.generate_token().decode("utf-8")
                # MyRedis().handle_redis_token(user.uid,token)
                return {'token': token}
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
