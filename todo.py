#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2023-01-05
# @Author : cyq
# @File : casesHub
# @Software: PyCharm
# @Desc:


"""
log 处理
1、用例运行实时log
2、全局log 定位异常


用户数据
1、用户绑定bug、case、msg。。

fastfds
1、存储备件


baogoa
1、运行后产出报告
2、具体内容
3、简单内容


"""

import pypinyin
import jsonpath

def demo():
    data = {"code":0,"data":"asdasdsa","msg":"ok"}
    jp = "$.d"
    print(jsonpath.jsonpath(data,jp))

if __name__ == '__main__':
    demo()