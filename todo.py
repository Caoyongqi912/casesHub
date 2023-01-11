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


# 不带声调的(style=pypinyin.NORMAL)
def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s


# 带声调的(默认)
def yinjie(word):
    s = ''
    # heteronym=True开启多音字
    for i in pypinyin.pinyin(word, heteronym=True):
        s = s + ''.join(i) + " "
    return s


if __name__ == "__main__":
    print(pinyin("asdasd"))
    print(yinjie("诗书继世长"))