#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023-06-01
# @Author : cyq
# @File : casesHub
# @Software: PyCharm
# @Desc:


from flask_socketio import SocketIO

socketIO = SocketIO(cors_allowed_origins='*', async_mode="gevent")
