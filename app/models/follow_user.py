# -*- coding: utf-8 -*-
# @Time    : 2018/12/18 17:10
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    :

from app.models.base import Base, db
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class follow_user(Base):
    """ 用户关注关系表 """
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))  # 创建的用户id
    followed_user = Column(Integer, nullable=False)
    followed_status = Column(Integer, default=2)  # 1 未关注 2 关注
    update_time = Column(Integer, default=int(datetime.now().timestamp()))  # 更新时间

    def keys(self):
        return ['id', 'uid', 'followed_user', 'followed_status']

    @staticmethod
    def followed_users(id, uid):
        """ 判断当前数据库是否有记录，如果没有创建,有判断关注字段修改关注或取消 """
        followed = follow_user.query.filter_by(followed_user=id, uid=uid).first()
        if not followed:
            follow_user.create_by_followed(id, uid)
        else:
            with db.auto_commit():
                status = followed.followed_status
                followed.followed_status = 2 if status == 1 else 1
                followed.update_time = int(datetime.now().timestamp())

    @staticmethod
    def create_by_followed(id, uid):
        """ 创建一条关注记录 """
        with db.auto_commit():
            followed = follow_user()
            followed.uid = uid,
            followed.followed_user = id
            db.session.add(followed)
