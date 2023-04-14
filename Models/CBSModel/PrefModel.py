# @Time : 2023/4/10 21:27 
# @Author : cyq
# @File : PrefModel.py 
# @Software: PyCharm
# @Desc:
from typing import List, Dict, NoReturn

from App import db
from sqlalchemy import Column, INTEGER, CursorResult

from Models.base import Base
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


def get_engine(city: str):
    SQLALCHEMY_BINDS = {"bj": "oracle://SCM:QGVdUD4xjQuO8Grj@10.10.105.110:1521/?service_name=cbsdbt",
                        "hz": "oracle://HZ_SCM:p9bv0h21GMWk40Fy@10.10.105.110:1521/?service_name=cbsdbt",
                        "nj": "oracle://NJ_SCM:p9bv0h21GMWk40Fy@10.10.105.110:1521/?service_name=cbsdbt"
                        }
    return create_engine(SQLALCHEMY_BINDS[city])


class RrefSettingModel(Base):
    __tablename__ = "PERF_MAINT_SETINFO"
    __bind_key__ = None
    id = None
    uid = None
    create_time = None
    update_time = None

    SET_INFO_ID = Column(INTEGER, primary_key=True, comment="主键")
    CORP_ID = Column(INTEGER, nullable=True, comment="法人公司id")
    BEGEARGEAR_SWITCH = Column(INTEGER, comment="偏离度档位开关")
    STATUS = Column(INTEGER, comment="状态1:待执行;2:执行中;3:无效")
    COMPANYID = Column(INTEGER, comment="公司id")
    ENABLED_STATUS = Column(INTEGER, comment="是否启用状态 1:启用 2:未启用")
    CALPERCENTWAY = Column(INTEGER, comment="计算比例得方式1默认比例 2计算比例")
    PARKINGORAUCTION = Column(INTEGER, comment="用途为车位或者法拍时是否产生维护人业绩（1：是 2：否）")
    USERLEAVE = Column(INTEGER, comment="维护人离职业绩处理 1：充公  2：给成交人")
    MAINTAINTOTAL = Column(INTEGER, comment="房源维护总分房源维护总分")
    HOUSECHECKOPTIONS = Column(INTEGER, comment="是否勾选了房源考核项  1：是  2：否")
    COUNTSTANDARD = Column(INTEGER, comment="计算基准（1：低价 2：对外报价）'")
    COUNTSTANDARDHOURS = Column(INTEGER, comment="价格取值时间")
    HOUSESCOREGETPERF = Column(INTEGER, comment="房源分达标分业绩比例百分比")
    BARGADEVGEARGETPERF = Column(INTEGER, comment="溢价偏离度达标分业绩比例")
    ADDHOUSETIMEFLAG = Column(INTEGER, comment="是否启用房源计算维护业绩的录入时间 1：启用 2：不启用")
    MAINTAINTOTALFLAG = Column(INTEGER, comment="是否启用房源维护总分 1：是  2：否")
    COUNTSTANDARDFLAG = Column(INTEGER, comment="是否启用计算基准价 1：启用 2：不启用")
    DEALBEFORE_TIMEFLAG = Column(INTEGER, comment="是否启用 报成交前（）小时维护人 1：是 2：否")
    ARGUEHOUSEINPUTFLAG = Column(INTEGER,
                                 comment="是否启用议价偏离度生成维护业绩需要满足房源录入时间是在成交（）小时 1：是 2：否")
    ARGUEHOUSEINPUT = Column(INTEGER, comment="议价偏离度生成维护业绩需要满足房源录入时间是在成交（）小时前")

    MAINTSCOREHOUSEINPUTFLAG = Column(INTEGER,
                                      comment="是否启用 维护分生成维护业绩需要满足房源录入时间在成交前（）小时 1：是  2：否")
    MAINTSCOREHOUSEINPUT = Column(INTEGER, comment="维护分生成维护业绩需要满足房源录入时间是成交（）小时前")
    SIGNTODEALHOURSFLAG = Column(INTEGER, comment="是否启用了录入到成交不足（）小时维护人逻辑")
    SIGNTODEALHOURS = Column(INTEGER, comment="录入到报成交不足（）小时维护人逻辑")
    MAINTCHOOSE = Column(INTEGER,
                         comment="录入到报成交不足（）小时后维护人取值范围1：录入后首次生成的维护人  2：成交时维护人")
    DEPTID = Column(INTEGER, comment="部门id")
    BUSINESSTYPE = Column(INTEGER, comment="业务类型 1：租赁 2：买卖")
    DEALBEFOREHOURS = Column(INTEGER, comment="报成交前（）小时维护人")

    def __repr__(self):
        return f"<{RrefSettingModel.__name__}>"

    @staticmethod
    def get_all(city: str):
        engine = get_engine(city)
        session = scoped_session(sessionmaker(bind=engine))
        entities = session.query(RrefSettingModel).all()
        session.close()

        return entities

    @staticmethod
    def update(cls, city, SET_INFO_ID, **kwargs) -> NoReturn:
        engine = get_engine(city)
        session = scoped_session(sessionmaker(bind=engine))
        entity = session.query(RrefSettingModel).filter(RrefSettingModel.SET_INFO_ID == SET_INFO_ID).first()
        if entity is None:
            raise ValueError(f'Entity with id={SET_INFO_ID} not found')
        for k, v in kwargs.items():
            if k in cls.columns():
                setattr(entity, k, v)
        session.add(entity)
        session.commit()
        session.close()


"""

Data Source: HZ_CBS Schema: HZ_SCM Table: PERF_MAINT_SETINFO  -- 维护人设置信息表 
-- auto-generated definition
create table PERF_MAINT_SETINFO
(
    SET_INFO_ID                NUMBER not null,
    CORP_ID                    NUMBER not null,
    PROXY_UPLOAD_SWITCH        NUMBER not null,
    PROXY_UPLOAD_TIME          NUMBER,
    ADDHOUSE_TIME_SWITCH       NUMBER,
    ADDHOUSE_TIME              NUMBER,
    DEALBEFORE_TIME_SWITCH     NUMBER,
    DEALBEFORE_TIME            NUMBER,
    HOUSEEVAL_SWITCH           NUMBER,
    HOUSEEVAL_NSALE_EXCEED     NUMBER,
    HOUSEEVAL_SALE_RECALL_DEAL NUMBER,
    BEGEARGEAR_SWITCH          NUMBER,
    CREATE_BY                  NUMBER,
    CREATE_TIME                TIMESTAMP(6),
    UPDATE_BY                  NUMBER,
    UPDATE_TIME                TIMESTAMP(6),
    REMARK                     VARCHAR2(255),
    ENDDATE                    TIMESTAMP(6),
    STATUS                     NUMBER,
    STARTDATE                  TIMESTAMP(6),
    COMPANYID                  NUMBER,
    ENABLED_STATUS             NUMBER,
    CALPERCENTWAY              NUMBER(30),
    PARKINGORAUCTION           NUMBER,
    USERLEAVE                  NUMBER,
    SIDESCHECK                 NUMBER,
    MAINTAINTOTAL              NUMBER,
    HOUSECHECKOPTIONS          NUMBER,
    COUNTSTANDARD              NUMBER,
    COUNTSTANDARDHOURS         NUMBER,
    HOUSESCOREGETPERF          NUMBER,
    BARGADEVGEARGETPERF        NUMBER,
    SIDESCHECKFLAG             NUMBER,
    ADDHOUSETIMEFLAG           NUMBER,
    MAINTAINTOTALFLAG          NUMBER,
    COUNTSTANDARDFLAG          NUMBER,
    DEALBEFORE_TIMEFLAG        NUMBER,
    ARGUEHOUSEINPUTFLAG        NUMBER,
    ARGUEHOUSEINPUT            NUMBER,
    MAINTSCOREHOUSEINPUTFLAG   NUMBER,
    MAINTSCOREHOUSEINPUT       NUMBER,
    SIGNTODEALHOURSFLAG        NUMBER,
    SIGNTODEALHOURS            NUMBER,
    FIRSTMAINTBYINPUT          NUMBER,
    DEALMAINT                  NUMBER,
    MAINTCHOOSE                NUMBER,
    DEPTID                     NUMBER,
    DEPTLEVEL                  NUMBER,
    BUSINESSTYPE               NUMBER,
    DEALBEFOREHOURS            NUMBER,
    VALUE_NODE                 NUMBER
)

comment on column PERF_MAINT_SETINFO.CORP_ID is '法人公司id'
comment on column PERF_MAINT_SETINFO.BEGEARGEAR_SWITCH is '偏离度档位开关'
comment on column PERF_MAINT_SETINFO.STATUS is '状态1:待执行;2:执行中;3:无效'
comment on column PERF_MAINT_SETINFO.COMPANYID is '公司id'
comment on column PERF_MAINT_SETINFO.ENABLED_STATUS is '是否启用状态 1:启用 2:未启用'
comment on column PERF_MAINT_SETINFO.CALPERCENTWAY is '计算比例得方式1默认比例 2计算比例'
comment on column PERF_MAINT_SETINFO.PARKINGORAUCTION is '用途为车位或者法拍时是否产生维护人业绩（1：是 2：否）'
comment on column PERF_MAINT_SETINFO.USERLEAVE is '维护人离职业绩处理 1：充公  2：给成交人'
comment on column PERF_MAINT_SETINFO.MAINTAINTOTAL is '房源维护总分'
comment on column PERF_MAINT_SETINFO.HOUSECHECKOPTIONS is '是否勾选了房源考核项  1：是  2：否'
comment on column PERF_MAINT_SETINFO.COUNTSTANDARD is '计算基准（1：低价 2：对外报价）'
comment on column PERF_MAINT_SETINFO.COUNTSTANDARDHOURS is '价格取值时间'
comment on column PERF_MAINT_SETINFO.HOUSESCOREGETPERF is '房源分达标分业绩比例百分比'
comment on column PERF_MAINT_SETINFO.BARGADEVGEARGETPERF is '溢价偏离度达标分业绩比例'
comment on column PERF_MAINT_SETINFO.ADDHOUSETIMEFLAG is '是否启用房源计算维护业绩的录入时间 1：启用 2：不启用'
comment on column PERF_MAINT_SETINFO.MAINTAINTOTALFLAG is '是否启用房源维护总分 1：是  2：否'
comment on column PERF_MAINT_SETINFO.COUNTSTANDARDFLAG is '是否启用计算基准价 1：启用 2：不启用'
comment on column PERF_MAINT_SETINFO.DEALBEFORE_TIMEFLAG is '是否启用 报成交前（）小时维护人 1：是 2：否'
comment on column PERF_MAINT_SETINFO.ARGUEHOUSEINPUTFLAG is '是否启用议价偏离度生成维护业绩需要满足房源录入时间是在成交（）小时 1：是 2：否'
comment on column PERF_MAINT_SETINFO.ARGUEHOUSEINPUT is '议价偏离度生成维护业绩需要满足房源录入时间是在成交（）小时前'
comment on column PERF_MAINT_SETINFO.MAINTSCOREHOUSEINPUTFLAG is '是否启用 维护分生成维护业绩需要满足房源录入时间在成交前（）小时 1：是  2：否'
comment on column PERF_MAINT_SETINFO.MAINTSCOREHOUSEINPUT is '维护分生成维护业绩需要满足房源录入时间是成交（）小时前'
comment on column PERF_MAINT_SETINFO.SIGNTODEALHOURSFLAG is '是否启用了录入到成交不足（）小时维护人逻辑'
comment on column PERF_MAINT_SETINFO.SIGNTODEALHOURS is '录入到报成交不足（）小时维护人逻辑'
comment on column PERF_MAINT_SETINFO.MAINTCHOOSE is '录入到报成交不足（）小时后维护人取值范围1：录入后首次生成的维护人  2：成交时维护人'
comment on column PERF_MAINT_SETINFO.DEPTID is '部门id'
comment on column PERF_MAINT_SETINFO.BUSINESSTYPE is '业务类型 1：租赁 2：买卖'
comment on column PERF_MAINT_SETINFO.DEALBEFOREHOURS is '报成交前（）小时维护人'
comment on column PERF_MAINT_SETINFO.VALUE_NODE is '议价偏离度取值节点(1-报意向,2-报成交)'
/
 Show table preview """
