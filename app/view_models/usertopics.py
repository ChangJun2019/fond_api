# -*- coding: utf-8 -*-
# @Time    : 2018/12/31 1:13
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    :

from app.models.topic_types import Topics
from app.models.user import User


class UserTopicsViewModels:

    @classmethod
    def cut_get_user_all_topics(cls, data):
        """ 获取当前用户关注的主题，对相关信息进行处理 """
        tid = data['followed_topic']
        topics = Topics.query.filter_by(id=tid).first()
        tuid = topics.uid
        user = User.query.filter_by(id=tuid).first()
        created_user = {
            "user_id": tuid,
            "user_name": user.nickname,
            "user_avater": user.avatar or ''
        }
        t = {
            "topic_id": tid,
            "topic_name": topics.topic_name,
            "cover": topics.cover,
            "created_user": created_user
        }
        return t
