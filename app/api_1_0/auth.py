#!/usr/bin/env python
# coding:utf-8
# author : w0xffff
# date   : 2018/4/2 21:15
# IDE    : PyCharm

from flask_httpauth import HTTPBasicAuth
from app.models import AnonymousUser,User
from . import api
from flask import g
from .errors import forbidden,unauthorized
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(name_or_token,password):
    if name_or_token == '':
        g.current_user = AnonymousUser()
        return True

    if password == "":
        g.current_user = User.verify_auth_token(name_or_token)
        g.token_used = True
        return g.current_user is not None

    user = User.query.filter_by(name=name_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')

from .errors import forbidden
@api.before_request
@auth.login_required
def before_requests():
    if not g.current_user.is_anonymous:
        return forbidden("Unlogin account")
@api.route("/token")
def get_token():
    if g.current_user.is_anonymous:
        return