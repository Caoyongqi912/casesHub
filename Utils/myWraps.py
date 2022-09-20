# @Time : 2022/7/12 21:58
# @Author : cyq
# @File : myWraps.py
# @Software: PyCharm
# @Desc:
from functools import wraps

from Utils.myTools import MyTools


def pageSerialize(func):
    """
    分页序列化装饰器
    :param func: Pagination
    """

    @wraps(func)
    def decorator(cls, *args, **kwargs):
        info = func(cls, *args, **kwargs)
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
    def decorator(self, **kwargs):
        info = func(self, **kwargs)
        results = {
            "items": [{
                "id": i.id,
                "title": i.title,
                "desc": i.desc,
                "creator": i.creator,
                "case_level": i.case_level,
                "create_time": i.create_time,
                "update_time": i.update_time

            } for i in info.items],
            "pageInfo": {
                "total": info.total,
                "pages": info.pages,
                "page": info.page,
                "limit": info.per_page
            }
        }
        return results

    return decorator


def variable2dict(func):
    @wraps(func)
    def decorator(self):
        info = func(self)
        result = [{"key": var.key, "val": var.val} for var in info]
        return MyTools.list2Dict(params=result)

    return decorator

if __name__ == '__main__':
    from datetime import datetime
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))