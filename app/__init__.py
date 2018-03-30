#!/usr/bin/env python
#coding:utf-8
'''
    @Author:John Wen
    @description:
        
'''

from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
db = SQLAlchemy(use_native_unicode='utf8')
migrate = Migrate()
login = LoginManager()
login.session_protection = 'strong'
login.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    migrate.init_app(app,db)
    login.init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    from app.article import article as article_blueprint
    app.register_blueprint(article_blueprint)

    from app.api_1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint)


    return app


