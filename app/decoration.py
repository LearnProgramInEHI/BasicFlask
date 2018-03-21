#!/usr/bin/env python
#coding:utf-8
'''
    @Author:John Wen
    @description:
        
'''
from flask import abort
from .models import Permissions
from functools import wraps
from flask_login import current_user
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decoration_func(*args,**kw):
            if not current_user.can(permission):
                abort(403)
            return f(*args,**kw)
        return decoration_func
    return decorator

def admin_required(f):
    return permission_required(Permissions.ADMINISTER)(f)



