# -*- coding: utf-8 -*-
# @Time    : 2018/12/18 16:29
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    :
from sqlalchemy import Column, Integer, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, db
from datetime import datetime


class follow_topics(Base):
    """ 关注主题关系数据模型 """
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))  # 创建的用户id
    topics = relationship('Topics')
    followed_topic = Column(Integer, ForeignKey('topics.id'))  # 关注的主题id
    followed_status = Column(SmallInteger, default=2)  # 1 未关注 2关注
    update_time = Column(Integer, default=int(datetime.now().timestamp()))  # 更新时间

    def keys(self):
        return ['id', 'uid', 'followed_topic', 'followed_status']

    @staticmethod
    def followed_topics(id, uid):
        """ 判断当前数据库是否有记录，如果没有创建,有判断关注字段修改关注或取消 """
        followed = follow_topics.query.filter_by(followed_topic=id, uid=uid).first()
        if not followed:
            follow_topics.create_by_followed(id, uid)
        else:
            with db.auto_commit():
                status = followed.followed_status
                followed.followed_status = 2 if status == 1 else 1
                followed.update_time = int(datetime.now().timestamp())



    @staticmethod
    def create_by_followed(id, uid):
        """ 创建一条关注记录 """
        with db.auto_commit():
            followed = follow_topics()
            followed.uid = uid,
            followed.followed_topic = id
            db.session.add(followed)
