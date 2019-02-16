# -*- coding: utf-8 -*-
# @Time     : 2018/8/21 22:42
# @Author   : ChangJun
# @Email    : 52chinaweb@gmail.com
# @Function ：红图对象


""" 自定义红图对象 """

""" 蓝图分离视图函数有两点问题,一是蓝图只是为了拆分模块并不是为了拆分视图函数
    而在编写代码时，我们的同一类可能有很多视图函数。而是url因前者也会变得很冗余。
"""

""" 因此定义红图对象"""


class Redprint():
    def __init__(self, name):
        self.name = name
        self.mound = []

    """ 实现路由注册参照蓝图代码,
        rule路由地址
        options参数
        定义mound为一个字典存储三个参数
    """

    def route(self, rule, **options):
        def decorator(f):
            # 将蓝图对象、路由、参数保存在定义好的列表当中
            self.mound.append((f, rule, options))
            return f

        return decorator

    """ 实现注册路由的方法 """

    def register(self, bp, url_prefix=None):
        # 如果没有指定的前缀就是该模块的名字
        # 为了优化我们的红图对象
        if url_prefix is None:
            url_prefix = '/' + self.name
        # 循环遍历字典拿到每一个参数
        for f, rule, options in self.mound:
            # 利用了字典pop方法,如果endpoint存在的话就讲其拿出来删掉原来存在的
            # 如果其不存在就将其指定为视图函数的名字
            endpoint = self.name + '+' + options.pop("endpoint", f.__name__)
            # 此处调用add_url_rule方法来实现路由的注册
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)
