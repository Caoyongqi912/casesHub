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


"""
关系表参数

ondelete: 级联删除
CASCADE 级联删除、 SET NULL 只有父表被删除，子表修改为NULL 、 RESTRICT 阻止删除数据
比如
productID = db.Column(db.INTEGER, db.ForeignKey("product.id",ondelete="CASCADE"), comment="所属产品")

lazy: ->relationship
懒加载 、 获取对象而非列表
比如
versions = db.relationship("Version", backref="product", lazy="dynamic")

cascade: ->relationship
save-update：在添加一条数据的时候，会把其他和它相关联的数据都添加到数据库中
delete:表示当删除某一个模型中的数据的时候，是否也删除掉使用relationship和它关联的数据。
delete-orphan:表示当对一个ORM对象解除了父表中的关联对象的时候，自己便会被删除掉。
当然如果表中的数据被删除，自己也会被删除。这个选项只能用在一对多上，不能用在多对多以及多对一上。
并且还需要在子模型中的relationship中，增加一个single_parent=True的参数。
merge:默认选项。当在使用session.merge，合并一个对象的时候，会将使用了relationship相关联的对象也进行merge操作
expunge:移除操作的时候，会将相关联的对象也进行移除。这个操作只是从session中移除，并不会真正的从数据库中删除。
all:是对save-update，merge，refresh-expire，expunge，delete几种的填写
比如
articles = relationship("Article",cascade="save-update,delete")

"""
from typing import List, AnyStr, Dict, NoReturn

from flask_sqlalchemy import Pagination
from sqlalchemy import asc
from App import db
from datetime import datetime
from Enums.errorCode import ResponseMsg
from Utils.myLog import MyLog
from Comment.myException import MyException, ParamException
from Utils.myUid import UUID

log = MyLog.get_log(__file__)


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(50), index=True, comment="唯一标识")
    create_time = db.Column(db.Date, default=datetime.now, comment="创建时间")
    update_time = db.Column(db.Date, default=datetime.now, onupdate=datetime.now, comment="修改时间")

    def save(self) -> NoReturn:
        """save"""
        try:
            self.uid = UUID().getUId
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            log.error(f"{self.__name__}  [ {e} ]")
            db.session.rollback()
            raise MyException()

    def delete(self) -> NoReturn:
        """delete"""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            log.error(e)
            db.session.rollback()
            raise MyException()

    @classmethod
    def delete_by_id(cls, id: int) -> NoReturn:
        """
        通过id 删除
        :param id: cls。id
        :raise:   ParamException
        """
        target = cls.get(id, f"{cls.__name__} id")
        target.delete()

    @classmethod
    def update(cls, **kwargs) -> NoReturn:
        """
        通过kwargs.get('id') 获得实例 修改
        """
        target = cls.get(kwargs.pop('id'))
        c = [i.name for i in cls.__table__.columns]
        for k, v in kwargs.items():
            if k in c:
                setattr(target, k, v)
        target.save()

    @classmethod
    def all(cls) -> List:
        """
        返回所有
        """
        return cls.query.filter_by().order_by(asc(cls.id)).all()

    @classmethod
    def get(cls, ident: int, name: AnyStr = None):
        """
        get entity by id
        :param ident: field id
        :param name: field name
        :return: get_or_NoFound
        """
        return cls.query.get_or_NoFound(ident, name)

    @classmethod
    def verify_unique(cls, **kwargs) -> NoReturn:
        """verify_unique by field name"""
        rv = cls.query.filter_by(**kwargs).first()
        if rv:
            raise ParamException(ResponseMsg.already_exist(list(kwargs.values())[0]))

    @staticmethod
    def to_json(obj) -> Dict:
        return {c.name: getattr(obj, c.name, None) for c in obj.__table__.columns}

    @classmethod
    def page(cls, **kwargs) -> Pagination:
        """
        :param page: 页
        :param limit: 数量
        :param by: filed
        :return:
        """
        return cls.query.my_paginate(**kwargs)
