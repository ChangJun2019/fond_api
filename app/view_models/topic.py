# -*- coding: utf-8 -*-
# @Time    : 2018/12/19 0:02
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    :
from app.models.topic_types import Topics
from app.models.user import User


class TopicViewModel:

    @classmethod
    def cut_one_topic_data(cls, data):
        topic = {
            'id': data['id'],
            'cover': data['cover'],
            'topic_name': data['topic_name'],
            'desc': data['desc']
        }
        user = User.query.filter_by(id=data['uid']).first()
        us = {
            'user_name': user['nickname'],
            'user_avatar': user['avatar']
        }
        topic['create_user'] = us
        return topic


    @classmethod
    def return_tow_topic(cls, data):
        topic = {
            'value': data['id'],
            'label': data['topic_name']
        }
        return topic

    @classmethod
    def find_tow_topic(cls, id, all_topics):
        topics = Topics.query.filter_by(parent_id=id).all()
        if topics:
            tow_topics = [cls.return_tow_topic(topic) for topic in topics]
            all_topics['children'] = tow_topics
        return all_topics

    @classmethod
    def return_one_topic(cls, data):
        id = data['id']
        all_topics = {
            'value': data['id'],
            'label': data['topic_name']
        }
        all_topics = cls.find_tow_topic(id, all_topics)
        return all_topics
