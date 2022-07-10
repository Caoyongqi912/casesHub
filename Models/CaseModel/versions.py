# @Time : 2022/7/10 21:12 
# @Author : cyq
# @File : versions.py 
# @Software: PyCharm
# @Desc: 版本实体

from typing import AnyStr
from Models.base import Base
from App import db
from Utils.log import MyLog

log = MyLog.get_log(__file__)


class Version(Base):
    __tablename__ = "version"

    name = db.Column(db.String(20), unique=True, comment="版本名称")
    desc = db.Column(db.String(100), nullable=True, comment="版本描述")

    from Models.ProjectModel.pro import Product
    productID = db.Column(db.INTEGER, db.ForeignKey("product.id"), nullabel=False, comment="所属产品")

    def __init__(self, name: AnyStr, desc: AnyStr, adminID: int,
                 productID: int):
        self.name = name
        self.desc = desc
        self.adminID = adminID
        self.productID = productID
