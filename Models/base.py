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
from sqlalchemy.engine import CursorResult

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
with_entities
"""
from typing import List, AnyStr, Dict, NoReturn
from flask_sqlalchemy import Pagination
from sqlalchemy import asc, Column
from App import db
from datetime import datetime
from Enums import ResponseMsg
from Utils import MyLog, UUID, pageSerialize, MyTools
from Comment.myException import MyException, ParamException

log = MyLog.get_log(__file__)


class Base(db.Model):
    __abstract__ = True
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid: str = db.Column(db.String(50), index=True, comment="唯一标识")
    create_time: str = db.Column(db.DATETIME, default=datetime.now, comment="创建时间")
    update_time: str = db.Column(db.DATETIME, default=datetime.now, onupdate=datetime.now, comment="修改时间")

    def save(self) -> NoReturn:
        """save"""
        try:
            self.uid: str = UUID().getUId
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            log.error(f"db save error:  [ {repr(e)} ]")
            db.session.rollback()
            raise MyException()

    def delete(self) -> NoReturn:
        """delete"""
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            log.error(repr(e))
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
        id
        通过kwargs.get('id') 获得实例 修改
        """
        target = cls.get(kwargs.pop('id'))
        c = cls.columns()
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
    def search_like(cls, target: str, value: str):
        """
        模糊查询
        :param target: username  cls.column
        :param value:  search value
        :return: execute_sql
        """
        sql = "select * from {} where {} like '{}%'".format(cls.__tablename__, target, value)
        res = Base.execute_sql(sql)
        return res

    @classmethod
    def get(cls, ident: int | str, name: AnyStr = None):
        """
        get entity by id
        :param ident: field id
        :param name: field name
        :return: get_or_NoFound
        """
        return cls.query.get_or_NoFound(ident, name)

    @classmethod
    def get_by_uid(cls, uid):
        """
        通过uid 查询
        :param uid: uid
        :return:
        :raise: ParamException
        """
        rv = cls.query.filter_by(uid=uid).first()
        if not rv:
            raise ParamException(ResponseMsg.ERROR)
        return rv

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
    @pageSerialize
    def page(cls, pageSize: int, current: int, sort: str = None, filter_key: Dict = None) -> Pagination:
        """
        paginate
        :param filter_key:  filter_by(**filter_key)
        :param pageSize:    pageSize
        :param current:    current
        :param sort:    order_by(sort)
        :return:    Pagination
        """
        _fk = filter_key if filter_key else {}
        items = db.session.query(cls).filter_by(**_fk).order_by(sort).order_by(cls.create_time.desc()).limit(
            pageSize).offset(
            (current - 1) * pageSize).all()
        total = db.session.query(cls).filter_by(**_fk).order_by(sort).count()
        return Pagination(cls, current, pageSize, total, items)

    @staticmethod
    def search(nums: List[int], target: int) -> bool:
        """
        二分查找 存在返回True 不存在返回False
        :param nums:
        :param target:
        :return:bool
        """
        left, right = 0, len(nums) - 1
        while left <= right:
            mid = (right - left) // 2 + left
            num = nums[mid]
            if num == target:
                return True
            elif num > target:
                right = mid - 1
            else:
                left = mid + 1
        return False

    @classmethod
    def columns(cls) -> List[str]:
        """
        返回 cls 下所有column
        """
        return [c.name for c in cls.__table__.columns]

    @staticmethod
    def execute_sql(sql) -> List[Dict[str, str]] | None:
        """
        执行sql
        :param sql: sql
        :return: List[Dict[str, str]] | None
        """

        result: CursorResult = db.session.execute(sql)
        cursor = result.cursor
        if not cursor:
            return
        result_dict = [dict(zip([field[0].lower() for field in cursor.description], v)) for v in cursor.fetchall()]
        return result_dict

    @classmethod
    def search_data(cls, **kwargs):
        """
        字段搜索
        :param kwargs:
        :return:
        """

        log.info(cls.__tablename__)
        param: str = MyTools.kw2str(**kwargs)
        sql = f"select * from {cls.__tablename__} where {param}"
        res = Base.execute_sql(sql)
        return res
