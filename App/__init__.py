# @Time : 2022/7/5 21:03 
# @Author : cyq
# @File : __init__.py 
# @Software: PyCharm
# @Desc: 初始化app

from typing import AnyStr
from flask import Flask
from flask_httpauth import HTTPBasicAuth
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
siwa = SiwaDoc(title="CaseHubAPI", ui="redoc")
limiter = Limiter(key_func=get_remote_address, strategy="fixed-window")


def create_app(configName: AnyStr = "default") -> Flask:
    """
    初始化app
    定义环境配置
    定义中文
    支持跨域
    注册蓝本
    :param configName: projectConfig
    :return: app
    """

    app = Flask(__name__)
    app.config.from_object(config[configName])
    app.config["BABEL_DEFAULT_LOCALE"] = "zh"
    catch.init_app(app)  # 支持缓存
    db.init_app(app)  # db绑定app
    app.json_encoder = JSONEncoder  # json
    siwa.init_app(app)  # swagger
    limiter.init_app(app)  # 接口频率限制
    CORS(app, supports_credentials=True)

    from .DepartController import userBP
    app.register_blueprint(userBP)

    from .ProjectController import proBP
    app.register_blueprint(proBP)

    from .CaseController import caseBP
    app.register_blueprint(caseBP)

    from .PlatformController import platformBP
    app.register_blueprint(platformBP)

    from .UploadController import fileBP
    app.register_blueprint(fileBP)

    from .reqhook import logWrite, resp
    app.before_request(logWrite)
    app.after_request(resp)
    return app
