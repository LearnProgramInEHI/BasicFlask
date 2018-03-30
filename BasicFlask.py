#!/usr/bin/env python
#coding:utf-8
'''
    @Author:John Wen
    @description:
        
'''
from app import create_app,db
from app.models import User,Role,Permissions,Post
from flask import url_for
import os
from flask_migrate import upgrade,migrate

#from flask_migrate import Migrate

app = create_app('default')
#migrate = Migrate(app,db)
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User,Role=Role,Post=Post,
                Permission=Permissions)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.cli.command()
def deploy():
    db.drop_all()
    db.session.commit()
    #db.create_all()
    migrate()
    upgrade()
    Role.insert_roles()
    User.generate_fake()
    Post.generate_fake()
