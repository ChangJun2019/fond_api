# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 18:01
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    :
from flask import current_app, jsonify,session
import requests
import random
from qiniu import Auth
from app.libs.error_code import Success, ParameterException, MobileException
from app.libs.redprint import Redprint
from app.validators.forms import LoginUserForm, GetVerifyCode, VerifyCode
from app.models.user import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.libs.token_auth import auth

api = Redprint('token')


@api.route('/login', methods=['POST'])
def get_token():
    form = LoginUserForm().validate_for_api()
    identity = User.verify(form.account.data, form.password.data)
    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generate_auth_token(identity['uid'],
                                identity['scope'],
                                expiration)
    t = {
        'token': token.decode('ascii'),
        'scope': identity['scope'],
        'msg': 'ok'
    }
    return jsonify(t), 201


def generate_auth_token(uid, scope=None,
                        expiration=7200):
    """生成令牌"""
    s = Serializer(current_app.config['SECRET_KEY'],
                   expires_in=expiration)
    return s.dumps({
        'uid': uid,
        'scope': scope
    })


@api.route('/qiniu', methods=['GET'])
@auth.login_required
def get_qiniu_token():
    """ 获取七牛云token """
    access_key = current_app.config['ACCESS_KEY']
    secret_key = current_app.config['SECRET_KEY']
    q = Auth(access_key, secret_key)
    bucket_name = current_app.config['BUCKET_NAME']
    token = q.upload_token(bucket_name, key=None)
    t = {
        "token": token
    }
    return Success(msg=t)


@api.route('/code', methods=['POST'])
@auth.login_required
def get_verif_code():
    """ 获取验证码"""
    form = GetVerifyCode().validate_for_api()
    user = User.query.filter_by(mobile=form.mobile.data).first()
    if user:
        return MobileException()
    else:
        url = "http://v.juhe.cn/sms/send"
        code = "".join(str(i) for i in random.sample(range(0, 9), 4))
        params = {
            "mobile": form.mobile.data,
            "tpl_id": current_app.config["VERIFY_ID"],
            "tpl_value": "#code#=" + code,
            "key": current_app.config["VERIFY_KEY"],
        }
        res = requests.post(url=url, data=params)
        session['verify_code'] = code
        res = res.json()
        if res["error_code"] == 0:
            return Success(msg='获取短信成功')
        else:
            return ParameterException(msg="获取错误")


@api.route('/verifycode', methods=['POST'])
@auth.login_required
def verify_code():
    """ 验证手机验证码 """
    form = VerifyCode().validate_for_api()
    code = session.get('verify_code')
    if session.get('verify_code') == form.code.data:
        return Success(msg='验证通过')
    else:
        return ParameterException(msg='验证码错误，请重新输入！')
