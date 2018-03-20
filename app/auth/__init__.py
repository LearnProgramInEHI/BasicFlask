#!/usr/bin/env python
#coding:utf-8
'''
    @Author:John Wen
    @description:
        
'''
from flask import Blueprint
auth = Blueprint('auth',__name__,url_prefix='/admin')
from . import  views



