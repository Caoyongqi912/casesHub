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
from flask_sqlalchemy import SQLAlchemy
from Configs.projectConfig import config
from Models.base_query import BaseQuery

catch = Cache()
db = SQLAlchemy(query_class=BaseQuery)
auth = HTTPBasicAuth()


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

    CORS(app, supports_credentials=True)

    from .departmentController import userBP
    app.register_blueprint(userBP)

    from .indexController import indexPB
    app.register_blueprint(indexPB)

    return app
