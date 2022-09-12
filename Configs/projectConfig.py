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

basedir = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ProjectConfig:
    SECRET_KEY = 'hard to guess string'

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST = "127.0.0.1"
    redisPort = '6379'

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
    CACHE_DEFAULT_TIMEOUT = 300
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 123
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    REPORT_MAIL = "xxxx@mail.com"
    JSON_AS_ASCII = False  # 这个配置可以确保http请求返回的json数据中正常显示中文

    #    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/caseHub"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    CELERY_RESULT_BACKEND = 'redis://{}:{}'.format(ProjectConfig.HOST, ProjectConfig.redisPort)
    CELERY_BROKER_URL = 'redis://{}:{}'.format(ProjectConfig.HOST, ProjectConfig.redisPort)
    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_ACCEPT_CONTENT = ['json', 'pickle']
    CELERY_RESULT_SERIALIZER = "json"

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
if __name__ == '__main__':
    print(basedir)
