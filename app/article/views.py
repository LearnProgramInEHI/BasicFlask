#!/usr/bin/env python
#coding:utf-8
'''
    @Author:John Wen
    @description:
        
'''

from . import article
from flask import render_template,redirect,url_for,request,current_app,make_response
from ..models import User,Post,Permissions
from .forms import EditArticleForm
from flask_login import current_user,login_required
from .. import db

@article.route('/<username>')
def article_list(username):
    user = User.query.filter_by(name=username).first()
    query = Post.query.filter_by(user_id=user.id)
    page = request.args.get('page',1,type=int)
    pagination = query.order_by(Post.timestamp.desc()).paginate(page,error_out=False)
    posts = pagination.items
    return render_template('article/self_article.html',posts=posts,pagination=pagination,name=username)


@article.route('/<int:article_id>')
def article_detail(article_id):
    post = Post.query.get_or_404(article_id)
    return render_template('article/article.html',post=post,permissions=Permissions)

@article.route('/edit/<int:article_id>',methods=['GET',"POST"])
@login_required
def edit_article(article_id):
    post = Post.query.filter_by(id=article_id).first()
    form = EditArticleForm()
    if form.validate_on_submit() and current_user.name == post.author.name and current_user.can(Permissions.WRITE_ARTICLE):
        post.name = form.name.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("article.article_detail",article_id=article_id))
    form.name.data = post.name
    form.body.data = post.body
    return render_template('article/edit_article.html',form=form,post=post)

@article.route('/new',methods=["GET","POST"])
@login_required
def new_article():
    form=EditArticleForm()
    if form.validate_on_submit() and current_user.can(Permissions.WRITE_ARTICLE):
        post =Post(name=form.name.data,body=form.body.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("article.article_detail", article_id=post.id))
    return render_template('article/new_article.html',form=form)

@article.route('/delete/<post_id>')
@login_required
def delete_article(post_id):
    post = Post.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("article.article_list",username=current_user.name))
