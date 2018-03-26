#!/usr/bin/env python
#coding:utf-8
'''
    @Author:John Wen
    @description:
        先留着，不用

'''

from .widgets import DivArea
from wtforms import TextAreaField

class DivField(TextAreaField):
    widget = DivArea()
