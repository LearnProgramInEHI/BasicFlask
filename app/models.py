#!/usr/bin/env python
#coding:utf-8
'''
    @Author:John Wen
    @description:
'''

from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from . import login
from flask_login import UserMixin
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__= 'user'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True,index=True,nullable=False)
    email = db.Column(db.String(128),unique=True,nullable=False)
    description = db.Column(db.String(256))
    password_hash = db.Column(db.String(256))
    role_id = db.Column(db.Integer,db.ForeignKey('role.id'))

    def __repr__(self):
        return "<User : {}>".format(self.name)

    def get_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

class Role(db.Model):
    __tablename__ ='role'
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True,index=True)
    user = db.relationship('User',backref='role')

    def __repr__(self):
        return "<Roel : {}>".format(self.name)





