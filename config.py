#!/usr/bin/env python
#coding:utf-8
'''
    @Author:John Wen
    @description:
        
'''

import os



class Config():
    SECERT_KEY = os.environ.get('SECRET_KEY')

    @staticmethod
    def init_app(self):
        pass


class DevConfig():
    DEBUG = True

class TestConfig():
    TEST = True

class ProdConfig():
    pass

config = {
    'dev':DevConfig,
    'test':TestConfig,
    'prod':ProdConfig,
    'default':DevConfig
}