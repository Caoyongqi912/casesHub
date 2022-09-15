# @Time : 2022/9/12 19:09 
# @Author : cyq
# @File : tasks.py 
# @Software: PyCharm
# @Desc:
from Utils import MyLog
from App import create_app, celery

log = MyLog.get_log(__file__)



@celery.task()
def caseExcelWrite2Sql(projectID: int, creator: int, filePath: str):
    from Utils.myExcel import MyExcel
    my = MyExcel(file_path=filePath)
    my.sheetReader(projectID, creator)
