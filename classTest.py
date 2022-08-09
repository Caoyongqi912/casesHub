# @Time : 2022/7/15 20:10 
# @Author : cyq
# @File : classTest.py 
# @Software: PyCharm
# @Desc:
import json
import re
from typing import List


class Test:
    name = "cyq"
    desc = "desc"

    # def __str__(self):
    #     return json.dumps({"name": self.name,
    #                        "desc": self.desc})
    #
    # def __setattr__(self, key, value):
    #     self.__dict__[key] = "set + " + value
    #     print(self.__dict__)

    def search(self, nums: List[int], target: int) -> int:
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

    def test(self,a,b,c=None):
        print("PL")
if __name__ == '__main__':
    A = {"a":1,"b":2}
    Test().test(**A)