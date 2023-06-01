#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023-06-01
# @Author : cyq
# @File : casesHub
# @Software: PyCharm
# @Desc:

import gevent.monkey
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from App import create_app
from App.mySocket import socketIO

gevent.monkey.patch_all()
app = create_app()
if __name__ == '__main__':
    # 定义 WSGI 中间件
    dispatcher = DispatcherMiddleware(app, {'/socket.io': socketIO})
    # 定义 Gunicorn 服务器使用的 handler
    handler_class = WebSocketHandler
    # 启动 Gunicorn 服务器
    http_server = WSGIServer(('127.0.0.1', 5000), dispatcher, handler_class=handler_class)
    http_server.serve_forever()
