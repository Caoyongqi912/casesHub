#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023-01-04
# @Author : cyq
# @File : casesHub
# @Software: PyCharm
# @Desc:
from typing import Any

from App import mg

class FileDB(mg.Document):
    name = mg.StringField(required=True)
    file = mg.FileField()
    type = mg.StringField(required=True)

