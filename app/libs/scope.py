# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 20:50
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    :

class Scope:
    allow_api = []
    allow_module = []
    forbidden = []

    def __add__(self, other):
        self.allow_api = self.allow_api + other.allow_api
        self.allow_api = list(set(self.allow_api))
        # 运算符重载

        self.allow_module = self.allow_module + \
                            other.allow_module
        self.allow_module = list(set(self.allow_module))

        self.forbidden = self.forbidden + other.forbidden
        self.forbidden = list(set(self.forbidden))

        return self


class AdminScope(Scope):
    # allow_api = ['v1.super_get_user',
    #              'v1.super_delete_user']
    allow_module = ['v1.user', 'v1.topics', 'v1.token', 'v1.posts', 'v1.review','v1.message']

    def __init__(self):
        # 排除
        pass
        # self + UserScope()


class UserScope(Scope):
    allow_module = ['v1.user', 'v1.topics', 'v1.token', 'v1.posts', 'v1.review','v1.message']
    forbidden = ['v1.user+delete_user',
                 'v1.user+delete_in_batches_user',
                 'v1.user+set_user_auth',
                 'v1.topics+create_topic',
                 'v1.topics+update_topic_msg',
                 'v1.topics+delete_topic',
                 ]

    def __init__(self):
        self + AdminScope()


def is_in_scope(scope, endpoint):
    # globals 可以将当前模块下面所有的变量（包含类）变成一个dict
    scope = globals()[scope]()
    splits = endpoint.split('+')
    red_name = splits[0]
    if endpoint in scope.forbidden:
        return False
    if endpoint in scope.allow_api:
        return True
    if red_name in scope.allow_module:
        return True
    else:
        return False
