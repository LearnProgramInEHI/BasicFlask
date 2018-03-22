#!/usr/bin/env python
#coding:utf-8
'''
    @Author:John Wen
    @description:
        
'''
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

class EditForm(FlaskForm):
    name = StringField('用户名:', validators=[DataRequired(message="必填！！")])
    localtion = StringField('来自:', validators=[DataRequired(message="必填！！")])
    description = StringField('个性签名:', validators=[DataRequired(message="必填！！")])
    submit = SubmitField('提交')






