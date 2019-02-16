# -*- coding: utf-8 -*-
# @Time     : 2018/8/23 10:14
# @Author   : ChangJun
# @Email    : 52chinaweb@gmail.com
# @Function ：工具函数
import requests


def getjscode2session(js_code, appid, secret):
    """ 获取微信服务端用户唯一标识和会话秘钥 """
    url = ('https://api.weixin.qq.com/sns/jscode2session?'
           'appid={}&secret={}&js_code={}&grant_type=authorization_code'
           ).format(appid, secret, js_code)
    res = requests.get(url)
    return res.json()
