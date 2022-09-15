# @Time : 2022/9/12 19:57 
# @Author : cyq
# @File : myCelery.py 
# @Software: PyCharm
# @Desc:

from celery import Celery
from flask import Flask


def create_celery_app(app: Flask) -> Celery:
    celery = Celery(app.import_name, broker=app.config["CELERY_BROKER_URL"],
                    backend=app.config['RESULT_BACKEND'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super().__call__(*args, **kwargs)

    celery.Task = ContextTask
    return celery
