# -*- coding: utf-8 -*-
# @Time    : 2019/1/2 1:30
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    :
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, db
from datetime import datetime


class collect_posts(Base):
    """ 收藏文章数据模型 """
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))  # 用户id
    posts_id = Column(Integer)
    collecting_status = Column(Integer, default=2)  # 1 收藏 2 未收藏
    update_time = Column(Integer, default=int(datetime.now().timestamp()))

    def keys(self):
        return ['id', 'uid', 'posts_id', 'collecting_status','update_time']

    @staticmethod
    def collecting_posts(id, uid):
        collecting = collect_posts.query.filter_by(posts_id=id, uid=uid).first()
        if not collecting:
            collect_posts.create_by_collecting(id, uid)
        else:
            with db.auto_commit():
                status = collecting.collecting_status
                collecting.collecting_status = 2 if status == 1 else 1
                collecting.update_time = int(datetime.now().timestamp())

    @staticmethod
    def create_by_collecting(id, uid):
        with db.auto_commit():
            collecting = collect_posts()
            collecting.uid = uid
            collecting.posts_id = id
            db.session.add(collecting)
