# -*- coding: utf-8 -*-
# @Time    : 2018/12/12 10:24
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    : 项目入口文件,对flask核心对象进行操作

from datetime import date
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder
from app.libs.error_code import ServerError

class JSONEncoder(_JSONEncoder):
    """由于原来的jsonify并不能序列化一个模型对象
    故实现自己的序列化机制,将自己定义的default覆盖
    原来jsonify
    """

    def default(self, o):
        # 返回一个字典
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        # 如果时间对象能转化的话利default递归的特性返回出来
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        raise ServerError()


class Flask(_Flask):
    """ 自己定义Flask对象继承原来的Flask对象
        将其json_encoder变成自己定义的JSONEncoder
    """
    json_encoder = JSONEncoder