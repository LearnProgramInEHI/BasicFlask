#!/usr/bin/env python
#coding:utf-8
'''
    @Author:John Wen
    @description:
'''

from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from . import login
from flask_login import UserMixin,AnonymousUserMixin
from datetime import datetime
@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__= 'user'
    id = db.Column(db.Integer,primary_key=True)
    location = db.Column(db.String(64))
    member_since = db.Column(db.DateTime(),default =datetime.utcnow)
    last_seen = db.Column(db.DateTime(),default=datetime.utcnow)
    name = db.Column(db.String(64),unique=True,index=True,nullable=False)
    email = db.Column(db.String(128),unique=True,nullable=False)
    description = db.Column(db.String(256))
    password_hash = db.Column(db.String(256))
    role_id = db.Column(db.Integer,db.ForeignKey('role.id'))

    def __init__(self,**kw):
        super(User,self).__init__(**kw)
        if self.role is None:
            # 这里没有验证邮箱，如果以邮箱作为管理员的依据，会产生漏洞。
            if self.email == 'a403481704@163.com':
                self.role = Role.query.filter_by(permission=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def can(self,permission):
        return self.role is not None and (self.role.permission & permission) == permission
    def is_admin(self):
        return self.can(Permissions.ADMINISTER)


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
    permission = db.Column(db.Integer)
    default=db.Column(db.Boolean,default=False,index=True)
    user = db.relationship('User',backref='role')
    def __repr__(self):
        return "<Roel : {}>".format(self.name)

    @staticmethod
    def insert_roles():
        roles = {
            "Usere":(Permissions.FOLLOW|
                     Permissions.COMMENT|
                     Permissions.WRITE_ARTICLE,True),
            "Moderator":(Permissions.FOLLOW|
                         Permissions.COMMENT|
                         Permissions.WRITE_ARTICLE|
                         Permissions.MODERATE_COMMENT,False),
            "Administration":(0xff,False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permission = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

class Permissions():
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLE = 0x04
    MODERATE_COMMENT = 0x08
    ADMINISTER = 0x80

class AnonymousUser(AnonymousUserMixin):
    def can(self,permission):
        return False
    def is_admin(self):
        return False

