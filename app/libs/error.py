# -*- coding: utf-8 -*-
# @Time     : 2018/8/21 22:52
# @Author   : ChangJun
# @Email    : 52chinaweb@gmail.com
# @Function ：重写HTTPException，意在返回restful api异常方法

from flask import request, json
from werkzeug.exceptions import HTTPException

class APIException(HTTPException):
    """ 自定义API异常方法,继承HTTPException"""
    code = 500
    msg = '服务端产生未知的错误'
    error_code = 999
    def __init__(self, msg=None, code=None, error_code=None, headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request=request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]


    @staticmethod
    def get_url_no_param():
        """ 获取没有？后面的参数的请求路径"""
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]
