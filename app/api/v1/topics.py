# -*- coding: utf-8 -*-
# @Time    : 2018/12/18 18:37
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    :
from app.libs.error_code import Success, PutSuccess, DeleteSuccess
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.validators.forms import CreateNewTopics, UpdateTopicsMsg, FollowedTopics
from app.models.topic_types import Topics, db
from app.models.follow_topic import follow_topics
from app.view_models.topic import TopicViewModel
from flask import jsonify, g

api = Redprint('topics')


@api.route('', methods=['POST'])
@auth.login_required
def create_topic():
    """ 创建分类主题(包含二级分类) """
    uid = g.user.uid
    form = CreateNewTopics().validate_for_api()
    Topics.create_by_topic(form.topic_name.data, form.cover.data, form.desc.data, uid, form.parent_id.data)
    topic = Topics.query.filter_by(topic_name=form.topic_name.data).first()
    tid = {
        "topic_id": topic.id  # 返回创建好的分类id
    }
    return Success(msg=tid)


@api.route('', methods=['GET'])
@auth.login_required
def get_one_topic():
    """ 获取一级分类 """
    topic = Topics.query.filter_by(parent_id=0).all()
    topics = [TopicViewModel.cut_one_topic_data(topic) for topic in topic]
    return jsonify(topics)


@api.route('/<int:pid>', methods=['GET'])
@auth.login_required
def get_some_one_child_topic(pid):
    """ 查询一个一级分类下面的主题 """
    topic = Topics.query.filter_by(parent_id=pid).all()
    topics = [TopicViewModel.cut_one_topic_data(topic) for topic in topic]
    return jsonify(topics)


@api.route('', methods=['PUT'])
@auth.login_required
def update_topic_msg():
    """ 修改某个主题的信息 """
    form = UpdateTopicsMsg().validate_for_api()
    Topics.update_by_topic(form.id.data, form.topic_name.data, form.cover.data, form.desc.data)
    return PutSuccess()


@api.route('/<int:tid>', methods=['DELETE'])
@auth.login_required
def delete_topic(tid):
    """ 删除某个主题 """
    with db.auto_commit():
        topic = Topics.query.filter_by(id=tid).first_or_404()
        tow_topics = Topics.query.filter_by(parent_id=tid).all()
        topic.delete()
        for tow_topic in tow_topics:
            tow_topic.delete()
    return DeleteSuccess()


@api.route('/all', methods=['GET'])
@auth.login_required
def get_all_topics():
    """ 获取一级主题一级下面的二级主题 """
    topics = Topics.query.filter_by(parent_id=0).all()
    all_topics = [TopicViewModel.return_one_topic(topic) for topic in topics]
    return jsonify(all_topics)


@api.route('/followed', methods=['POST'])
@auth.login_required
def followed_topics():
    """ 关注主题"""
    uid = g.user.uid
    form = FollowedTopics().validate_for_api()
    follow_topics.followed_topics(form.id.data, uid)
    return Success()
