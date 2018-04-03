#!/usr/bin/env python
#coding:utf-8
# @Time       : 3/30/2018 4:11 PM
# @Author     : johnw
# @Modified   : 3/30/2018 4:11 PM
# @Software   : PyCharm Community Edition


from flask import Blueprint
api = Blueprint('api',__name__,url_prefix='/api/v1.0')

from . import auth, posts, users, comments, errors