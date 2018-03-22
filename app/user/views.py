#!/usr/bin/env python
#coding:utf-8
'''
    @Author:John Wen
    @description:
        
'''
from . import user
from app.models import User
from flask import render_template,abort,redirect,url_for
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
