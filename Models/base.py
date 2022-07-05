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
常见的SQLALCHEMY列选项
可选参数    描述
primary_key 如果设置为True，则为该列表的主键
unique  如果设置为True，该列不允许相同值
index   如果设置为True，为该列创建索引，查询效率会更高
nullable    如果设置为True，该列允许为空。如果设置为False，该列不允许空值
default 定义该列的默认值

primary_key	如果设为 True ,这列就是表的主键
unique	如果设为 True ,这列不允许出现重复的值
index	如果设为 True ,为这列创建索引,提升查询效率
nullable	如果设为 True ,这列允许使用空值;如果设为 False ,这列不允许使用空值
default	为这列定义默认值
"""
from App import db
from datetime import datetime


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.Date, default=datetime.now)
    update_time = db.Column(db.Date, default=datetime.now, onupdate=datetime.now)
