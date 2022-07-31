# @Time : 2022/7/31 15:25 
# @Author : cyq
# @File : myUid.py 
# @Software: PyCharm
# @Desc:


from faker import Faker


class UUID:
    @property
    def getUId(self):
        f = Faker()
        return f.pystr()
