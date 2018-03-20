#!/usr/bin/env python
#coding:utf-8
'''
    @Author:John Wen
    @description:
        
'''

from flask import url_for,render_template,redirect,flash,request
from . import auth
from .forms import LoginForm,RegisterForm
from ..models import User
from flask_login import login_user,current_user,logout_user
from werkzeug.urls import url_parse
from .. import db

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

@auth.route('/profile')
def profile():
    return "This is user profile"

@auth.route('/logout')
def logout():
    logout_user()
    flash("You have been logout!! ")
    return redirect(url_for('main.index'))