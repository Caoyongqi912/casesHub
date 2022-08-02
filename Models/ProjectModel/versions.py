# @Time : 2022/7/10 21:12 
# @Author : cyq
# @File : versions.py 
# @Software: PyCharm
# @Desc: 版本实体

from typing import AnyStr, NoReturn

from Comment.myException import ParamException
from Comment.myResponse import ParamError
from Enums.errorCode import ResponseMsg
from Models.ProjectModel import Product
from Models.base import Base
from App import db
from Utils.myLog import MyLog

log = MyLog.get_log(__file__)


class Version(Base):
    __tablename__ = "version"
    name = db.Column(db.String(20), comment="版本名称")
    desc = db.Column(db.String(100), nullable=True, comment="版本描述")
    productID = db.Column(db.INTEGER, db.ForeignKey("product.id", ondelete="CASCADE"), comment="所属产品")
    # prd = db.Column(db.String(200), nullable=False, comment="需求链接")
    bugs = db.relationship("Bug", backref='version', lazy="dynamic")

    def __init__(self, name: AnyStr, productID: int, desc: AnyStr = None):
        self.name = name
        self.desc = desc
        self.productID = productID
        self.__unionName()

    def __unionName(self) -> NoReturn:
        """
        表设置不重名 但是产品下的不可重名 不同产品的版本重名
        :raise:  ParamError
        """
        v = [v.name for v in Product.get(self.productID).query_version]
        if self.name in v:
            raise ParamException(ResponseMsg.already_exist(self.name))

    def __repr__(self):
        return f"<{Version.__name__} {self.name}>"
