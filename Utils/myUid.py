# @Time : 2022/7/31 15:25 
# @Author : cyq
# @File : myUid.py 
# @Software: PyCharm
# @Desc:
import hashlib
import time

from faker import Faker

class UUID:
    @property
    def getUId(self):
        f = Faker()
        return f.pystr()

    @property
    def getUUID(self):
        timestamp = str(int(time.time()))
        # 对字符串进行 MD5 加密
        md5hash = hashlib.md5(timestamp.encode('utf-8')).hexdigest()
        return md5hash
