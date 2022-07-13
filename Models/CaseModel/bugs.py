# @Time : 2022/7/10 21:55 
# @Author : cyq
# @File : bugs.py 
# @Software: PyCharm
# @Desc: bug实体


from Models.base import Base
from App import db
from Utils.myLog import MyLog

log = MyLog.get_log(__file__)


class Bug(Base):
    __tablename__ = "bug"
    name = db.Column(db.String(20), unique=True, comment="bug名称")
    desc = db.Column(db.String(100), nullable=True, comment="bug描述")
    tester = db.Column(db.String(20), nullable=False, comment="测试")
    developer = db.Column(db.String(20), nullable=False, comment="测试")
    pr = db.Column(db.String(20), nullable=False, comment="产品")
    level = db.Column(db.Enum("P1", "P2", "P3", "P4"), server_default="P1", comment="BUG等级")
    status = db.Column(db.Enum("OPEN", "CLOSE"), server_default="OPEN", comment="BUG状态")
    file = db.Column(db.String(50), nullable=False, comment="附件地址")
    mark = db.Column(db.String(100), nullable=True, comment="BUG备注")

    from .cases import Case
    case = db.relationship("Case", uselist=False, back_populates="bug")
