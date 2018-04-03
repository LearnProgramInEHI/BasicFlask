#!/usr/bin/env python
#coding:utf-8
# @Time       : 3/30/2018 4:17 PM
# @Author     : johnw
# @Modified   : 3/30/2018 4:17 PM
# @Software   : PyCharm Community Edition
from flask import jsonify
from . import api

def forbidden(message):
    response = jsonify({'error':'forbidden','message':message})
    response.status_code = 403
    return response


def unauthorized(message):
    response = jsonify({ "error":"unauthorized",'message':message})
    response.status_code = 401
    return response

def bad_request(message):
    response = jsonify({"error":'bad request',"message":message})
    response.status_code = 400
    return response


