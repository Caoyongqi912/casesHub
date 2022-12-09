# @Time : 2022/7/5 21:03 
# @Author : cyq
# @File : __init__.py 
# @Software: PyCharm
# @Desc: 初始化app

from typing import AnyStr
from flask import Flask
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_caching import Cache
from flask_cors import CORS
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from Configs.projectConfig import config
from Models.base_query import MyBaseQuery
from Utils import JSONEncoder
from flask_siwadoc import SiwaDoc
from flask_limiter import Limiter  # https://flask-limiter.readthedocs.io/

catch: Cache = Cache()
db: SQLAlchemy = SQLAlchemy(query_class=MyBaseQuery)
auth: HTTPBasicAuth = HTTPBasicAuth()
# auth: HTTPTokenAuth = HTTPTokenAuth()
siwa = SiwaDoc(title="CaseHubAPI", ui="redoc")
limiter = Limiter(key_func=get_remote_address, strategy="fixed-window")

UID = "uid"


def create_app(configName: AnyStr = "default", printSql: bool = False) -> Flask:
    """
    初始化app
    定义环境配置
    定义中文
    支持跨域
    注册蓝本
    :param printSql: 控制台是否输出sql
    :param configName: projectConfig
    :return: app
    """

    app = Flask(__name__)
    config[configName].SQLALCHEMY_ECHO = printSql
    app.config.from_object(config[configName])
    app.config["BABEL_DEFAULT_LOCALE"] = "zh"
    catch.init_app(app)  # 支持缓存
    db.init_app(app)  # db绑定app
    app.json_encoder = JSONEncoder  # json
    siwa.init_app(app)  # swagger
    limiter.init_app(app)  # 接口频率限制
    CORS(app, supports_credentials=True)

    from .UserController import userBP
    app.register_blueprint(userBP)

    from .ProjectController import proBP
    app.register_blueprint(proBP)

    from .CaseController import caseBP
    app.register_blueprint(caseBP)

    from .reqhook import logWrite, resp
    app.before_request(logWrite)
    app.after_request(resp)
    return app
