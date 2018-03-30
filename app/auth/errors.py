#!/usr/bin/env python
#coding:utf-8
# @Time       : 3/28/2018 11:20 AM
# @Author     : johnw
# @Modified   : 3/28/2018 11:20 AM
# @Software   : PyCharm Community Edition

from . import auth

@auth.app_errorhandler
def File_not_found():
    pass

