# @Time : 2022/9/12 19:09 
# @Author : cyq
# @File : tasks.py 
# @Software: PyCharm
# @Desc:
from App import create_app
from App.myCelery import create_celery_app

celery = create_celery_app(create_app())


# celery_cmd = "celery -A celery_task.tasks:celery worker -l info -P eventlet -E"



@celery.task
def caseExcelWrite2Sql(projectID: int, creator: int, filePath: str):
    from Utils.myExcel import MyExcel
    my = MyExcel(file_path=filePath)
    my.sheetReader(projectID, creator)
