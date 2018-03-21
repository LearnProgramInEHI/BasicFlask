#!/usr/bin/env python
#coding:utf-8
'''
    @Author:John Wen
    @description:
        
'''
from flask import Blueprint
auth = Blueprint('auth',__name__,url_prefix='/user')
from . import  views
from ..models import Permissions

@auth.app_context_processor
def inject_permission():
    return dict(Permissions=Permissions)

