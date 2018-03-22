#!/usr/bin/env python
#coding:utf-8
'''
    @Author:John Wen
    @description:
        
'''

import os

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or "qwe123"

    @staticmethod
    def init_app(self):
        pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://test:qwe123@192.168.232.132/blog?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TEST = True

class ProdConfig(Config):
    pass

config = {
    'dev':DevConfig,
    'test':TestConfig,
    'prod':ProdConfig,
    'default':DevConfig
}