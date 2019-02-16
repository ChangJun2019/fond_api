# -*- coding: utf-8 -*-
# @Time    : 2018/12/12 10:54
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    :

from flask import Blueprint

from app.api.v1 import user, client, token, wx, topics, posts, review, message


def create_blueprint_v1():
    """
        创建一个蓝图对象,当我们将每一个模块实例化红图对象后,我们需要将实例化后的红图对象
    注册一下蓝图对象。因此在我们的模块中创建一个蓝图对象。导入每一个模块下面的红图对象后
    注册一下创建的蓝图对象。
    """
    bp_v1 = Blueprint('v1', __name__)
    user.api.register(bp_v1)
    client.api.register(bp_v1)
    token.api.register(bp_v1)
    wx.api.register(bp_v1)
    topics.api.register(bp_v1)
    posts.api.register(bp_v1)
    review.api.register(bp_v1)
    message.api.register(bp_v1)
    return bp_v1
