# -*- coding: utf-8 -*-
# @Time    : 2018/12/19 15:43
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    :

from app.models.posts import Posts
from app.models.message import Message


class UserViewModels:

    @classmethod
    def paginate_user_all(cls, data):
        """ 对要返回的所有用户进行分页加工处理"""
        returned = {
            "list": [cls.cut_get_my_user(user) for user in data.items],
            "pagination": {
                "total": data.total,
                "pageSize": data.per_page,
                "page": data.page,
                "pages": data.pages
            }
        }
        return returned

    @classmethod
    def cut_get_my_user(cls, data):
        tags = [] if data['tags'] is None else data['tags'].split(",")
        uid = data['id']
        up = Posts.query.filter_by(uid=uid).count()
        total_count = Message.query.filter_by(tuid=uid).count()
        pwd = True if data['password'] else False
        user = {
            'id': data['id'],
            'avatar': data['avatar'] or 'http://www.sucaijishi.com/uploadfile/2018/0508/20180508023754592.png',
            'gender': data['gender'] or '',
            'mobile': data['mobile'] or '',
            'nickname': data['nickname'] or '',
            'pro': data['pro'] or '',
            'sig': data['sig'] or '',
            'tags': tags,
            'email': data['email'] or '',
            'country': data['country'] or '',
            'auth': '普通用户' if data['auth'] == 1 else '管理员',
            'posts_count': up,
            'message_count': total_count,
            "create_time": data['create_time'],
            "has_pawd": pwd
        }
        if data['city'] is None and data['province'] is None:
            return user
        else:
            geographic = {
                "city": {
                    "key": data['city'].split(',')[0],
                    "label": data['city'].split(',')[1]
                },
                "province": {
                    "key": data['province'].split(',')[0],
                    "label": data['province'].split(',')[1]
                }
            }
            user['geographic'] = geographic
            return user
