#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023-02-08
# @Author : cyq
# @File : casesHub
# @Software: PyCharm
# @Desc:
import time

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/login", methods=["POST"])
def login():
    time.sleep(3)
    return jsonify({"code": 0, "data": "im token", "msg": "ok"})


@app.route("/query", methods=["GET"])
def query():
    time.sleep(3)
    return jsonify({"code": 0, "data": [{"name": "cyq"}, {"name": "dawa"}], "msg": "ok"})


if __name__ == '__main__':
    app.run(port=8080)
