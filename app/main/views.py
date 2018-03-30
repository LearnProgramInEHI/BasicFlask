# !/usr/bin/env python
#-*- coding:utf-8 -*-

from . import main
from flask import render_template,request,make_response,redirect,url_for
from ..models import Post
from flask_login import current_user,login_required
@main.route('/')
def index():
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed', ''))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
    page = request.args.get('page',1,type=int)
    paginate = query.paginate(page,error_out=False)
    posts=paginate.items
    return render_template("main/index.html",posts=posts,paginate=paginate)

@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('main.index')))
    resp.set_cookie('show_followed','',max_age=30*24*60*60)
    return resp

@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('main.index')))
    resp.set_cookie('show_followed','1',max_age=30*24*60*60)
    return resp