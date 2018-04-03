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
import bleach
from itsdangerous import Serializer
from flask import current_app


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Follow(db.Model):
    follower_id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True)
    followed_id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)

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
    posts = db.relationship('Post',backref='author',lazy='dynamic')
    followed = db.relationship('Follow',foreign_keys=[Follow.follower_id],backref=db.backref('follower',lazy='joined'),
                               lazy='dynamic',
                               cascade = 'all,delete-orphan')
    followers = db.relationship('Follow',foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed',lazy='joined'),
                                lazy='dynamic',
                                cascade='all,delete-orphan')

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

    def generate_auth_token(self,expiration):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
        return s.dumps({'id':self.id})
    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            datas = s.loads(token)
        except:
            return None
        return User.query.get(datas['id'])

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py
        seed()
        for i in range(count):
            u = User(name=forgery_py.internet.user_name(True),
                     email=forgery_py.internet.email_address(),
                     location=forgery_py.address.city(),
                     description=forgery_py.lorem_ipsum.sentence(),
                     member_since=forgery_py.date.date(True))
            u.get_password('qwe123')
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def can(self,permission):
        return self.role is not None and (self.role.permission & permission) == permission
    def is_admin(self):
        return self.can(Permissions.ADMINISTER)

    def follow(self,user):
        if not self.is_following(user):
            f = Follow(follower=self,followed=user)
            db.session.add(f)
            db.session.commit()

    def unfollow(self,user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)
            db.session.commit()

    def is_following(self,user):
        return self.followed.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self,user):
        return self.followers.filter_by(follower_id=user.id).first() is not None

    @property
    def followed_posts(self):
        return Post.query.join(Follow, Follow.followed_id == Post.user_id).filter(Follow.follower_id == self.id)

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

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128),index=True)
    body = db.Column(db.Text())
    body_html = db.Column(db.Text())
    timestamp = db.Column(db.DateTime(),default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return "<Post:{}>".format(self.name)
    @staticmethod
    def on_changed_body(target,value,oldvalue,initiator):
        allowed_tags = [
            'a','abbr','acronym','b','blockquote','code','em','i','li',
            'ol','strong','ul','h1','h2','h3','p','pre','span','img','table','tr','td','th','thead','tbody'
        ]
        attrs = {
            "*":['style']
        }
        styles = ['color','font-weight','font-style','text-decoration-line','background-color','border','width','cellpadding','cellspacing']
        target.body_html = bleach.clean(value,tags=allowed_tags,strip=True, attributes=attrs,styles=styles)

    @staticmethod
    def generate_fake(count=100):
        from random import seed,randint
        import forgery_py
        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0,user_count-1)).first()
            p = Post(name=forgery_py.lorem_ipsum.word(),
                     body=forgery_py.lorem_ipsum.sentences(randint(1,99)),
                     timestamp=forgery_py.date.date(True),
                     author=u)
            db.session.add(p)
            db.session.commit()


db.event.listen(Post.body, 'set', Post.on_changed_body)
login.anonymous_user = AnonymousUser



