# -*- coding: utf-8 -*-
# @Time     : 2018/8/22 16:28
# @Author   : ChangJun
# @Email    : 52chinaweb@gmail.com
# @Function ：token验证拦截器
from collections import namedtuple

from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth, MultiAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from app.libs.error_code import AuthFailed, Forbidden
from app.libs.scope import is_in_scope

auth = HTTPBasicAuth()
User = namedtuple('User', ['uid', 'scope'])


@auth.verify_password
def verify_password(token, password):
    """ HTTPBasicAuth
            header key:value
            key = Authorization
            value = basic base64(ChangJun:123456)
            通过HTTPBasicAuth的方式获取token
    """
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        g.user = user_info
        return True


def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    """验证token
       首先需要序列化解密token
       捕捉错误异常
       如果BadSignature表示token是无效的
       如果SignatureExpired表示token是过期的
    """
    try:
        """ 解密token """
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg='token是不合法的',
                         error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token是过期的',
                         error_code=1003)
    uid = data['uid']
    scope = data['scope']
    allow = is_in_scope(scope, request.endpoint)
    if not allow:
        raise Forbidden()
    return User(uid, scope)