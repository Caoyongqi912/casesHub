# @Time : 2022/7/12 21:41 
# @Author : cyq
# @File : myJsonSerialize.py
# @Software: PyCharm
# @Desc:
import decimal
from datetime import datetime
from flask.json import JSONEncoder as BaseJSONEncoder


class JSONEncoder(BaseJSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(o, decimal.Decimal):
            return float(o)
        from Models.base import Base
        if isinstance(o, Base):
            return o.to_json(o)
        return super(JSONEncoder, self).default(o)

