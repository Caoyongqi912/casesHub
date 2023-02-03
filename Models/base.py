# @Time : 2022/7/5 21:35
# @Author : cyq
# @File : base.py
# @Software: PyCharm
# @Desc: 模型基类

from sqlalchemy.engine import CursorResult
from typing import List, AnyStr, Dict, NoReturn, Any
from flask_sqlalchemy import Pagination
from sqlalchemy import asc, Column, or_,and_
from App import db
from datetime import datetime
from Enums import ResponseMsg
from Enums.baseEnum import BaseEnum
from Utils import MyLog, UUID, pageSerialize, MyTools
from Comment.myException import MyException, ParamException

log = MyLog.get_log(__file__)


class Base(db.Model):
    __abstract__ = True
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid: str = db.Column(db.String(50), index=True, comment="唯一标识")
    create_time: str = db.Column(db.DATETIME, default=datetime.now, comment="创建时间")
    update_time: str = db.Column(db.DATETIME, nullable=True, onupdate=datetime.now, comment="修改时间")

    def save(self, new: bool = True) -> NoReturn:
        """
        save
        :param new 首次录入

        """
        try:
            if new:
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
    def delete_by_id(cls, uid: str) -> NoReturn:
        """
        通过id 删除
        :param    uid: cls。uid
        :raise:   ParamException
        """
        target = cls.get_by_uid(uid)
        target.delete()

    @classmethod
    def update(cls, **kwargs) -> NoReturn:
        """

        通过kwargs.get_by_uid() 获得实例 修改
        """
        from flask import g
        kwargs.setdefault("updater", g.user.id)  # 修改人
        target = cls.get_by_uid(kwargs.pop('uid'))
        c = cls.columns()
        try:
            for k, v in kwargs.items():
                if k in c:
                    setattr(target, k, v)
            target.save(False)
        except Exception as e:
            log.error(repr(e))
            raise ParamException(ResponseMsg.ERROR)

    @classmethod
    def update_by_id(cls, **kwargs) -> NoReturn:
        """

        通过kwargs.get_by_uid() 获得实例 修改
        """
        from flask import g
        kwargs.setdefault("updater", g.user.id)  # 修改人
        target = cls.get(id=kwargs.pop('id'))
        c = cls.columns()
        try:
            for k, v in kwargs.items():
                if k in c:
                    setattr(target, k, v)
            target.save(False)
        except Exception as e:
            log.error(repr(e))
            raise ParamException(ResponseMsg.ERROR)

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
    def get(cls, id: int | str, name: AnyStr = None):
        """
        get entity by id
        :param id: field id
        :param name: field name
        :return: get_or_NoFound
        """
        return cls.query.get_or_NoFound(id, name)

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
            raise ParamException(ResponseMsg.NOT_FOUND)
        return rv

    @classmethod
    def query_by_field(cls, **kwargs):
        """
        通过字段查询
        :param kwargs: cls field
        :return:
        """
        return cls.query.filter_by(**kwargs).all()

    @classmethod
    def get_by_field(cls, **kwargs):
        """
        通过字段查询
        :param kwargs: cls field
        :return:
        """

        rv = cls.query.filter_by(**kwargs).first()
        if not rv:
            raise ParamException(ResponseMsg.NOT_FOUND)
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
    def page(cls, pageSize: int, current: int, sort: Dict = None, **kwargs) -> Pagination:
        """
        paginate
        如果指定sort排序 则走sort  否则 默认 create_time.desc()
        :param pageSize:    pageSize
        :param current:     current
        :param sort:        order_by(sort)  'descend' or "ascend'
        :return:            Pagination
        """
        searchData: List = getSearchData(cls, **kwargs)
        sortList: List = getSortData(cls, sort)
        if sortList:
            items = db.session.query(cls).filter(and_(*searchData)) \
                .order_by(*sortList) \
                .limit(pageSize) \
                .offset((current - 1) * pageSize) \
                .all()
        else:
            items = db.session.query(cls).filter(and_(*searchData)) \
                .order_by(cls.create_time.desc()) \
                .limit(pageSize) \
                .offset((current - 1) * pageSize) \
                .all()
        total = db.session.query(cls).filter(and_(*searchData)).count()
        return Pagination(cls, current, pageSize, total, items)

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
    def search_data(cls, **kwargs) -> List:
        """
        使用原生SQL搜索

        :param kwargs:
        :return:
        """

        param: str = MyTools.kw2str(**kwargs)
        sql = f"select * from {cls.__tablename__} where {param} order by create_time desc"
        log.info(sql)
        res = Base.execute_sql(sql)
        return res

    @classmethod
    def search_by_chemy(cls, **kwargs) -> List:
        """
        使用SQLAlchemy 搜索 create_time 倒叙
        :param kwargs:
        :return:
        """
        searchData: List = getSearchData(cls, **kwargs)
        res = cls.query.filter(or_(*searchData)).order_by(cls.create_time.desc()).all()
        return res


def getSearchData(cls, **kwargs) -> List:
    """
    从对应实体类里获取 数据成列
    :param cls: 目标实体
    :param kwargs:  {name:xxx}
    :return: [] | [cls]
    """
    searchData = []
    if not kwargs:
        return searchData
    for k, v in kwargs.items():
        if hasattr(cls, k):
            searchData.append(getattr(cls, k) == v)
    return searchData


def getSortData(cls, kw: Dict[str, Any] = None) -> List:
    """
    根据关键字段升序或者降序
    :param cls: 目标实体
    :param kw: {id：ascend} | {time：descend}
    :return: [] | [cls]
    """
    sortList = []
    if not kw:
        return sortList
    for k, v in kw.items():
        if v == "descend":
            sortList.append(getattr(cls, k).desc())
        else:
            sortList.append(getattr(cls, k).asc())
    return sortList
