# @Time : 2022/7/5 21:35 
# @Author : cyq
# @File : base.py
# @Software: PyCharm
# @Desc: 模型基类
"""
Integer int 常规整形，通常为32位
SmallInteger    int 短整形，通常为16位
BigInteger  int或long    精度不受限整形
Float   float   浮点数
Numeric decimal.Decimal 定点数
String  str 可变长度字符串
Text    str 可变长度字符串，适合大量文本
Unicode unicode 可变长度Unicode字符串
Boolean bool    布尔型
Date    datetime.date   日期类型
Time    datetime.time   时间类型
Interval    datetime.timedelta  时间间隔
Enum    str 字符列表
PickleType  任意Python对象  自动Pickle序列化
LargeBinary str 二进制
primary_key 如果设置为True，则为该列表的主键
unique  如果设置为True，该列不允许相同值
index   如果设置为True，为该列创建索引，查询效率会更高
default 定义该列的默认值
unique	如果设为 True ,这列不允许出现重复的值
index	如果设为 True ,为这列创建索引,提升查询效率
nullable	如果设为 True ,这列允许使用空值;如果设为 False ,这列不允许使用空值
default	为这列定义默认值
"""
from typing import List, AnyStr
from sqlalchemy import desc
from App import db
from datetime import datetime
from Enums.errorCode import ResponseMsg
from Utils.log import MyLog
from Comment.myException import MyException, ParamException

log = MyLog.get_log(__file__)


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.Date, default=datetime.now, comment="创建时间")
    update_time = db.Column(db.Date, default=datetime.now, onupdate=datetime.now, comment="修改时间")

    def save(self):
        """save"""
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            log.error(e)
            db.session.rollback()
            raise MyException()

    def delete(self):
        """delete"""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            log.error(e)
            db.session.rollback()
            raise MyException()

    @classmethod
    def all(cls) -> List:
        """
        返回所有
        """
        return cls.query.filter_by().order_by(desc(cls.id)).all()

    @classmethod
    def get(cls, ident: int, name: AnyStr):
        """
        get entity by id
        :param ident: field id
        :param name: field name
        :return: get_or_NoFound
        """
        return cls.query.get_or_NoFound(ident, name)

    @classmethod
    def verify_unique(cls,  **kwargs) -> None:
        """verify_unique by field name"""
        rv = cls.query.filter_by(**kwargs).first()
        if rv:
            raise ParamException(ResponseMsg.already_exist(list(kwargs.values())[0]))
