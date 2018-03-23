#!/usr/bin/env python
#coding:utf-8
'''
    @Author:John Wen
    @description:
        
'''
from flask import Blueprint
article = Blueprint('article',__name__,url_prefix='/article')

from . import views
