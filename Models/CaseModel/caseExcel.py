from Models.base import Base
from App import db
from Utils import MyLog

log = MyLog.get_log(__file__)


class CaseExcel(Base):
    __tablename__ = "case_excel"
    fileName = db.Column(db.String(50), unique=True, comment="附件名")
    filePath = db.Column(db.String(200), comment="附件路径")

    def __init__(self, fileName: str, filePath: str):
        self.filePath = filePath
        self.fileName = fileName
