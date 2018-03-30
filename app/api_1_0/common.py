#!/usr/bin/env python
#coding:utf-8
# @Time       : 3/30/2018 5:19 PM
# @Author     : johnw
# @Modified   : 3/30/2018 5:19 PM
# @Software   : PyCharm Community Edition

def trueReturn(data,msg):
    return {
        "status":True,
        "data":data,
        "msg":msg
    }

def falseRturn(data,msg):
    return {
        "status":False,
        "data":data,
        "msg":msg
    }
