# !/usr/bin/env python
#-*- coding:utf-8 -*-

from . import main
from flask import render_template,request
from ..models import Post

@main.route('/')
def index():
    page = request.args.get('page',1,type=int)
    paginate = Post.query.paginate(page,error_out=False)
    posts=paginate.items
    return render_template("main/index.html",posts=posts,paginate=paginate)