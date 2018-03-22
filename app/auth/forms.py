#!/usr/bin/env python
#coding:utf-8
'''
    @Author:John Wen
    @description:
        
'''

from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Length,Regexp,EqualTo,Email,ValidationError
from ..models import User,Role

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
    localtion = StringField('来自: ',validators=[DataRequired()])
    description = TextAreaField('个性签名:',validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The email address has register. Please login or reset password')

    def validate_username(self,field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('The username already used! ')

class AdminEditUserForm(FlaskForm):
    username = StringField('用户名: ',validators=[DataRequired(),Length(1,64),Regexp('^[a-zA-Z][a-zA-Z0-9]+$',0,'username must have only letters,numbers')])
    email = StringField('邮箱: ',validators=[DataRequired(),Email()])
    description = StringField('个性签名：',validators=[DataRequired()])
    localtion = StringField('来自：',validators=[DataRequired()])
    role =  SelectField('角色：',coerce=int)
    submit = SubmitField('提交')

    def __init__(self,user,**kw):
        super(AdminEditUserForm,self).__init__(**kw)
        self.role.choices = [(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self,field):
        if field.data!=self.user.email and User.query.filter_by(email=field.data).first():
            raise ValidationError('The email address has register. Please login or reset password')

    def validate_username(self,field):
        if field.data!=self.user.name and User.query.filter_by(name=field.data).first():
            raise ValidationError('The username already used! ')
