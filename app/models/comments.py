# -*- coding: utf-8 -*-
# @Time    : 2019/1/5 7:21
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    : 评论

from sqlalchemy import Column, Integer, String
from app.models.base import Base, db
from datetime import datetime


class Comments(Base):
    """ 评论表 """
    id = Column(Integer, primary_key=True)
    posts_id = Column(Integer)  # 帖子id
    content = Column(String(150))  # 内容
    from_uid = Column(Integer)  # 评论人id
    to_uid = Column(Integer)  # 评论评论人id
    update_time = Column(Integer, default=int(datetime.now().timestamp()))

    def keys(self):
        return ['id', 'posts_id', 'content', 'from_uid', 'to_uid', "update_time"]

    @staticmethod
    def create_by_comments(pid, content, uid, tuid):
        """ 创建评论 """
        with db.auto_commit():
            comments = Comments()
            comments.posts_id = pid
            comments.content = content
            comments.from_uid = uid
            comments.to_uid = tuid
            db.session.add(comments)
