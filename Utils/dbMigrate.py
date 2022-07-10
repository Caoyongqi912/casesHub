# @Time : 2022/7/9 14:06 
# @Author : cyq
# @File : dbMigrate.py 
# @Software: PyCharm
# @Desc:

from App import create_app,db
from Models.UserModel import users,departments


if __name__ == '__main__':
    create_app().app_context().push()
    db.create_all()