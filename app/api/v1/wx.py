# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 22:38
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    :
from flask import current_app, jsonify

from app.api.v1.token import generate_auth_token
from app.libs.help import getjscode2session
from app.libs.redprint import Redprint
from app.validators.forms import LoginWxForm
from app.models.user import User

api = Redprint('wx')


@api.route('/login', methods=['POST'])
def wx_login():
    form = LoginWxForm().validate_for_api()
    appid = current_app.config['WX_APPID']
    secret = current_app.config['WX_SECRET']
    wxres = getjscode2session(js_code=form.code.data, appid=appid, secret=secret)
    openid = wxres['openid']
    user = User.query.filter_by(openid=openid).first()
    if not user:
        User.register_by_user_wx(openid)
        ruser = User.query.filter_by(openid=openid).first()
        scope = 'AdminScope' if ruser.auth == 2 else 'UserScope'
        token = return_token(ruser.id, scope)
    else:
        ruser = User.query.filter_by(openid=openid).first()
        scope = 'AdminScope' if ruser.auth == 2 else 'UserScope'
        token = return_token(user.id, scope)
    return token


def return_token(uid, scope):
    """ 生成加密token"""
    token = generate_auth_token(uid, scope)
    t = {
        'token': token.decode('ascii')
    }
    return jsonify(t)
