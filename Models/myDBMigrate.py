# @Time : 2022/7/9 14:06 
# @Author : cyq
# @File : myDBMigrate.py
# @Software: PyCharm
# @Desc:
from App import create_app, db
if __name__ == '__main__':
    create_app(printSql=True).app_context().push()
    db.create_all()
