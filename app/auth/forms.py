#!/usr/bin/env python
#coding:utf-8
'''
    @Author:John Wen
    @description:
        
'''

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length,Regexp,EqualTo,Email,ValidationError
from ..models import User

class LoginForm(FlaskForm):
    username = StringField('用户名 : ',validators=[DataRequired()])
    password = PasswordField('密码: ',validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class RegisterForm(FlaskForm):
    username = StringField('用户名: ',validators=[DataRequired(),Length(1,64),Regexp('^[a-zA-Z][a-zA-Z0-9]+$',0,'username must have only letters,numbers')])
    password = PasswordField('密码: ',validators=[DataRequired(),EqualTo("password2",message='Password must be matched.')])
    password2 = PasswordField('重新输入密码: ',validators=[DataRequired()])
    email = StringField('邮箱: ',validators=[DataRequired(),Email()])
    description = TextAreaField('个性签名:',validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The email address has register. Please login or reset password')

    def validate_username(self,field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('The username already used! ')





