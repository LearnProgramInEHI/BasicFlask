#!/usr/bin/env python
#coding:utf-8
# @Time       : 3/30/2018 4:20 PM
# @Author     : johnw
# @Modified   : 3/30/2018 4:20 PM
# @Software   : PyCharm Community Edition
# http://www.thatyou.cn/flask-pyjwt-%E5%AE%9E%E7%8E%B0%E5%9F%BA%E4%BA%8Ejson-web-token%E7%9A%84%E7%94%A8%E6%88%B7%E8%AE%A4%E8%AF%81%E6%8E%88%E6%9D%83/
from functools import wraps
from flask import request
from .common import trueReturn,falseRturn
from datetime import datetime,timedelta
import jwt
from config import Config
class Auth():
    @staticmethod
    def decode_auth_token(auth_token):
        pass

    @staticmethod
    def encode_auth_token(user_id,login_time):
        try:
            payload = {
                'exp': datetime.utcnow()+ timedelta(days=0,seconds=10),
                'iat': datetime.utcnow(),
                'iss':'ken',
                'data':{
                    id:user_id,
                    'login_time':login_time
                }
            }
            return jwt.encode(
                payload,
                Config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            pass


    def login_required(self,f):
        @wraps(f)
        def decorated(*args,**kwargs):
            auth_header = request.headers.get("Authorization")
            if auth_header:
                auth_tokenArr = auth_header.split(" ")
                if not auth_tokenArr or auth_tokenArr[0] != 'JWT' or len(auth_tokenArr)!=2:
                    result = falseRturn('','请传递正确的验证头信息。')
                else:
                    auth_tokenArr = auth_tokenArr[1]


