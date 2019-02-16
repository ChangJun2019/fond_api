# -*- coding: utf-8 -*-
# @Time    : 2018/12/13 5:22
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    :

from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.validators.forms import RegisterUserForm
from app.models.user import User

""" 
 客户端注册接口
 /v1/client/ 
"""

api = Redprint('client')


@api.route('/register', methods=['POST'])
def create_user():
    form = RegisterUserForm().validate_for_api()
    User.register_by_user(form.account.data, form.password.data, form.mobile.data)
    return Success()