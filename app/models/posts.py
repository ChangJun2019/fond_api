# -*- coding: utf-8 -*-
# @Time    : 2018/12/29 12:36
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    : 帖子模型

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base, db
from datetime import datetime


class Posts(Base):
    """帖子数据模型"""
    id = Column(Integer, primary_key=True)  # id
    title = Column(String(50), unique=True)  # 标题
    cover = Column(Text)  # 主题封面
    images = Column(Text)  # 主题图片
    desc = Column(String(150))
    type = Column(Integer)  # 类型 1、文章 2、图文动态 3、视频动态
    atype = Column(Integer, default=1)  # 原创、转载、翻译
    videosrc = Column(Text)
    content = Column(Text)  # 内容
    topics = relationship('Topics')
    tid = Column(Integer, ForeignKey('topics.id'))
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))  # 创建的用户id
    reply_count = Column(Integer, default=0)  # 评论数
    visit_count = Column(Integer, default=0)  # 访问数
    like_count = Column(Integer, default=0)  # 点赞数
    good = Column(Integer, default=0)  # 是否加精
    top = Column(Integer, default=0)  # 是否推荐
    update_time = Column(Integer, default=int(datetime.now().timestamp()))  # 更新时间

    def keys(self):
        return ['id', 'title', 'cover', 'images', 'type', 'atype', 'content', 'tid', 'uid', 'reply_count',
                'visit_count', 'like_count', 'good', 'top', 'update_time', 'videosrc']

    @staticmethod
    def create_by_posts(form, uid):
        type = form.type.data
        if type == 1:
            Posts.create_by_articles(form.title.data, form.sort.data, form.cover.data, form.desc.data,
                                     form.content.data,
                                     form.type.data,
                                     form.atype.data,
                                     uid)
        if type == 2:
            Posts.create_by_states(form.title.data, form.sort.data, form.images.data, form.content.data,
                                   form.type.data, uid)
        if type == 3:
            Posts.create_by_video(form.title.data, form.sort.data, form.video.data, form.content.data,
                                  form.type.data, uid)

    @staticmethod
    def create_by_articles(title, sort, cover, desc, content, type, atype, uid):
        """ 创建文章帖子 """
        with db.auto_commit():
            posts = Posts()
            posts.title = title
            posts.tid = sort
            posts.cover = cover
            posts.desc = desc
            posts.content = content
            posts.type = type
            posts.atype = atype
            posts.uid = uid
            db.session.add(posts)

    @staticmethod
    def create_by_states(title, sort, images, content, type, uid):
        with db.auto_commit():
            posts = Posts()
            posts.title = title
            posts.tid = sort
            posts.images = ",".join(images)
            posts.type = type
            posts.content = content
            posts.uid = uid
            db.session.add(posts)

    @staticmethod
    def create_by_video(title, sort, video, content, type, uid):
        with db.auto_commit():
            posts = Posts()
            posts.title = title
            posts.tid = sort
            posts.videosrc = video
            posts.type = type
            posts.content = content
            posts.uid = uid
            db.session.add(posts)
