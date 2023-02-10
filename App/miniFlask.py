#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023-02-08
# @Author : cyq
# @File : casesHub
# @Software: PyCharm
# @Desc:
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/login", methods=["POST"])
def login():
    return jsonify({"code": 0, "data": "asdasdsa", "msg": "ok"})


@app.route("/query", methods=["GET"])
def query():
    return jsonify({"code": 0, "data": [{"name": "cyq"}, {"name": "dawa"}], "msg": "ok"})


if __name__ == '__main__':
    app.run(port=8080)
