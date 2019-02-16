# -*- coding: utf-8 -*-
# @Time    : 2019/1/5 7:34
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    : 评论点赞

from sqlalchemy import Column, Integer, ForeignKey
from app.models.base import Base, db
from sqlalchemy.orm import relationship
from datetime import datetime


class like_comments(Base):
    """ 评论点赞表 """
    id = Column(Integer, primary_key=True)
    posts_id = Column(Integer)  # 帖子id
    uid = Column(Integer)  # 用户id
    comments = relationship('Comments')
    comment_id = Column(Integer, ForeignKey('comments.id'))  # 评论id
    like_status = Column(Integer, default=0)  # 点赞状态 0 未点赞 1 点赞
    update_time = Column(Integer, default=int(datetime.now().timestamp()))

    def keys(self):
        return ['id', 'posts_id', 'uid', 'comment_id', 'like_status', 'update_time']

    @staticmethod
    def like_to_comments(pid, cid, uid):
        """ 查询是否已存在点赞记录 如果不存在就创建 """
        likes = like_comments.query.filter_by(posts_id=pid, comment_id=cid, uid=uid).first()
        if not likes:
            like_comments.create_like_comments(pid, cid, uid)
        else:
            with db.auto_commit():
                status = likes.like_status
                likes.like_status = 1 if status == 0 else 0
                likes.update_time = int(datetime.now().timestamp())

    @staticmethod
    def create_like_comments(pid, cid, uid):
        with db.auto_commit():
            likecomments = like_comments()
            likecomments.posts_id = pid
            likecomments.uid = uid
            likecomments.comment_id = cid
            db.session.add(likecomments)
