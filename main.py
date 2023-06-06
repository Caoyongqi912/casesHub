#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023-06-01
# @Author : cyq
# @File : casesHub
# @Software: PyCharm
# @Desc:

import gevent.monkey

gevent.monkey.patch_all()

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from App import create_app, io

app = create_app()
if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
    # io.run(app, host="127.0.0.1", port=5000, debug=True)
