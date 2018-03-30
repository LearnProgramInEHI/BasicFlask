#!/usr/bin/env python
#coding:utf-8
'''
    @Author:John Wen
    @description:
        
'''
from . import user
from app.models import User
from flask import render_template,abort,redirect,url_for,flash,request
from .forms import EditForm
from flask_login import current_user,login_required
from app import db

@user.route('/profile/<username>')
def profile(username):
    u = User.query.filter_by(name=username).first()
    if u is None:
        abort(404)
    return render_template('user/profile.html',user=u)

@user.route('/edit-profile',methods=["GET","POST"])
@login_required
def edit_profile():
    form = EditForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.localtion.data
        current_user.description = form.description.data
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('user.profile',username=current_user.name))

    form.name.data = current_user.name
    form.localtion.data = current_user.location
    form.description.data = current_user.description
    return render_template('user/editprofile.html',form=form)

@user.route("/follow/<username>")
@login_required
def follow(username):
    u = User.query.filter_by(name=username).first()
    if u!=current_user and u is not None and not current_user.is_following(u):
        current_user.follow(u)
    return redirect(url_for('user.profile',username=u.name))

@user.route('/unfollow/<username>')
@login_required
def unfollow(username):
    u = User.query.filter_by(name=username).first()
    if u != current_user and u is not None and current_user.is_following(u):
        current_user.unfollow(u)
    return redirect(url_for('user.profile',username=u.name))


@user.route("/followers/<username>")
def followers(username):
    u = User.query.filter_by(name=username).first()
    if u is None:
        flash('Invalid user')
        return redirect(url_for("user.profile",username=current_user.name))
    page = request.args.get('page',1,type=int)
    pagination = u.followers.paginate(page,per_page=10,error_out=False)
    follows = [{'user':item.follower,'timestamp':item.timestamp} for item in pagination.items]
    return render_template('user/followers.html',user=u,endpoint='user.followers',pagination=pagination,follows=follows)

@user.route('/followed')
def followed():
    pass

