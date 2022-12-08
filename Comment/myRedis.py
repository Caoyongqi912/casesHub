# @Time : 2022/12/10 13:28
# @Author : cyq
# @File : myRedis.py
# @Software: PyCharm
# @Desc: redis

from redis import Redis
from flask_restful import current_app


class MyRedis:

    def __init__(self):
        # 建立数据库连接
        self.r = Redis(
            host=current_app.config["HOST"],
            port=current_app.config["REDIS_PORT"],
            decode_responses=True  # get() 得到字符串类型的数据
        )

    def handle_redis_token(self, key, value=None, ex=3600 * 24):
        if value:  # 如果value非空，那么就设置key和value，EXPIRE_TIME为过期时间
            self.r.set(key, value, ex=ex)

        else:  # 如果value为空，那么直接通过key从redis中取值
            redis_token = self.r.get(key)
            return redis_token



