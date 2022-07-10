# @Time : 2022/7/10 21:17 
# @Author : cyq
# @File : cases.py 
# @Software: PyCharm
# @Desc: 用例实体


from Models.base import Base
from App import db
from Utils.log import MyLog

log = MyLog.get_log(__file__)


class Case(Base):
    __tablename__ = "case"
    title = db.Column(db.String(20), unique=True, comment="用例名称")
    desc = db.Column(db.String(100), nullable=True, comment="用例描述")
    creator = db.Column(db.INTEGER, nullable=False, comment="创建人")
    updater = db.Column(db.INTEGER, nullable=False, comment="修改人")
    setup = db.Column(db.String(100), nullable=True, comment="用例前置")
    steps = db.Column(db.JSON, nullable=False, comment="用例步骤")
    exp = db.Column(db.String(100), nullable=True, comment="用例预期")
    res = db.Column(db.String(100), nullable=False, comment="用例实际")
    level = db.Column(db.Enum("P1", "P2", "P3", "P4"), server_default="P1", comment="用例等级")
    show_type = db.Column(db.Enum(1, 2, 3), server_default=1, comment="用例等级")  # 1 excel # xmind # normal
    case_type = db.Column(db.Enum(1, 2, 3), server_default=1, comment="用例等级")  # 1 功能 2 接口 3 性能
    mark = db.Column(db.String(100), nullable=True, comment="用例备注")
    prd = db.Column(db.String(200), nullable=True, comment="需求链接")

    from .bugs import Bug
    bugID = db.Column(db.INTEGER, db.ForeignKey("bug.id"), nullable=True, comment="bug")
    bug = db.relationship("Bug", back_populates="case")

    from .platforms import Platform
    platformID = db.Column(db.INTEGER, db.ForeignKey('platform.id'), comment="所属平台")

    from .versions import Version
    versionID = db.Column(db.INTEGER, db.ForeignKey('version.id'), comment="所属版本")

    from Models.ProjectModel.pro import Project,Product
    projectID = db.Column(db.INTEGER, db.ForeignKey("project.id"), nullable=True, comment="所属项目")
    productID = db.Column(db.INTEGER, db.ForeignKey("product.id"), nullable=True, comment="所属产品")
