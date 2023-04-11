#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023-04-11
# @Author : cyq
# @File : casesHub
# @Software: PyCharm
# @Desc:


from flask import Blueprint

cbsBP = Blueprint("cbsBP", __name__, url_prefix="/api/cbs")
from . import PerfController
