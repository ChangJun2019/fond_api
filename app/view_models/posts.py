# -*- coding: utf-8 -*-
# @Time    : 2019/1/1 23:29
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    :

from app.models.user import User
from app.models.topic_types import Topics
from app.models.collect_posts import collect_posts
from app.models.comments import Comments


class PostsViewModels:

    @classmethod
    def get_all_posts_vstates(cls, data):
        returned = {
            "list": [cls.cut_get_my_vstates(item) for item in data],
            "count": len(data)
        }
        return returned

    @classmethod
    def get_all_posts_states(cls, data):
        returned = {
            "list": [cls.cut_get_my_states(item) for item in data],
            "count": len(data)
        }
        return returned

    @classmethod
    def get_all_posts_articles(cls, data):
        returned = {
            "list": [cls.cut_get_my_articles(item) for item in data],
            "count": len(data)
        }
        return returned

    @classmethod
    def paginate_all_video_states(cls, data):
        returned = {
            "list": [cls.cut_get_my_vstates(item) for item in data.items],
            "pagination": {
                "total": data.total,
                "pageSize": data.per_page,
                "page": data.page,
                "pages": data.pages
            }
        }
        return returned

    @classmethod
    def paginate_all_articles(cls, data):
        """ 对要返回的所有文章进行分页加工处理 """
        returned = {
            "list": [cls.cut_get_my_articles(item) for item in data.items],
            "pagination": {
                "total": data.total,
                "pageSize": data.per_page,
                "page": data.page,
                "pages": data.pages
            }
        }
        return returned

    @classmethod
    def paginate_all_states(cls, data):
        """ 对要返回的所有动态进行分页加工处理 """
        returned = {
            "list": [cls.cut_get_my_states(item) for item in data.items],
            "pagination": {
                "total": data.total,
                "pageSize": data.per_page,
                "page": data.page,
                "pages": data.pages
            }
        }
        return returned

    @classmethod
    def paginate_user_all_articles(cls, data):
        """ 对要返回的所有用户进行分页加工处理"""
        returned = {
            "list": [cls.cut_get_my_articles(item) for item in data.items],
            "total": data.total,  # 总条数
            "pages": data.pages,  # 总页数
            "page": data.page,  # 当前页数
            "per_page": data.per_page,  # 每页显示条数
            "has_next": data.has_next,  # 是否还有上一页
            "has_prev": data.has_prev  # 是否还有下一页
        }
        return returned

    @classmethod
    def cut_get_my_vstates(cls, data):
        uid = data['uid']
        tid = data['tid']
        post_id = data['id']
        user = User.query.filter_by(id=uid).first()
        topic = Topics.query.filter_by(id=tid).first()
        tuid = topic['uid']
        tuser = User.query.filter_by(id=tuid).first()
        comments = Comments.query.filter_by(posts_id=post_id).all()
        us = {
            "user_name": user['nickname'],
            "user_avatar": user['avatar']
        }
        ts = {
            "topics_name": topic['topic_name'],
            "created_user": tuser['nickname'],
            "create_time": topic['create_time']
        }
        vstates = {
            "id": data['id'],
            "titile": data['title'],
            "content": data['content'],
            "videosrc": data['videosrc'],
            "reply_count": data['reply_count'],
            "visit_count": data['visit_count'],
            "like_count": data['like_count'],
            "update_time": data['update_time'],
            "good": data['good'],
            "top": data["top"],
            "create_time": topic['create_time'],
            "created_user": us,
            "from_topic": ts,
            "comments": [cls.cut_comments_by_posts(item) for item in comments]
        }
        return vstates

    @classmethod
    def cut_comments_by_posts(cls, data):
        fromuid = data['from_uid']
        user = User.query.filter_by(id=fromuid).first()
        return {
            "id": data['id'],
            "create_time": data['create_time'],
            "content": data["content"],
            "comment_user": {
                "user_name": user['nickname'],
                "user_avatar": user['avatar']
            }
        }

    @classmethod
    def cut_get_my_states(cls, data):
        uid = data['uid']
        tid = data['tid']
        sid = data['id']
        post_id = data['id']
        user = User.query.filter_by(id=uid).first()
        topic = Topics.query.filter_by(id=tid).first()
        tuid = topic['uid']
        tuser = User.query.filter_by(id=tuid).first()
        collects = collect_posts.query.filter_by(uid=uid, posts_id=sid, collecting_status=2).limit(8)
        collects_count = collect_posts.query.filter_by(uid=uid, posts_id=sid, collecting_status=2).count()
        collecting_user = [cls.cut_user_info(item) for item in collects]
        comments = Comments.query.filter_by(posts_id=post_id).all()
        us = {
            "user_name": user['nickname'],
            "user_avatar": user['avatar']
        }
        ts = {
            "topics_name": topic['topic_name'],
            "created_user": tuser['nickname'],
            "cover": topic["cover"],
            "create_time": topic['create_time']
        }
        states = {
            "id": data['id'],
            "titile": data['title'],
            "images": data['images'].split(','),
            "content": data['content'],
            "reply_count": data['reply_count'],
            "visit_count": data['visit_count'],
            "like_count": data['like_count'],
            "update_time": data['update_time'],
            "collects_count": collects_count,
            "create_time": topic['create_time'],
            "created_user": us,
            "from_topic": ts,
            "good": data['good'],
            "top": data["top"],
            "collectors": collecting_user,
            "comments": [cls.cut_comments_by_posts(item) for item in comments]
        }
        return states

    @classmethod
    def cut_get_my_articles(cls, data):
        uid = data['uid']
        tid = data['tid']
        aid = data['id']
        post_id = data['id']
        user = User.query.filter_by(id=uid).first()
        topic = Topics.query.filter_by(id=tid).first()
        tuid = topic['uid']
        tuser = User.query.filter_by(id=tuid).first()
        collects = collect_posts.query.filter_by(uid=uid, posts_id=aid, collecting_status=2).limit(8)
        collects_count = collect_posts.query.filter_by(uid=uid, posts_id=aid, collecting_status=2).count()
        collecting_user = [cls.cut_user_info(item) for item in collects]
        comments = Comments.query.filter_by(posts_id=post_id).all()
        us = {
            "user_name": user['nickname'],
            "user_avatar": user['avatar'],
            "user_id": user['id']
        }
        ts = {
            "topics_name": topic['topic_name'],
            "created_user": tuser['nickname'],
            "cover": topic["cover"],
            "create_time": topic['create_time']
        }
        articles = {
            "id": data['id'],
            "titile": data['title'],
            "cover": data["cover"],
            "desc": data['desc'],
            "type": data['type'],  # 1文章 2动态 3视频动态
            "atype": data['atype'],  # 1原创 2转载 3翻译
            "reply_count": data['reply_count'],
            "visit_count": data['visit_count'],
            "like_count": data['like_count'],
            "content": data["content"],
            "collects_count": collects_count,
            "update_time": data['update_time'],
            "good": data['good'],
            "top": data["top"],
            "created_user": us,
            "from_topic": ts,
            "collectors": collecting_user,
            "comments": [cls.cut_comments_by_posts(item) for item in comments]
        }
        return articles

    @classmethod
    def cut_user_info(cls, data):
        id = data['uid']
        user = User.query.filter_by(id=id).first()
        us = {
            "user_name": user['nickname'],
            "user_avatar": user['avatar']
        }
        return us
