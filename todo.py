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

#FayShelbie
import os
import openai
openai.organization = "org-5v8dDJZbk121QxKBznYe2nNC"
openai.api_key = "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"
response = openai.Completion.create(
  model="text-davinci-003",
  prompt="hi",
  temperature=0,
  max_tokens=100,
  top_p=1.0,
  frequency_penalty=0.2,
  presence_penalty=0.0,
  stop=[" Human:", " AI:"]
)
print(response)
