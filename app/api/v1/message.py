# -*- coding: utf-8 -*-
# @Time    : 2019/1/7 6:21
# @Author  : ChangJun
# @Email   : 52chinaweb@gmail.com 
# @desc    : 消息


from flask import g, jsonify

from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.validators.forms import CreateNewMessage, ChangeMessageStatus
from app.models.message import Message
from app.view_models.message import MessageViewModel

api = Redprint('message')


@api.route("", methods=['PUT'])
@auth.login_required
def create_by_message():
    """ 创建一个新的消息 """
    uid = g.user.uid
    form = CreateNewMessage().validate_for_api()
    Message.create_by_message(form, uid)
    return Success()


@api.route("/changed", methods=['PUT'])
@auth.login_required
def change_message_status():
    """ 修改一个消息的状态 """
    form = ChangeMessageStatus().validate_for_api()
    Message.change_message_status(id=form.id.data)
    return Success()


@api.route("", methods=['GET'])
@auth.login_required
def get_current_user_message():
    """ 获取用户的消息 """
    uid = g.user.uid
    unread_messages = Message.query.filter_by(tuid=uid, read_staus=0).all()
    unread_count = Message.query.filter_by(tuid=uid, read_staus=0).count()
    read_messages = Message.query.filter_by(tuid=uid, read_staus=1).all()
    read_count = Message.query.filter_by(tuid=uid, read_staus=1).count()
    total_count = Message.query.filter_by(tuid=uid).count()
    returned = {
        "unread_messages": [MessageViewModel.cut_user_message(item) for item in unread_messages],
        "read_messages": [MessageViewModel.cut_user_message(item) for item in read_messages],
        "total_count": total_count,
        "unread_count": unread_count,
        'read_count': read_count
    }
    return jsonify(returned)
