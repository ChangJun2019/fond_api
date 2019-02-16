# -*- coding: utf-8 -*-
# @Time     : 2018/8/21 22:51
# @Author   : ChangJun
# @Email    : 52chinaweb@gmail.com
# @Function ：重写wtforms


from flask import request
from wtforms import Form
from app.libs.error_code import ParameterException


class BaseForm(Form):
    def __init__(self):
        data = request.get_json(silent=True)
        args = request.args.to_dict()
        super(BaseForm, self).__init__(data=data, **args)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            raise ParameterException(msg=self.errors)
        return self
