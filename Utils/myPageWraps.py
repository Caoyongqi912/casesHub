# @Time : 2022/7/12 21:58
# @Author : cyq
# @File : myPageWraps.py
# @Software: PyCharm
# @Desc:
from functools import wraps


def pageSerialize(func):
    """
    分页序列化装饰器
    :param func: Pagination
    """

    @wraps(func)
    def decorator(cls, page, limit, *args):
        info = func(cls, page, limit, *args)
        results = {
            "items": info.items,
            "pageInfo": {
                "total": info.total,
                "pages": info.pages,
                "page": info.page,
                "limit": info.per_page
            }
        }
        return results
    return decorator
