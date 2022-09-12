# @Time : 2022/9/12 19:09 
# @Author : cyq
# @File : tasks.py 
# @Software: PyCharm
# @Desc:
from Utils import MyLog
from App import create_app, celery
import time

log = MyLog.get_log(__file__)

app = create_app()
app.app_context().push()


@celery.task()
def add(x, y):
    for i in range(10):
        time.sleep(1)
        log.info(i)

    return str(x + y)
