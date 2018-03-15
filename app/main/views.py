# !/usr/bin/env python
#-*- coding:utf-8 -*-

from . import main

@main.route('/')
def main():
    return "<h1>Hello World</h1>"