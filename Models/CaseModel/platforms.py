# @Time : 2022/7/10 21:15 
# @Author : cyq
# @File : platforms.py 
# @Software: PyCharm
# @Desc: 平台实体


from typing import AnyStr
from Models.base import Base
from App import db


class Platform(Base):
    __tablename__ = "platform"

    name = db.Column(db.String(20), unique=True, comment="平台名称")
    desc = db.Column(db.String(100), nullable=True, comment="平台描述")

    def __init__(self, name: AnyStr, desc: AnyStr):
        self.name = name
        self.desc = desc
