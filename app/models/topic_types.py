# -*- coding: utf-8 -*-
# @Time    : 2018/12/18 16:08
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    : 话题分类表

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, db


class Topics(Base):
    """ 主题分类表 """
    id = Column(Integer, primary_key=True)
    topic_name = Column(String(24), unique=True)  # 主题名字
    parent_id = Column(Integer, default=0)  # 父类id
    cover = Column(Text)  # 主题封面
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))  # 创建的用户id
    desc = Column(String(100))  # 主题描述

    def keys(self):
        return ['id', 'topic_name', 'parent_id', 'cover', 'desc', 'follow_count', 'uid']

    @staticmethod
    def create_by_topic(name, cover, desc, uid, parent_id=0, ):
        """ 创建一个主题 """
        with db.auto_commit():
            topics = Topics()
            topics.topic_name = name
            topics.cover = cover
            topics.desc = desc
            topics.uid = uid
            topics.parent_id = parent_id
            db.session.add(topics)

    @staticmethod
    def update_by_topic(tid, name, cover, desc):
        with db.auto_commit():
            topic = Topics.query.filter_by(id=tid).first_or_404()
            if name:
                topic.topic_name = name
            if cover:
                topic.cover = cover
            if desc:
                topic.desc = desc
