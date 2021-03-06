# @Time : 2022/7/12 21:58
# @Author : cyq
# @File : myWraps.py
# @Software: PyCharm
# @Desc:
from functools import wraps


def pageSerialize(func):
    """
    分页序列化装饰器
    :param func: Pagination
    """

    @wraps(func)
    def decorator(cls, page, limit, *args, **kwargs):
        info = func(cls, page, limit, *args, **kwargs)
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


def simpleBug(func):
    """
    指定字段展示bug 并按照ct 排序
    """

    @wraps(func)
    def d(*args, **kwargs):
        bugs = func(*args, **kwargs)
        res = [
            {
                "id": bug.id,
                "title": bug.title,
                "level": bug.level,
                "status": bug.status,
                "create_time": bug.create_time
            } for bug in bugs
        ]
        return res

    return d


def simpleCase(func):
    """
    指定CASE字段返回
    """

    @wraps(func)
    def d(cls, page, limit, by, *args):
        info = func(cls, page, limit, by, *args)
        results = {
            "items": [{
                "id": i.id,
                "title": i.title,
                "desc": i.desc,
                "creator": i.creator,
                "case_level": i.case_level,
                "create_time": i.create_time
            } for i in info.items],
            "pageInfo": {
                "total": info.total,
                "pages": info.pages,
                "page": info.page,
                "limit": info.per_page
            }
        }
        return results

    return d
