#!/usr/bin/env python
#coding:utf-8
'''
    @Author:John Wen
    @description:
        
'''

from flask import url_for,render_template,redirect,flash,request,abort
from . import auth
from .forms import LoginForm,RegisterForm
from ..models import User,Permissions
from flask_login import login_user,current_user,logout_user,login_required
from werkzeug.urls import url_parse
from .. import db
from ..decoration import permission_required,admin_required

@auth.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is None and not user.check_password(form.password.data):
            flash('Error username or password')
            return redirect(url_for('auth.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc!='':
            next_page =  url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html',form=form)



@auth.route('/register',methods=['GET',"POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        u = User(name=form.username.data,email=form.email.data,description=form.description.data)
        u.get_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('Congratulation! successful')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

@auth.route('/profile/<username>')
def profile(username):
    u = User.query.filter_by(name=username).first()
    if u is None:
        abort(404)
    return render_template('auth/profile.html',user=u)


@auth.route('/logout')
def logout():
    logout_user()
    flash("You have been logout!! ")
    return redirect(url_for('main.index'))

@auth.route('/admin')
@login_required
@admin_required
def for_admin_only():
    return render_template('auth/admin.html')

@auth.route('/moderator')
@login_required
@permission_required(Permissions.MODERATE_COMMENT)
def for_moderate_only():
    return "For moderator only"




