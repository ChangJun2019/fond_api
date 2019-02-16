# -*- coding: utf-8 -*-
# @Time    : 2018/12/13 5:00
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    :

from flask import jsonify, g
from app.libs.error_code import DeleteSuccess, PutSuccess, Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.user import User, db
from app.models.follow_user import follow_user
from app.models.follow_topic import follow_topics
from app.validators.forms import UpdateUserMsg, GetAllUsers, FollowedUsers, AddUserTags, DeleteInBatches, SetUserAuth
from app.view_models.user import UserViewModels
from app.view_models.usertopics import UserTopicsViewModels

api = Redprint('user')


@api.route('/<int:uid>', methods=['GET'])
@auth.login_required
def get_some_user(uid):
    """ 获取一个用户的用户信息 """
    user = User.query.get_or_404(uid)
    user = UserViewModels.cut_get_my_user(user)
    return jsonify(user)


@api.route('', methods=['GET'])
@auth.login_required
def get_my_user():
    """ 获取当前登录用户的信息 """
    uid = g.user.uid
    user = User.query.filter_by(id=uid).first_or_404()
    user = UserViewModels.cut_get_my_user(user)
    return jsonify(user)


@api.route('/all', methods=['POST'])
@auth.login_required
def get_all_user():
    """ 获取所有的用户信息 """
    form = GetAllUsers().validate_for_api()
    users = get_uses_all_data(form)
    users = UserViewModels.paginate_user_all(users)
    return jsonify(users)


@api.route('/<int:uid>', methods=['DELETE'])
@auth.login_required
def delete_user(uid):
    """ 删除一个用户 """
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404()
        user.delete()
    return DeleteSuccess()


@api.route('/delete', methods=['POST'])
@auth.login_required
def delete_in_batches_user():
    """ 批量删除用户 """
    form = DeleteInBatches().validate_for_api()
    ids = tuple(form.idTuple.data)
    with db.auto_commit():
        users = User.query.filter(User.id.in_(ids))
        [user.delete() for user in users]
    return DeleteSuccess()


@api.route('', methods=['PUT'])
@auth.login_required
def update_user_msg():
    """ 修改当前登录用户个人信息 """
    uid = g.user.uid
    form = UpdateUserMsg().validate_for_api()
    User.update_user_msg(uid, form.nickname.data, form.avatar.data, form.gender.data, form.pro.data, form.sig.data,
                         form.country.data,form.mobile.data, form.geographic.data)
    return PutSuccess()


@api.route('/followed', methods=['POST'])
@auth.login_required
def followed_topics():
    """ 关注主题"""
    uid = g.user.uid
    form = FollowedUsers().validate_for_api()
    follow_user.followed_users(form.id.data, uid)
    return Success()


@api.route('/auth', methods=['PUT'])
@auth.login_required
def set_user_auth():
    """ 设置管理员 """
    form = SetUserAuth().validate_for_api()
    with db.auto_commit():
        user = User.query.filter_by(id=form.id.data).first_or_404()
        user.auth = 2
    return Success()


@api.route('/followed', methods=['GET'])
@auth.login_required
def get_current_user_followed_topic():
    """ 当前用户关注的主题 """
    uid = g.user.uid,
    topics = follow_topics.query.filter_by(uid=uid, followed_status=2).all()
    followedTopics = [UserTopicsViewModels.cut_get_user_all_topics(topic) for topic in topics]
    return jsonify(followedTopics)


@api.route('/tags', methods=['PUT'])
@auth.login_required
def put_user_tags():
    """ 增加当前用户的标签 """
    uid = g.user.uid,
    form = AddUserTags().validate_for_api()
    User.put_user_new_tag(form.tag_title.data, uid)
    return Success()


def get_uses_all_data(form):
    """ 多条件查询模糊查询用户列表 """
    users = User.query.filter_by()
    if form.auth.data:
        users = User.query.filter_by(auth=form.auth.data)
    if form.gender.data:
        users = User.query.filter_by(gender=form.gender.data)
    if form.auth.data and form.gender.data:
        users = User.query.filter_by(auth=form.auth.data, gender=form.gender.data)
    nickname_words = form.nickname.data.strip() if form.nickname.data else ""
    users = users.filter(
        User.nickname.like("%" + nickname_words + "%"),
    ).paginate(page=form.page.data,
               per_page=form.per_page.data,
               error_out=False)
    return users
