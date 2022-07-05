# @Time : 2022/7/5 21:48 
# @Author : cyq
# @File : users.py 
# @Software: PyCharm
# @Desc: 用户模型类
from typing import AnyStr

from base import Base
from App import db


class Users(Base):
    __tablename__ = "users"
    username = db.Column(db.String(20), unique=True, comment="用户名")
    phone = db.Column(db.String(12), unique=True, comment="手机")
    password = db.Column(db.String(100), comment="密码")
    email = db.Column(db.String(40), unique=True, comment="邮箱")
    gender = db.Column(db.Enum("MALE", "FEMALE"), server_default="MALE", comment="性别")
    avatar = db.Column(db.LargeBinary, nullable=True, comment="头像")
    isAdmin = db.Column(db.Boolean, default=False, comment="管理")

    def __int__(self, username: AnyStr, password: AnyStr, email: AnyStr, gender: AnyStr, isAdmin: bool):
        self.username = username
        self.password = password
        self.email = email
        self.gender = gender
        self.isAdmin = isAdmin


    def __repr__(self):
        return f"<{Users.__name__} {self.username}>"


if __name__ == '__main__':
    print(Users)
