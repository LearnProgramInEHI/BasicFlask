#!/usr/bin/env python
#coding:utf-8
'''
    @Author:John Wen
    @description:
        
'''

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField,TextAreaField,SubmitField

class EditArticleForm(FlaskForm):
    name = StringField('文章标题',validators=[DataRequired()])
    body = TextAreaField("文章内容",validators=[DataRequired()])
    submit = SubmitField('提交')


