# @Time : 2022/7/5 21:11 
# @Author : cyq
# @File : projectConfig.py 
# @Software: PyCharm
# @Desc: 项目配置类


"""
SQLALCHEMY_DATABASE_URI 连接数据库。示例：mysql://username:password@host/post/db?charset=utf-8
SQLALCHEMY_BINDS 一个将会绑定多种数据库的字典。 更多详细信息请看官文 绑定多种数据库.
SQLALCHEMY_ECHO 调试设置为true
SQLALCHEMY_POOL_SIZE 数据库池的大小，默认值为5。
SQLALCHEMY_POOL_TIMEOUT 连接超时时间
SQLALCHEMY_POOL_RECYCLE 自动回收连接的秒数。
SQLALCHEMY_MAX_OVERFLOW 控制在连接池达到最大值后可以创建的连接数。当这些额外的 连接回收到连接池后将会被断开和抛弃。
SQLALCHEMY_TRACK_MODIFICATIONS 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
"""
import os
import cx_Oracle as cx

basedir = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ProjectConfig:
    SECRET_KEY = 'hard to guess string'

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST = "127.0.0.1"
    REDIS_PORT = 6379
    MYSQL_PORT = 3306
    ORAClE_PORT = 1521
    MONGODB_PORT = 27017
    MYSQL_DATABASE = 'caseHub'
    MONGODB_DB = 'caseHub'
    FLASK_ADMIN_SWATCH = 'cerulean'

    # FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    # FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    # FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(ProjectConfig):
    DEBUG = True

    CACHE_TYPE = 'simple'
    ERROR_404_HELP = False
    CACHE_DEFAULT_TIMEOUT = 3000
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 123
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    REPORT_MAIL = "xxxx@mail.com"
    JSON_AS_ASCII = False  # 这个配置可以确保http请求返回的json数据中正常显示中文

    # mysql
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@{ProjectConfig.HOST}:{ProjectConfig.MYSQL_PORT}/{ProjectConfig.MYSQL_DATABASE}"

    SQLALCHEMY_BINDS = {"bj": "oracle://SCM:QGVdUD4xjQuO8Grj@10.10.105.110:1521/?service_name=cbsdbt",
                        "hz": "oracle://HZ_SCM:p9bv0h21GMWk40Fy@10.10.105.110:1521/?service_name=cbsdbt",
                        "nj": "oracle://NJ_SCM:p9bv0h21GMWk40Fy@10.10.105.110:1521/?service_name=cbsdbt"
                        }
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis
    RATELIMIT_STORAGE_URI = 'redis://{}:{}/1'.format(ProjectConfig.HOST, ProjectConfig.REDIS_PORT)
    RESULT_BACKEND = 'redis://{}:{}/1'.format(ProjectConfig.HOST, ProjectConfig.REDIS_PORT)
    CELERY_BROKER_URL = 'redis://{}:{}/2'.format(ProjectConfig.HOST, ProjectConfig.REDIS_PORT)

    # mongodb
    MONGODB_SETTINGS = {
        "db": ProjectConfig.MONGODB_DB,
        "host": ProjectConfig.HOST,
        "port": ProjectConfig.MONGODB_PORT
    }
    timezone = 'Asia/Shanghai'
    accept_content = ['json', 'pickle']
    result_serializer = "json"

    # CELERYBEAT_SCHEDULE = {
    #     'import_data': {
    #         'task': 'test_ddd',
    #         'schedule': timedelta(seconds=10)
    #     },
    # }
    #


class TestingConfig(ProjectConfig):
    TESTING = True
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(ProjectConfig):
    pass


config = {
    "dev": DevelopmentConfig,
    "test": TestingConfig,
    "pro": ProjectConfig,
    "default": DevelopmentConfig
}
